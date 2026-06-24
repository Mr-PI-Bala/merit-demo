"""meritsubs HTTP API (Phase 1A/1B)."""

from __future__ import annotations

import os
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jwt
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from core.audit_factory import create_audit_log
from core.cohort import CohortStore
from core.entitlements import merge_grants
from core.providers.revenuecat import RevenueCatProvider
from core.security import AuditEvent, FixedWindowRateLimiter
from core.store_factory import create_subscriber_store, store_backend_name
from core.tiers import TIER_GUEST, TIER_REGISTERED, validate_tier

from api.ops_router import mount_admin_static, router as ops_router

app = FastAPI(title="meritsubs", version="0.0.8")
app.include_router(ops_router)
_SERVICE_VERSION = app.version
_store = create_subscriber_store()
_JWT_SECRET = os.environ.get("MERITSUBS_JWT_SECRET", "dev-only-change-me-at-least-32-bytes")
_JWT_ALG = "HS256"
_MERITSTORE_URL = os.environ.get("MERITSTORE_BASE_URL", "http://localhost:3000")
_ADMIN_KEY = os.environ.get("MERITSUBS_ADMIN_KEY", "")
_rc_provider = RevenueCatProvider(webhook_secret=os.environ.get("REVENUECAT_WEBHOOK_SECRET", ""))
_rate_limiter = FixedWindowRateLimiter(limit=180, window_seconds=60)
_audit, _audit_backend = create_audit_log()
_cohort = CohortStore()

