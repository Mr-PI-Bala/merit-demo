"""Ops portal session auth (MSU-OPS-01)."""

from __future__ import annotations

import json
import os
import secrets
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import httpx
import jwt
from fastapi import HTTPException, Request

_OPS_AUD = "msu-ops-portal"
_COOKIE = "msu_admin_session"
_SESSION_HOURS = 8


def _ops_secret() -> str:
    return os.environ.get("MERITSUBS_OPS_JWT_SECRET") or os.environ.get("MERITSUBS_ADMIN_KEY", "")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_operator_allowlist() -> dict[str, Any]:
    path = _repo_root() / "cfg" / "admin-operators.json"
    if not path.exists():
        return {"operators": [], "allow_dev_key_login": True}
    return json.loads(path.read_text(encoding="utf-8"))


def _allowed_emails() -> set[str]:
    cfg = load_operator_allowlist()
    return {str(o.get("email", "")).lower() for o in cfg.get("operators", []) if o.get("email")}


def allow_dev_key_login() -> bool:
    return bool(load_operator_allowlist().get("allow_dev_key_login", False))


def session_cookie_name() -> str:
    return _COOKIE


def issue_session(*, subject: str, email: str, name: str, via: str) -> str:
    secret = _ops_secret()
    if not secret:
        raise HTTPException(503, "ops session secret not configured")
    now = int(time.time())
    payload = {
        "sub": subject,
        "email": email,
        "name": name,
        "via": via,
        "aud": _OPS_AUD,
        "iat": now,
        "exp": now + _SESSION_HOURS * 3600,
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def read_session(request: Request) -> dict[str, Any]:
    token = request.cookies.get(_COOKIE)
    if not token:
        raise HTTPException(401, "not authenticated")
    secret = _ops_secret()
    if not secret:
        raise HTTPException(503, "ops session secret not configured")
    try:
        data = jwt.decode(token, secret, algorithms=["HS256"], audience=_OPS_AUD)
    except jwt.PyJWTError as exc:
        raise HTTPException(401, "invalid session") from exc
    return data


def github_oauth_configured() -> bool:
    return bool(
        os.environ.get("MERITSUBS_GITHUB_CLIENT_ID")
        and os.environ.get("MERITSUBS_GITHUB_CLIENT_SECRET")
    )


def github_authorize_url(state: str) -> str:
    client_id = os.environ.get("MERITSUBS_GITHUB_CLIENT_ID", "")
    redirect = os.environ.get(
        "MERITSUBS_OPS_CALLBACK_URL",
        "http://127.0.0.1:8090/api/admin/auth/github/callback",
    )
    params = {
        "client_id": client_id,
        "redirect_uri": redirect,
        "scope": "read:user user:email",
        "state": state,
    }
    return f"https://github.com/login/oauth/authorize?{urlencode(params)}"


async def github_exchange_code(code: str) -> dict[str, Any]:
    redirect = os.environ.get(
        "MERITSUBS_OPS_CALLBACK_URL",
        "http://127.0.0.1:8090/api/admin/auth/github/callback",
    )
    async with httpx.AsyncClient(timeout=30.0) as client:
        token_res = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": os.environ.get("MERITSUBS_GITHUB_CLIENT_ID"),
                "client_secret": os.environ.get("MERITSUBS_GITHUB_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": redirect,
            },
        )
        token_res.raise_for_status()
        access = token_res.json().get("access_token")
        if not access:
            raise HTTPException(400, "github token exchange failed")
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access}", "Accept": "application/vnd.github+json"},
        )
        user_res.raise_for_status()
        user = user_res.json()
        email = user.get("email")
        if not email:
            emails_res = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access}", "Accept": "application/vnd.github+json"},
            )
            emails_res.raise_for_status()
            for row in emails_res.json():
                if row.get("primary") and row.get("verified"):
                    email = row.get("email")
                    break
        if not email:
            raise HTTPException(403, "github account has no verified email")
        email_l = email.lower()
        if email_l not in _allowed_emails():
            raise HTTPException(403, "email not in admin allowlist")
        return {
            "id": str(user.get("id")),
            "email": email,
            "name": user.get("name") or user.get("login") or email,
        }


def new_oauth_state() -> str:
    return secrets.token_urlsafe(24)


def verify_dev_admin_key(key: str) -> bool:
    expected = os.environ.get("MERITSUBS_ADMIN_KEY", "")
    return bool(expected) and secrets.compare_digest(key, expected)
