"""Entitlement merge and feature resolution for consumer namespaces."""

from __future__ import annotations

from typing import Any

from .consumer_mirror import load_dirt_tier_features
from .tiers import TIER_AGE_VERIFIED, TIER_CERTIFIED, TIER_GUEST, TIER_REGISTERED, tier_at_least
from .verification import VerificationState

DIRT_TIER_FEATURES: dict[str, dict[str, bool]] = load_dirt_tier_features()

SOMATUNE_PACK_MIN_TIER: dict[str, str] = {
    "intro": TIER_GUEST,
    "kids": TIER_REGISTERED,
    "somatic": TIER_REGISTERED,
    "x_rated": TIER_AGE_VERIFIED,
}

SOMATUNE_PAID_PRODUCT_TIERS: tuple[str, ...] = ("free", "plus", "couples", "studio")


def merge_grants(
    tier: str,
    namespace_grants: dict[str, list[str]],
    *,
    verification: VerificationState | None = None,
) -> dict[str, Any]:
    verification = verification or VerificationState()
    filtered: dict[str, list[str]] = {}
    for namespace, keys in namespace_grants.items():
        if namespace == "somatune.packs":
            filtered[namespace] = [
                k for k in keys if _pack_allowed(k, tier, verification)
            ]
        else:
            filtered[namespace] = list(keys)

    return {
        "tier": tier,
        "grants": filtered,
        "verification": verification.to_dict(),
        "features": _resolve_features(filtered),
        "paid_product_tiers": {
            "somatune": list(SOMATUNE_PAID_PRODUCT_TIERS),
            "dirt": ["content_creator", "advanced_content_creator"],
        },
    }


def _pack_allowed(pack_id: str, tier: str, verification: VerificationState) -> bool:
    required = SOMATUNE_PACK_MIN_TIER.get(pack_id, TIER_AGE_VERIFIED)
    if not tier_at_least(tier, required):
        return False
    if pack_id == "x_rated":
        return verification.allows_adult_gated_content()
    return True


def _resolve_features(grants: dict[str, list[str]]) -> dict[str, bool]:
    dirt_keys = grants.get("dirt.dashboard", [])
    if "advanced_content_creator" in dirt_keys:
        return dict(DIRT_TIER_FEATURES["advanced_content_creator"])
    if "content_creator" in dirt_keys:
        return dict(DIRT_TIER_FEATURES["content_creator"])
    return {}
