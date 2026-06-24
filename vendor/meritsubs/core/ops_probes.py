"""Ops capability probes — entitlements, webhook replay, cohort (MSU-OPS-02)."""

from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import HTTPException

from core.entitlements import merge_grants
from core.tiers import validate_tier
from core.verification import VerificationState


from core.ops_config import consumer_api_base
from core.ops_http import parse_json_response


def _msu_base() -> str:
    return consumer_api_base()


def subscriber_entitlements_probe(subscriber_id: str) -> dict[str, Any]:
    from core.ops_supabase import get_row

    try:
        row = get_row("subscribers", subscriber_id)
    except HTTPException as exc:
        if exc.status_code == 404:
            raise HTTPException(404, "subscriber not found in Supabase") from exc
        raise
    tier = validate_tier(row.get("tier", "guest"))
    grants = row.get("namespace_grants") or {}
    vraw = row.get("verification") or {}
    verification = VerificationState(
        payment_status=vraw.get("payment_status", "none"),
        age_status=vraw.get("age_status", "none"),
        age_band=vraw.get("age_band", "unknown"),
        square_verification_ref=vraw.get("square_verification_ref"),
        attestation_at=vraw.get("attestation_at"),
    )
    payload = merge_grants(tier, grants, verification=verification)
    return {
        "subscriber_id": subscriber_id,
        "row": row,
        **payload,
    }


async def webhook_replay_probe(
    *,
    subscriber_id: str,
    grants: dict[str, list[str]],
    payment_id: str = "ops_replay",
) -> dict[str, Any]:
    secret = os.environ.get("MERITSTORE_WEBHOOK_SECRET", "")
    base = _msu_base()
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(
            f"{base}/api/v1/webhooks/meritstore",
            headers={"x-meritstore-secret": secret} if secret else {},
            json={"subscriber_id": subscriber_id, "grants": grants, "payment_id": payment_id},
        )
        if res.status_code >= 400:
            raise HTTPException(res.status_code, res.text)
        return {"status": res.status_code, "body": parse_json_response(res)}


def cohort_aggregates_probe(*, consumer_id: str | None = None, limit: int = 20) -> dict[str, Any]:
    admin = os.environ.get("MERITSUBS_ADMIN_KEY", "")
    base = _msu_base()
    if not admin:
        raise HTTPException(503, "MERITSUBS_ADMIN_KEY not configured")
    params: dict[str, Any] = {"limit": limit}
    if consumer_id:
        params["consumer_id"] = consumer_id
    res = httpx.get(
        f"{base}/api/v1/admin/cohort-aggregates",
        params=params,
        headers={"x-admin-key": admin},
        timeout=20.0,
    )
    if res.status_code >= 400:
        raise HTTPException(res.status_code, parse_json_response(res))
    return parse_json_response(res)
