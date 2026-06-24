"""Ops portal env resolution (consumer API SSOT + Supabase)."""

from __future__ import annotations

import os

CONSUMER_API_SSOT = "https://somatune.vercel.app/api/meritsubs"


def consumer_api_base() -> str:
    """Subscriber API lives on consumer host — never meritsubs.vercel.app (ops-only)."""
    for key in ("MERITSUBS_PUBLIC_BASE_URL", "MERITSUBS_BASE_URL"):
        raw = os.environ.get(key, "").strip().rstrip("/")
        if not raw:
            continue
        if "meritsubs.vercel.app" in raw and "/api/meritsubs" not in raw:
            continue
        return raw
    return CONSUMER_API_SSOT


def consumer_health_url() -> str:
    base = consumer_api_base()
    return f"{base}/api/v1/health"


def supabase_configured() -> bool:
    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))
