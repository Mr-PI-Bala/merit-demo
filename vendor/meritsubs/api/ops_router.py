"""Ops portal BFF routes (/api/admin/*)."""

from __future__ import annotations

import json
from pathlib import Path

from typing import Any

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from core import ops_auth, ops_probes, ops_square_probe, ops_supabase

router = APIRouter(prefix="/api/admin", tags=["ops-admin"])

_oauth_states: dict[str, str] = {}


class DevKeyLogin(BaseModel):
    admin_key: str = Field(min_length=8)


class SquareProbeRequest(BaseModel):
    mode: str = Field(pattern="^(sandbox|production)$")


class RefundRequest(BaseModel):
    registration_id: str


class WebhookReplayRequest(BaseModel):
    subscriber_id: str
    grants: dict[str, list[str]] = Field(default_factory=lambda: {"meritsubs.tier": ["certified"]})
    payment_id: str = "ops_replay"


class SupabasePatchRequest(BaseModel):
    patch: dict[str, Any] = Field(default_factory=dict)


def _set_session_cookie(response: Response, token: str) -> None:
    import os

    callback = os.environ.get("MERITSUBS_OPS_CALLBACK_URL", "http://127.0.0.1:8090/api/admin/auth/github/callback")
    secure = callback.startswith("https://")
    response.set_cookie(
        key=ops_auth.session_cookie_name(),
        value=token,
        httponly=True,
        secure=secure,
        samesite="lax",
        max_age=8 * 3600,
        path="/",
    )


@router.get("/auth/config")
def auth_config():
    cfg = ops_auth.load_operator_allowlist()
    return {
        "github_oauth": ops_auth.github_oauth_configured(),
        "allow_dev_key_login": ops_auth.allow_dev_key_login() and bool(
            __import__("os").environ.get("MERITSUBS_ADMIN_KEY")
        ),
        "operator_count": len(cfg.get("operators", [])),
    }


@router.get("/auth/github")
def auth_github_start():
    if not ops_auth.github_oauth_configured():
        raise HTTPException(503, "GitHub OAuth not configured")
    state = ops_auth.new_oauth_state()
    _oauth_states[state] = "pending"
    return RedirectResponse(ops_auth.github_authorize_url(state))


@router.get("/auth/github/callback")
async def auth_github_callback(code: str | None = None, state: str | None = None):
    if not code or not state or state not in _oauth_states:
        raise HTTPException(400, "invalid oauth state")
    del _oauth_states[state]
    user = await ops_auth.github_exchange_code(code)
    token = ops_auth.issue_session(
        subject=user["id"],
        email=user["email"],
        name=user["name"],
        via="github",
    )
    response = RedirectResponse(url="/admin/", status_code=302)
    _set_session_cookie(response, token)
    return response


@router.post("/auth/key")
def auth_dev_key(body: DevKeyLogin):
    if not ops_auth.allow_dev_key_login():
        raise HTTPException(403, "dev key login disabled")
    if not ops_auth.verify_dev_admin_key(body.admin_key):
        raise HTTPException(401, "invalid admin key")
    token = ops_auth.issue_session(
        subject="dev-key",
        email="dev-key@ops.local",
        name="Dev operator",
        via="admin_key",
    )
    response = Response(content=json.dumps({"ok": True}), media_type="application/json")
    _set_session_cookie(response, token)
    return response


@router.post("/auth/logout")
def auth_logout():
    response = Response(content=json.dumps({"ok": True}), media_type="application/json")
    response.delete_cookie(ops_auth.session_cookie_name(), path="/")
    return response


@router.get("/auth/me")
def auth_me(request: Request):
    return ops_auth.read_session(request)


@router.get("/health")
async def ops_health(request: Request):
    ops_auth.read_session(request)
    return await ops_square_probe.combined_health()


@router.post("/square/probe")
async def square_probe(body: SquareProbeRequest, request: Request):
    session = ops_auth.read_session(request)
    result = await ops_square_probe.run_square_probe(mode=body.mode)
    result["operator"] = session.get("email")
    return result


@router.post("/square/refund")
async def square_refund(body: RefundRequest, request: Request):
    ops_auth.read_session(request)
    try:
        detail = await ops_square_probe.refund_registration(body.registration_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(400, str(exc)) from exc
    return {"ok": True, "detail": detail}


@router.get("/audit-tail")
def ops_audit_tail(request: Request, limit: int = 30):
    """Proxy audit tail using server-held admin key."""
    ops_auth.read_session(request)
    import os

    import httpx

    from core.ops_config import consumer_api_base
    from core.ops_http import parse_json_response

    admin = os.environ.get("MERITSUBS_ADMIN_KEY", "")
    base = consumer_api_base()
    if not admin or not base:
        raise HTTPException(503, "admin proxy not configured")
    res = httpx.get(f"{base}/api/v1/admin/audit-tail", params={"limit": limit}, headers={"x-admin-key": admin}, timeout=20.0)
    if res.status_code >= 400:
        raise HTTPException(res.status_code, parse_json_response(res))
    return parse_json_response(res)


@router.get("/supabase/tables")
def supabase_tables(request: Request):
    ops_auth.read_session(request)
    return {"tables": ops_supabase.list_tables()}


@router.get("/supabase/{table}")
def supabase_list(table: str, request: Request, limit: int = 20, offset: int = 0):
    ops_auth.read_session(request)
    return {"rows": ops_supabase.list_rows(table, limit=limit, offset=offset)}


@router.get("/supabase/{table}/{row_id}")
def supabase_get(table: str, row_id: str, request: Request):
    ops_auth.read_session(request)
    return ops_supabase.get_row(table, row_id)


@router.patch("/supabase/{table}/{row_id}")
def supabase_patch(table: str, row_id: str, body: SupabasePatchRequest, request: Request):
    ops_auth.read_session(request)
    return ops_supabase.patch_row(table, row_id, body.patch)


@router.delete("/supabase/{table}/{row_id}")
def supabase_delete(table: str, row_id: str, request: Request, confirm: bool = False):
    ops_auth.read_session(request)
    if not confirm:
        raise HTTPException(400, "set confirm=true to delete")
    return ops_supabase.delete_row(table, row_id)


@router.get("/probes/cohort")
def probes_cohort(request: Request, consumer_id: str | None = None, limit: int = 20):
    ops_auth.read_session(request)
    return ops_probes.cohort_aggregates_probe(consumer_id=consumer_id, limit=limit)


@router.get("/probes/entitlements/{subscriber_id}")
def probes_entitlements(subscriber_id: str, request: Request):
    ops_auth.read_session(request)
    return ops_probes.subscriber_entitlements_probe(subscriber_id)


@router.post("/probes/webhook-replay")
async def probes_webhook_replay(body: WebhookReplayRequest, request: Request):
    session = ops_auth.read_session(request)
    result = await ops_probes.webhook_replay_probe(
        subscriber_id=body.subscriber_id,
        grants=body.grants,
        payment_id=body.payment_id,
    )
    result["operator"] = session.get("email")
    return result


def mount_admin_static(app) -> None:
    """Local dev: serve /admin static files."""
    admin_dir = Path(__file__).resolve().parent.parent / "admin"
    if admin_dir.is_dir():
        from fastapi.staticfiles import StaticFiles

        app.mount("/admin", StaticFiles(directory=str(admin_dir), html=True), name="admin-static")
