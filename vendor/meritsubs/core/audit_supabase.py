"""Append-only audit log via Supabase (Vercel-safe)."""

from __future__ import annotations

from dataclasses import asdict

import httpx

from .security import AuditEvent


class SupabaseAuditLog:
    def __init__(self, url: str, service_role_key: str, *, timeout: float = 20.0):
        self._url = url.rstrip("/") + "/rest/v1/audit_events"
        self._headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
        self._client = httpx.Client(timeout=timeout)

    def append(self, event: AuditEvent) -> None:
        payload = asdict(event)
        if payload.get("subscriber_id") is None:
            payload.pop("subscriber_id", None)
        res = self._client.post(self._url, headers=self._headers, json=payload)
        res.raise_for_status()

    def tail(self, limit: int = 20) -> list[dict]:
        res = self._client.get(
            self._url,
            params={"select": "*", "order": "at.desc", "limit": str(limit)},
            headers=self._headers,
        )
        res.raise_for_status()
        return list(res.json())
