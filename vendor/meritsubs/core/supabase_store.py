"""Supabase PostgREST backend for subscriber store (production / Vercel)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

from .consumer_mirror import (
    DIRT_CONSUMER_ID,
    dirt_mirror_uuid,
    dirt_namespace_grants,
    dirt_product_to_ladder,
    validate_dirt_sync_payload,
)
from .freemium import FreemiumPolicy
from .store import Subscriber
from .tiers import TIER_GUEST, TIER_REGISTERED, validate_tier
from .verification import VerificationState


class SupabaseSubscriberStore:
    """Same surface as SubscriberStore; persists via Supabase REST."""

    def __init__(self, url: str, service_role_key: str, *, timeout: float = 20.0):
        self._base = url.rstrip("/") + "/rest/v1"
        self._headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        self._client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def onboard_guest(self, *, handle: str, consumer_id: str) -> Subscriber:
        row = self._insert_row(
            {
                "tier": TIER_GUEST,
                "handle": handle.strip(),
                "consumer_id": consumer_id,
            }
        )
        return self._from_row(row)

    def onboard_registered(self, *, email: str, consumer_id: str) -> Subscriber:
        row = self._insert_row(
            {
                "tier": TIER_REGISTERED,
                "email": email.strip().lower(),
                "consumer_id": consumer_id,
            }
        )
        return self._from_row(row)

    def mark_certified(self, subscriber_id: str, *, square_ref: str) -> Subscriber:
        sub = self._get_required(subscriber_id)
        sub.verification.payment_status = "verified"
        sub.verification.square_verification_ref = square_ref
        sub.tier = validate_tier("certified")
        return self._save(sub)

    def attest_age(
        self,
        subscriber_id: str,
        *,
        date_of_birth_iso: str,
        age_band: str,
    ) -> Subscriber:
        sub = self._get_required(subscriber_id)
        if sub.verification.payment_status != "verified":
            raise ValueError("payment verification required before age attestation")
        sub.verification.age_status = "self_attested"
        sub.verification.age_band = age_band  # type: ignore[assignment]
        sub.verification.attestation_at = datetime.now(timezone.utc).isoformat()
        sub.tier = validate_tier("age_verified")
        return self._save(sub)

    def add_grants(self, subscriber_id: str, namespace: str, keys: list[str]) -> Subscriber:
        sub = self._get_required(subscriber_id)
        existing = set(sub.namespace_grants.get(namespace, []))
        existing.update(keys)
        sub.namespace_grants[namespace] = sorted(existing)
        return self._save(sub)

    def get(self, subscriber_id: str) -> Subscriber | None:
        res = self._client.get(
            f"{self._base}/subscribers",
            params={"id": f"eq.{subscriber_id}", "select": "*"},
            headers=self._headers,
        )
        res.raise_for_status()
        rows = res.json()
        if not rows:
            return None
        return self._from_row(rows[0])

    def sync_consumer_mirror(
        self,
        *,
        action: str,
        subscriber: dict[str, Any],
        consumer_id: str = DIRT_CONSUMER_ID,
    ) -> Subscriber | None:
        external_id, product_tier = validate_dirt_sync_payload(action, subscriber)
        internal_id = dirt_mirror_uuid(external_id)
        if action == "delete":
            self._client.delete(
                f"{self._base}/subscribers",
                params={"id": f"eq.{internal_id}"},
                headers=self._headers,
            )
            return None
        ladder_tier = dirt_product_to_ladder(product_tier)
        grants = dirt_namespace_grants(product_tier)
        existing = self.get(internal_id)
        if existing:
            existing.tier = ladder_tier
            existing.namespace_grants = grants
            existing.consumer_id = consumer_id
            existing.handle = external_id
            return self._save(existing)
        row = self._insert_row(
            {
                "id": internal_id,
                "tier": ladder_tier,
                "handle": external_id,
                "consumer_id": consumer_id,
                "namespace_grants": grants,
            }
        )
        return self._from_row(row)

    def _get_required(self, subscriber_id: str) -> Subscriber:
        sub = self.get(subscriber_id)
        if not sub:
            raise KeyError(subscriber_id)
        return sub

    def _insert_row(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = {"id": str(uuid.uuid4()), **payload}
        res = self._client.post(f"{self._base}/subscribers", headers=self._headers, json=row)
        res.raise_for_status()
        rows = res.json()
        return rows[0] if isinstance(rows, list) else rows

    def _save(self, sub: Subscriber) -> Subscriber:
        body = {
            "tier": sub.tier,
            "handle": sub.handle,
            "email": sub.email,
            "consumer_id": sub.consumer_id,
            "verification": sub.verification.to_dict(),
            "namespace_grants": sub.namespace_grants,
        }
        res = self._client.patch(
            f"{self._base}/subscribers",
            params={"id": f"eq.{sub.id}"},
            headers=self._headers,
            json=body,
        )
        res.raise_for_status()
        rows = res.json()
        return self._from_row(rows[0] if rows else {**body, "id": sub.id, "created_at": sub.created_at.isoformat()})

    @staticmethod
    def _from_row(row: dict[str, Any]) -> Subscriber:
        verification_raw = row.get("verification") or {}
        created_raw = row.get("created_at")
        if isinstance(created_raw, str):
            created_at = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
        else:
            created_at = datetime.now(timezone.utc)
        return Subscriber(
            id=str(row["id"]),
            tier=row["tier"],
            handle=row.get("handle"),
            email=row.get("email"),
            consumer_id=row.get("consumer_id") or "somatune",
            verification=VerificationState(
                payment_status=verification_raw.get("payment_status", "none"),
                age_status=verification_raw.get("age_status", "none"),
                age_band=verification_raw.get("age_band", "unknown"),
                square_verification_ref=verification_raw.get("square_verification_ref"),
                attestation_at=verification_raw.get("attestation_at"),
            ),
            namespace_grants=dict(row.get("namespace_grants") or {}),
            created_at=created_at,
            freemium_policy=FreemiumPolicy(),
        )
