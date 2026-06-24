"""Ops portal — allowlisted Supabase PostgREST access (MSU-OPS-02)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx
from fastapi import HTTPException


def _cfg() -> dict[str, Any]:
    path = Path(__file__).resolve().parent.parent / "cfg" / "ops-supabase-tables.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _table_meta(name: str) -> dict[str, Any]:
    for t in _cfg().get("tables", []):
        if t["name"] == name:
            return t
    raise HTTPException(404, f"table not allowlisted: {name}")


def _client() -> httpx.Client:
    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key:
        raise HTTPException(503, "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not configured on ops host")
    return httpx.Client(
        base_url=f"{url}/rest/v1",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        },
        timeout=30.0,
    )


def list_tables() -> list[dict[str, Any]]:
    return [
        {
            "name": t["name"],
            "id_column": t["id_column"],
            "read_only": bool(t.get("read_only")),
            "max_list": t.get("max_list", 50),
        }
        for t in _cfg().get("tables", [])
    ]


def list_rows(table: str, *, limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    meta = _table_meta(table)
    cap = min(limit, int(meta.get("max_list", 50)))
    with _client() as client:
        res = client.get(
            f"/{table}",
            params={
                "select": "*",
                "order": f"{meta['id_column']}.desc",
                "limit": cap,
                "offset": offset,
            },
        )
        if res.status_code >= 400:
            raise HTTPException(res.status_code, res.text)
        return res.json()


def get_row(table: str, row_id: str) -> dict[str, Any]:
    meta = _table_meta(table)
    col = meta["id_column"]
    with _client() as client:
        res = client.get(f"/{table}", params={"select": "*", col: f"eq.{row_id}"})
        if res.status_code >= 400:
            raise HTTPException(res.status_code, res.text)
        rows = res.json()
        if not rows:
            raise HTTPException(404, "row not found")
        return rows[0]


def patch_row(table: str, row_id: str, patch: dict[str, Any]) -> dict[str, Any]:
    meta = _table_meta(table)
    if meta.get("read_only"):
        raise HTTPException(403, "table is read-only")
    allowed = set(meta.get("writable_columns", []))
    body = {k: v for k, v in patch.items() if k in allowed}
    if not body:
        raise HTTPException(400, "no writable fields in patch")
    col = meta["id_column"]
    with _client() as client:
        res = client.patch(f"/{table}?{col}=eq.{row_id}", json=body)
        if res.status_code >= 400:
            raise HTTPException(res.status_code, res.text)
        rows = res.json()
        return rows[0] if rows else {"ok": True}


def delete_row(table: str, row_id: str) -> dict[str, Any]:
    meta = _table_meta(table)
    if meta.get("read_only"):
        raise HTTPException(403, "table is read-only")
    col = meta["id_column"]
    with _client() as client:
        res = client.delete(f"/{table}?{col}=eq.{row_id}")
        if res.status_code >= 400:
            raise HTTPException(res.status_code, res.text)
        return {"deleted": row_id, "table": table}
