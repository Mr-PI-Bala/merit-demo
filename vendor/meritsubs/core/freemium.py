"""Freemium trial windows and IAR anomaly flags."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass(frozen=True)
class FreemiumPolicy:
  guest_max_days: int = 3
  registered_required_after_days: int = 7
  certified_required_after_days: int = 14
  allow_guest_forever: bool = False
  allow_registered_forever: bool = False

  def anomalies(self) -> list[dict[str, Any]]:
    """Flag configs that need AgentDraven review (IAR anomaly table)."""
    flags: list[dict[str, Any]] = []
    if self.guest_max_days > 3 and self.registered_required_after_days > 7:
      flags.append(
        {
          "code": "FREEMIUM_TRIAL_EXTENDED",
          "severity": "review",
          "detail": (
            f"guest_max_days={self.guest_max_days}>3 AND "
            f"registered_required_after_days={self.registered_required_after_days}>7"
          ),
        }
      )
    if self.certified_required_after_days > 14 and not (
      self.allow_guest_forever or self.allow_registered_forever
    ):
      flags.append(
        {
          "code": "CERTIFIED_DEADLINE_EXTENDED",
          "severity": "info",
          "detail": f"certified_required_after_days={self.certified_required_after_days}>14",
        }
      )
    return flags


def required_tier_by_age(
  *,
  created_at: datetime,
  current_tier: str,
  policy: FreemiumPolicy,
  now: datetime | None = None,
) -> tuple[str | None, str | None]:
  """
  Return (required_tier, reason) when subscriber must upgrade; else (None, None).
  """
  from .tiers import TIER_CERTIFIED, TIER_GUEST, TIER_REGISTERED, tier_rank

  now = now or datetime.now(timezone.utc)
  if created_at.tzinfo is None:
    created_at = created_at.replace(tzinfo=timezone.utc)
  age_days = (now - created_at).days

  if policy.allow_guest_forever and policy.allow_registered_forever:
    return None, None

  if tier_rank(current_tier) < tier_rank(TIER_REGISTERED):
    if not policy.allow_guest_forever and age_days >= policy.registered_required_after_days:
      return TIER_REGISTERED, f"guest trial exceeded {policy.registered_required_after_days}d"
    if age_days >= policy.guest_max_days and not policy.allow_guest_forever:
      return TIER_REGISTERED, f"guest window exceeded {policy.guest_max_days}d"

  if tier_rank(current_tier) < tier_rank(TIER_CERTIFIED):
    if not policy.allow_registered_forever and age_days >= policy.certified_required_after_days:
      return TIER_CERTIFIED, f"certified required after {policy.certified_required_after_days}d"

  return None, None
