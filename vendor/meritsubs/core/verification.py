"""Payment vs age verification — Square certifies payment, not age."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PaymentStatus = Literal["none", "pending", "verified", "failed"]
AgeStatus = Literal["none", "self_attested", "verified_adult", "verified_minor", "failed"]
AgeBand = Literal["unknown", "child", "teen", "adult"]


@dataclass
class VerificationState:
  payment_status: PaymentStatus = "none"
  age_status: AgeStatus = "none"
  age_band: AgeBand = "unknown"
  square_verification_ref: str | None = None
  attestation_at: str | None = None

  def allows_adult_gated_content(self) -> bool:
    return (
      self.payment_status == "verified"
      and self.age_status in ("verified_adult", "self_attested")
      and self.age_band == "adult"
    )

  def to_dict(self) -> dict[str, str | None]:
    return {
      "payment_status": self.payment_status,
      "age_status": self.age_status,
      "age_band": self.age_band,
      "square_verification_ref": self.square_verification_ref,
      "attestation_at": self.attestation_at,
    }


def tier_from_verification(state: VerificationState) -> str:
  """Derive ladder tier from verification axes."""
  from .tiers import TIER_AGE_VERIFIED, TIER_CERTIFIED, TIER_GUEST, TIER_REGISTERED

  if state.allows_adult_gated_content() or state.age_status in (
    "verified_adult",
    "verified_minor",
    "self_attested",
  ):
    if state.payment_status == "verified":
      return TIER_AGE_VERIFIED
  if state.payment_status == "verified":
    return TIER_CERTIFIED
  return TIER_REGISTERED if state.age_status != "none" else TIER_GUEST
