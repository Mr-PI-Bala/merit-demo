"""Shared HTTP helpers for ops BFF."""

from __future__ import annotations

from typing import Any

import httpx


def parse_json_response(res: httpx.Response) -> Any:
    text = (res.text or "").strip()
    if not text:
        return {
            "error": "empty response body",
            "status": res.status_code,
            "url": str(res.url),
            "hint": "Check MERITSUBS_PUBLIC_BASE_URL points to somatune.vercel.app/api/meritsubs not meritsubs.vercel.app",
        }
    try:
        return res.json()
    except ValueError:
        return {
            "error": "non-json response",
            "status": res.status_code,
            "url": str(res.url),
            "body_preview": text[:240],
            "hint": "Consumer API must be https://somatune.vercel.app/api/meritsubs",
        }
