"""In-memory subscriber store (alpha — mirrors meritstore alpha mode)."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .consumer_mirror import (
    DIRT_CONSUMER_ID,
    dirt_mirror_uuid,
    dirt_namespace_grants,
    dirt_product_to_ladder,
    validate_dirt_sync_payload,
)
from .freemium import FreemiumPolicy, required_tier_by_age
from .tiers import TIER_GUEST, TIER_REGISTERED, validate_tier
from .verification import VerificationState


@dataclass
class Subscriber:
  id: str
  tier: str
  handle: str | None = None
  email: str | None = None
  consumer_id: str = "meritsubs"
  verification: VerificationState = field(default_factory=VerificationState)
  namespace_grants: dict[str, list[str]] = field(default_factory=dict)
  created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
  freemium_policy: FreemiumPolicy = field(default_factory=FreemiumPolicy)

  def to_dict(self) -> dict[str, Any]:
    required, reason = required_tier_by_age(
      created_at=self.created_at,
      current_tier=self.tier,
      policy=self.freemium_policy,
    )
    return {
      "subscriber_id": self.id,
      "tier": self.tier,
      "handle": self.handle,
      "email": self.email,
      "consumer_id": self.consumer_id,
      "verification": self.verification.to_dict(),
      "grants": self.namespace_grants,
      "created_at": self.created_at.isoformat(),
      "upgrade_required": {"tier": required, "reason": reason} if required else None,
    }


class SubscriberStore:
  def __init__(self, persist_path: Path | None = None):
    self._subscribers: dict[str, Subscriber] = {}
    self._persist_path = persist_path

  def onboard_guest(self, *, handle: str, consumer_id: str) -> Subscriber:
    sub = Subscriber(
      id=str(uuid.uuid4()),
      tier=TIER_GUEST,
      handle=handle.strip(),
      consumer_id=consumer_id,
    )
    self._subscribers[sub.id] = sub
    self._maybe_persist()
    return sub

  def onboard_registered(self, *, email: str, consumer_id: str) -> Subscriber:
    sub = Subscriber(
      id=str(uuid.uuid4()),
      tier=TIER_REGISTERED,
      email=email.strip().lower(),
      consumer_id=consumer_id,
    )
    self._subscribers[sub.id] = sub
    self._maybe_persist()
    return sub

  def mark_certified(self, subscriber_id: str, *, square_ref: str) -> Subscriber:
    sub = self._get(subscriber_id)
    sub.verification.payment_status = "verified"
    sub.verification.square_verification_ref = square_ref
    sub.tier = validate_tier("certified")
    self._maybe_persist()
    return sub

  def attest_age(
    self,
    subscriber_id: str,
    *,
    date_of_birth_iso: str,
    age_band: str,
  ) -> Subscriber:
    sub = self._get(subscriber_id)
    if sub.verification.payment_status != "verified":
      raise ValueError("payment verification required before age attestation")
    sub.verification.age_status = "self_attested"
    sub.verification.age_band = age_band  # type: ignore[assignment]
    sub.verification.attestation_at = datetime.now(timezone.utc).isoformat()
    sub.tier = validate_tier("age_verified")
    self._maybe_persist()
    return sub

  def add_grants(self, subscriber_id: str, namespace: str, keys: list[str]) -> Subscriber:
    sub = self._get(subscriber_id)
    existing = set(sub.namespace_grants.get(namespace, []))
    existing.update(keys)
    sub.namespace_grants[namespace] = sorted(existing)
    self._maybe_persist()
    return sub

  def get(self, subscriber_id: str) -> Subscriber | None:
    return self._subscribers.get(subscriber_id)

  def sync_consumer_mirror(
    self,
    *,
    action: str,
    subscriber: dict[str, Any],
    consumer_id: str = DIRT_CONSUMER_ID,
  ) -> Subscriber | None:
    """DIRT admin CRUD mirror — external subscriber_id is the stable key."""
    external_id, product_tier = validate_dirt_sync_payload(action, subscriber)
    internal_id = dirt_mirror_uuid(external_id)
    if action == "delete":
      self._subscribers.pop(internal_id, None)
      self._maybe_persist()
      return None
    ladder_tier = dirt_product_to_ladder(product_tier)
    grants = dirt_namespace_grants(product_tier)
    existing = self.get(internal_id)
    if existing:
      existing.tier = ladder_tier
      existing.namespace_grants = grants
      existing.consumer_id = consumer_id
      existing.handle = external_id
      self._maybe_persist()
      return existing
    sub = Subscriber(
      id=internal_id,
      tier=ladder_tier,
      handle=external_id,
      consumer_id=consumer_id,
      namespace_grants=grants,
    )
    self._subscribers[sub.id] = sub
    self._maybe_persist()
    return sub

  def _get(self, subscriber_id: str) -> Subscriber:
    sub = self.get(subscriber_id)
    if not sub:
      raise KeyError(subscriber_id)
    return sub

  def _maybe_persist(self) -> None:
    if not self._persist_path:
      return
    payload = {sid: s.to_dict() for sid, s in self._subscribers.items()}
    self._persist_path.parent.mkdir(parents=True, exist_ok=True)
    self._persist_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