_SUBSCRIPTION_TERMS_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>MERIT Subscription Terms</title></head>
<body>
<h1>MERIT Subscription Terms</h1>
<p>These terms govern paid and free subscription tiers for MERIT consumer products
(SomaTune, AURAVYBE, DIRT) fulfilled via meritsubs identity and entitlement services.</p>
<ul>
<li>Paid tiers require verified payment (Square via meritstore) and applicable age attestation.</li>
<li>Age-gated content requires <code>age_verified</code> tier and <code>age_band=adult</code>.</li>
<li>Payment card data is processed by PCI-DSS-compliant processors; meritsubs does not store full PAN.</li>
</ul>
<p>Consumer product privacy and play policies remain on the product portal (e.g. SomaTune legal).</p>
<p><small>meritsubs provider · served in consumer context per MERIT §0.D.1</small></p>
</body></html>"""


def _audit_event(
    *,
    action: str,
    subscriber_id: str | None,
    consumer_id: str | None,
    result: str,
    detail: dict,
) -> None:
    _audit.append(
        AuditEvent(
            at=datetime.now(timezone.utc).isoformat(),
            action=action,
            subscriber_id=subscriber_id,
            consumer_id=consumer_id,
            result=result,
            detail=detail,
        )
    )


class GuestOnboard(BaseModel):
    handle: str = Field(min_length=2, max_length=32)
    consumer_id: str = "somatune"


class EmailOnboard(BaseModel):
    email: str
    consumer_id: str = "somatune"


class AgeAttest(BaseModel):
    date_of_birth: str
    age_band: str = Field(pattern="^(child|teen|adult)$")


class CertifiedComplete(BaseModel):
    square_verification_ref: str


class CheckoutRequest(BaseModel):
    plan: str = Field(pattern="^(certified-verify|plus-monthly|couples-monthly|studio-monthly)$")
    tenant: str = "meritsubs"


class CitationClickEvent(BaseModel):
    age_band: str | None = None
    region: str | None = None
    chronotype: str | None = None
    phenotype_ancestry: str | None = None
    link_type: str | None = None


class CitationClickBatch(BaseModel):
    consumer_id: str = Field(min_length=1)
    events: list[CitationClickEvent] = Field(min_length=1, max_length=500)


class SubscriberSyncRequest(BaseModel):
    action: str = Field(pattern="^(create|update|delete)$")
    subscriber: dict[str, Any]


def _require_sync_auth(authorization: str | None) -> None:
    api_key = os.environ.get("MERITSUBS_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(503, "sync not configured")
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "missing bearer token")
    if authorization.split(" ", 1)[1].strip() != api_key:
        raise HTTPException(401, "invalid bearer token")


def _issue_token(subscriber_id: str, tier: str, consumer_id: str) -> str:
    sub = _store.get(subscriber_id)
    if not sub:
        raise HTTPException(404, "subscriber not found")
    payload = merge_grants(tier, sub.namespace_grants, verification=sub.verification)
    claims = {
        "sub": subscriber_id,
        "tier": tier,
        "consumer": consumer_id,
        "grants": payload["grants"],
        "verification": payload["verification"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(claims, _JWT_SECRET, algorithm=_JWT_ALG)


def _subscriber_from_auth(authorization: str | None) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        data = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALG])
    except jwt.PyJWTError as exc:
        raise HTTPException(401, "invalid token") from exc
    return str(data["sub"])


def _require_admin(x_admin_key: str | None) -> None:
    if not _ADMIN_KEY:
        raise HTTPException(503, "admin key not configured")
    if x_admin_key != _ADMIN_KEY:
        raise HTTPException(401, "invalid admin key")


def _enforce_rate_limit(request: Request) -> None:
    key = request.client.host if request.client else "unknown"
    if not _rate_limiter.allow(key):
        raise HTTPException(429, "rate limit exceeded")


def _service_mode() -> str:
    explicit = os.environ.get("MERITSUBS_MODE", "").strip().lower()
    if explicit in ("production", "prod"):
        return "production"
    if explicit in ("alpha", "dev", "development"):
        return "alpha"
    if os.environ.get("MERITSUBS_JWT_SECRET") and os.environ.get("MERITSUBS_ADMIN_KEY"):
        return "production"
    return "alpha"


@app.get("/api/v1/health")
def health():
    return {
        "ok": True,
        "service": "meritsubs",
        "mode": _service_mode(),
        "version": _SERVICE_VERSION,
        "store": store_backend_name(),
        "audit": _audit_backend,
        "supabase": store_backend_name() == "supabase",
        "consumer_context": True,
    }


@app.get("/legal/terms", response_class=HTMLResponse)
@app.get("/api/v1/legal/terms")
def subscription_terms():
    """Published subscription terms (STN-MSU-01) — serve on consumer host per §0.D.1."""
    return HTMLResponse(_SUBSCRIPTION_TERMS_HTML)


@app.post("/api/v1/analytics/citation-clicks")
def citation_clicks_ingest(
    body: CitationClickBatch,
    request: Request,
    x_consumer_secret: str | None = Header(default=None),
):
    """De-identified cohort ingest from consumer Supabase emitters (STN-MSU-03)."""
    _enforce_rate_limit(request)
    expected = os.environ.get(f"MERITSUBS_CONSUMER_SECRET_{body.consumer_id.upper()}", "")
    if expected and x_consumer_secret != expected:
        raise HTTPException(401, "invalid consumer secret")
    result = _cohort.ingest(
        consumer_id=body.consumer_id,
        events=[e.model_dump(exclude_none=True) for e in body.events],
    )
    _audit_event(
        action="cohort_ingest",
        subscriber_id=None,
        consumer_id=body.consumer_id,
        result="ok",
        detail={"accepted": result.accepted, "aggregate_key": result.aggregate_key},
    )
    return {"ok": True, "accepted": result.accepted, "aggregate_key": result.aggregate_key}


@app.get("/api/v1/admin/cohort-aggregates")
def cohort_aggregates(
    consumer_id: str | None = None,
    limit: int = 20,
    x_admin_key: str | None = Header(default=None),
):
    _require_admin(x_admin_key)
    return {"aggregates": _cohort.aggregates(consumer_id=consumer_id, limit=limit)}


@app.get("/api/v1/showcase")
def showcase():
    return {
        "launchpad": "portal/index.html",
        "integrations": {
            "somatune": {
                "entitlements_api": "/api/v1/entitlements",
                "room_gate": "use /api/v1/entitlements + seat token validation in SomaTune",
            },
            "auravybe": {
                "commerce": "meritstore tenant meritsubs",
                "payment_provider": "square",
            },
            "dirt": {
                "tier_namespace": "dirt.dashboard",
                "provider": "revenuecat webhook + meritsubs grants",
            },
            "meritstore": {
                "webhook": "/api/v1/webhooks/meritstore",
                "checkout_handoff": "/api/v1/subscribers/{subscriber_id}/checkout/meritstore",
            },
        },
    }


@app.post("/api/v1/subscribers/onboard/guest")
def onboard_guest(body: GuestOnboard, request: Request):
    _enforce_rate_limit(request)
    sub = _store.onboard_guest(handle=body.handle, consumer_id=body.consumer_id)
    token = _issue_token(sub.id, TIER_GUEST, body.consumer_id)
    _audit_event(
        action="onboard_guest",
        subscriber_id=sub.id,
        consumer_id=body.consumer_id,
        result="ok",
        detail={"tier": TIER_GUEST},
    )
    return {"subscriber": sub.to_dict(), "token": token}


@app.post("/api/v1/subscribers/onboard/email")
def onboard_email(body: EmailOnboard, request: Request):
    _enforce_rate_limit(request)
    sub = _store.onboard_registered(email=body.email, consumer_id=body.consumer_id)
    token = _issue_token(sub.id, TIER_REGISTERED, body.consumer_id)
    _audit_event(
        action="onboard_registered",
        subscriber_id=sub.id,
        consumer_id=body.consumer_id,
        result="ok",
        detail={"tier": TIER_REGISTERED},
    )
    return {"subscriber": sub.to_dict(), "token": token, "magic_link": "stub://verify-email"}


@app.get("/api/v1/entitlements")
def entitlements(authorization: str | None = Header(default=None), request: Request = None):
    if request:
        _enforce_rate_limit(request)
    sid = _subscriber_from_auth(authorization)
    sub = _store.get(sid)
    if not sub:
        raise HTTPException(404, "subscriber not found")
    payload = merge_grants(sub.tier, sub.namespace_grants, verification=sub.verification)
    return {"subscriber_id": sid, **payload}


@app.post("/api/subscribers/sync")
def subscribers_sync(
    body: SubscriberSyncRequest,
    authorization: str | None = Header(default=None),
):
    """DIRT admin CRUD mirror (MSU-DRT-04) — stable contract for MeritSubsProvider.sync."""
    _require_sync_auth(authorization)
    try:
        sub = _store.sync_consumer_mirror(action=body.action, subscriber=body.subscriber)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    external_id = str(body.subscriber.get("subscriber_id") or "").strip()
    if body.action == "delete":
        return {"subscriber_id": external_id, "status": "ok", "action": body.action}
    if not sub:
        raise HTTPException(500, "sync failed")
    return {
        "subscriber_id": external_id,
        "status": "ok",
        "action": body.action,
        "subscriber": sub.to_dict(),
    }


@app.post("/api/v1/subscribers/{subscriber_id}/certified/complete")
def certified_complete(
    subscriber_id: str,
    body: CertifiedComplete,
    authorization: str | None = Header(default=None),
):
    if _subscriber_from_auth(authorization) != subscriber_id:
        raise HTTPException(403, "token mismatch")
    sub = _store.mark_certified(subscriber_id, square_ref=body.square_verification_ref)
    token = _issue_token(sub.id, sub.tier, sub.consumer_id)
    _audit_event(
        action="certified_complete",
        subscriber_id=subscriber_id,
        consumer_id=sub.consumer_id,
        result="ok",
        detail={"square_ref": body.square_verification_ref},
    )
    return {"subscriber": sub.to_dict(), "token": token}


@app.post("/api/v1/subscribers/{subscriber_id}/age/attest")
def age_attest(subscriber_id: str, body: AgeAttest, authorization: str | None = Header(default=None)):
    if _subscriber_from_auth(authorization) != subscriber_id:
        raise HTTPException(403, "token mismatch")
    try:
        sub = _store.attest_age(subscriber_id, date_of_birth_iso=body.date_of_birth, age_band=body.age_band)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    token = _issue_token(sub.id, sub.tier, sub.consumer_id)
    _audit_event(
        action="age_attest",
        subscriber_id=subscriber_id,
        consumer_id=sub.consumer_id,
        result="ok",
        detail={"age_band": body.age_band},
    )
    return {"subscriber": sub.to_dict(), "token": token}


@app.post("/api/v1/subscribers/{subscriber_id}/checkout/meritstore")
def meritstore_checkout_url(
    subscriber_id: str,
    body: CheckoutRequest,
    authorization: str | None = Header(default=None),
):
    """Hand off to meritstore Square checkout (certified-verify or paid SKUs)."""
    if _subscriber_from_auth(authorization) != subscriber_id:
        raise HTTPException(403, "token mismatch")
    sub = _store.get(subscriber_id)
    if not sub:
        raise HTTPException(404, "subscriber not found")
    tier = validate_tier(sub.tier)
    if body.plan == "certified-verify":
        if tier not in ("registered", "certified", "age_verified"):
            raise HTTPException(400, "registered tier required for certified-verify")
    elif tier not in ("certified", "age_verified"):
        raise HTTPException(400, "certified tier required for paid checkout")
    url = (
        f"{_MERITSTORE_URL}/{body.tenant}/register?"
        f"subscriber_id={subscriber_id}&plan={body.plan}&email={sub.email or ''}"
    )
    _audit_event(
        action="checkout_meritstore",
        subscriber_id=subscriber_id,
        consumer_id=sub.consumer_id,
        result="ok",
        detail={"plan": body.plan, "tenant": body.tenant},
    )
    return {"checkout_url": url, "tenant": body.tenant, "plan": body.plan}


@app.post("/api/v1/webhooks/meritstore")
def meritstore_webhook(payload: dict, x_meritstore_secret: str | None = Header(default=None)):
    expected = os.environ.get("MERITSTORE_WEBHOOK_SECRET", "")
    if expected and x_meritstore_secret != expected:
        raise HTTPException(401, "invalid webhook secret")
    subscriber_id = payload.get("subscriber_id")
    grants = payload.get("grants") or {}
    if not subscriber_id:
        raise HTTPException(400, "subscriber_id required")
    sub = _store.get(str(subscriber_id))
    if not sub:
        raise HTTPException(404, "subscriber not found")
    for namespace, keys in grants.items():
        if isinstance(keys, list):
            _store.add_grants(subscriber_id, namespace, [str(k) for k in keys])
            if namespace == "meritsubs.tier" and "certified" in keys:
                _store.mark_certified(subscriber_id, square_ref=payload.get("payment_id", "meritstore"))
    _audit_event(
        action="webhook_meritstore",
        subscriber_id=str(subscriber_id),
        consumer_id=sub.consumer_id,
        result="ok",
        detail={"grants": grants},
    )
    return {"ok": True, "subscriber": _store.get(subscriber_id).to_dict()}


@app.post("/api/v1/webhooks/revenuecat")
def revenuecat_webhook(payload: dict, authorization: str | None = Header(default=None)):
    if not _rc_provider.verify_webhook(authorization):
        raise HTTPException(401, "invalid revenuecat authorization")
    subscriber_id = (
        payload.get("event", {}).get("subscriber_attributes", {}).get("meritsubs_id", {}).get("value")
    )
    if not subscriber_id:
        raise HTTPException(400, "missing meritsubs_id attribute")
    sub = _store.get(str(subscriber_id))
    if not sub:
        raise HTTPException(404, "subscriber not found")
    mapped = _rc_provider.map_entitlement(payload)
    for namespace, keys in mapped.get("grants", {}).items():
        _store.add_grants(sub.id, namespace, list(keys))
    if mapped.get("tier") == "certified":
        _store.mark_certified(sub.id, square_ref="revenuecat")
    _audit_event(
        action="webhook_revenuecat",
        subscriber_id=sub.id,
        consumer_id=sub.consumer_id,
        result="ok",
        detail={"entitlement_ids": mapped.get("entitlement_ids", [])},
    )
    return {"ok": True, "subscriber": _store.get(sub.id).to_dict()}


@app.get("/api/v1/admin/audit-tail")
def audit_tail(limit: int = 20, x_admin_key: str | None = Header(default=None)):
    _require_admin(x_admin_key)
    if _audit_backend == "supabase" and hasattr(_audit, "tail"):
        return {"events": _audit.tail(limit=limit)}
    path = Path("output/audit/events.jsonl")
    if not path.exists():
        return {"events": []}
    lines = path.read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) if line.strip() else {} for line in lines[-limit:]]
    return {"events": events}


def _wrap_mount_prefix(asgi_app):
    """Strip MERITSUBS_MOUNT_PREFIX when embedded under consumer host (e.g. /api/meritsubs)."""
    prefix = os.environ.get("MERITSUBS_MOUNT_PREFIX", "").rstrip("/")
    if not prefix:
        return asgi_app

    async def mounted(scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith(prefix):
            scope = dict(scope)
            scope["path"] = scope["path"][len(prefix) :] or "/"
        await asgi_app(scope, receive, send)

    return mounted


mount_admin_static(app)
app = _wrap_mount_prefix(app)  # noqa: F811 — ASGI export for Vercel; use _SERVICE_VERSION not app.version below
