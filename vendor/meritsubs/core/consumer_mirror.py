"""Consumer admin CRUD mirror helpers (DIRT subscriber_identity lane)."""

from __future__ import annotations

import json
import uuid
from functools import lru_cache
from pathlib import Path
from typing import Any

TIER_MATRIX_PATH = Path(__file__).resolve().parents[1] / "cfg" / "tier-matrix.json"

DIRT_PRODUCT_TIERS: tuple[str, ...] = ("content_creator", "advanced_content_creator")
DIRT_CONSUMER_ID = "dirt"
DIRT_NAMESPACE = "dirt.dashboard"


@lru_cache(maxsize=1)
def _tier_matrix() -> dict[str, Any]:
    return json.loads(TIER_MATRIX_PATH.read_text(encoding="utf-8"))


def dirt_product_to_ladder(product_tier: str) -> str:
    mapping = _tier_matrix()["consumer_mappings"]["dirt"]["product_to_ladder"]
    return str(mapping.get(product_tier, "registered"))


def dirt_namespace_grants(product_tier: str) -> dict[str, list[str]]:
    return {DIRT_NAMESPACE: [product_tier]}


def dirt_mirror_uuid(external_id: str) -> str:
    """Deterministic internal id for DIRT registry subscriber_id strings."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"dirt.mirror.{external_id.strip()}"))


def load_dirt_tier_features() -> dict[str, dict[str, bool]]:
    return dict(_tier_matrix()["consumer_mappings"]["dirt"]["tier_features"])


def validate_dirt_sync_payload(action: str, subscriber: dict[str, Any]) -> tuple[str, str]:
    if action not in ("create", "update", "delete"):
        raise ValueError(f"unknown action: {action}")
    sid = str(subscriber.get("subscriber_id") or "").strip()
    if not sid:
        raise ValueError("subscriber_id required")
    tier = str(subscriber.get("tier") or "content_creator").strip()
    if action != "delete" and tier not in DIRT_PRODUCT_TIERS:
        raise ValueError(f"unknown tier: {tier}")
    return sid, tier
