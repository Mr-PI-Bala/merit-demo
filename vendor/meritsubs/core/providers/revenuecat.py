"""RevenueCat adapter — ported from dirt/core/subscribers/providers/revenuecat.py."""

from __future__ import annotations

import hmac


class RevenueCatProvider:
    """Webhook verification and entitlement mapping for native mobile subscriptions."""

    name = "revenuecat"

    def __init__(self, webhook_secret: str | None = None):
        self.webhook_secret = webhook_secret or ""

    def verify_webhook(self, authorization_header: str | None) -> bool:
        if not self.webhook_secret:
            return False
        token = (authorization_header or "").removeprefix("Bearer ").strip()
        return hmac.compare_digest(token, self.webhook_secret)

    def map_entitlement(self, revenuecat_payload: dict) -> dict:
        """Map RC event to meritsubs grant keys per consumer namespace."""
        entitlement_ids = _extract_entitlement_ids(revenuecat_payload)
        grants: dict[str, list[str]] = {"dirt.dashboard": []}

        if "advanced_content_creator" in entitlement_ids:
            grants["dirt.dashboard"] = ["advanced_content_creator"]
        elif "content_creator" in entitlement_ids:
            grants["dirt.dashboard"] = ["content_creator"]

        # SomaTune paid tiers via RC product identifiers (extend in Phase 2B)
        somatune_packs = [e for e in entitlement_ids if e.startswith("somatune.")]
        if somatune_packs:
            grants["somatune.packs"] = [p.removeprefix("somatune.") for p in somatune_packs]

        tier = "certified" if entitlement_ids else "registered"
        return {
            "provider": self.name,
            "tier": tier,
            "grants": grants,
            "entitlement_ids": sorted(entitlement_ids),
        }


def _extract_entitlement_ids(payload: dict) -> set[str]:
    event = payload.get("event", {}) if isinstance(payload, dict) else {}
    entitlements = event.get("entitlements", {}) if isinstance(event, dict) else {}
    ids = set(entitlements.keys()) if isinstance(entitlements, dict) else set()
    subscriber_attributes = event.get("subscriber_attributes", {}) if isinstance(event, dict) else {}
    for attr_key in ("dirt_tier", "somatune_tier"):
        attr = subscriber_attributes.get(attr_key, {}) if isinstance(subscriber_attributes, dict) else {}
        value = attr.get("value") if isinstance(attr, dict) else None
        if value:
            ids.add(str(value))
    return ids
