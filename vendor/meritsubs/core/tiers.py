"""MERIT subscriber tier ladder — SSOT for trust levels."""

from __future__ import annotations

from typing import Final

TIER_GUEST: Final = "guest"
TIER_REGISTERED: Final = "registered"
TIER_CERTIFIED: Final = "certified"
TIER_AGE_VERIFIED: Final = "age_verified"

# Base trust ladder — paid product tiers are consumer namespaces, not ladder steps.
TIER_LADDER: tuple[str, ...] = (
    TIER_GUEST,
    TIER_REGISTERED,
    TIER_CERTIFIED,
    TIER_AGE_VERIFIED,
)

TIER_METADATA: dict[str, dict[str, object]] = {
    TIER_GUEST: {
        "label": "Guest",
        "requires_email": False,
        "requires_handle": True,
        "payment_verification_required": False,
        "age_verification_required": False,
        "stores_pii": False,
        "description": "Handle-only trial tier; no registration or PII.",
    },
    TIER_REGISTERED: {
        "label": "Registered",
        "requires_email": True,
        "requires_handle": False,
        "payment_verification_required": False,
        "age_verification_required": False,
        "stores_pii": True,
        "pii_fields": ("email",),
        "description": "Email-verified free tier; no payment or age gate.",
    },
    TIER_CERTIFIED: {
        "label": "Certified",
        "requires_email": True,
        "requires_handle": False,
        "payment_verification_required": True,
        "age_verification_required": False,
        "stores_pii": True,
        "pii_fields": ("email",),
        "description": "Square payment-instrument verified; does NOT prove age.",
    },
    TIER_AGE_VERIFIED: {
        "label": "Age Verified",
        "requires_email": True,
        "requires_handle": False,
        "payment_verification_required": True,
        "age_verification_required": True,
        "stores_pii": True,
        "pii_fields": ("email", "date_of_birth_attestation"),
        "description": "DOB attestation (+ certified payment); required for adult-gated content.",
    },
}

# Legacy aliases — reject at API boundary; map only in migration helpers.
LEGACY_TIER_ALIASES: dict[str, str] = {
    "ghost": TIER_GUEST,
    "free_registered": TIER_REGISTERED,
}


def normalize_tier(tier: str) -> str:
    """Map legacy tier ids to current SSOT names."""
    tier = (tier or "").strip()
    return LEGACY_TIER_ALIASES.get(tier, tier)


def tier_rank(tier: str) -> int:
    tier = normalize_tier(tier)
    try:
        return TIER_LADDER.index(tier)
    except ValueError:
        return -1


def tier_at_least(current: str, required: str) -> bool:
    return tier_rank(current) >= tier_rank(required)


def validate_tier(tier: str) -> str:
    tier = normalize_tier(tier)
    if tier not in TIER_METADATA:
        raise ValueError(f"Unknown tier: {tier}")
    return tier
