"""Square E2E probe orchestration (meritstore + meritsubs consumer API)."""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import httpx

from core.ops_config import consumer_api_base, consumer_health_url

_TENANT = "meritsubs"
_OFFERING = "certified-verify"
_PROMO = "ONLY5CENT"


from core.ops_http import parse_json_response


def _msu_base() -> str:
    return consumer_api_base()


def _mst_base() -> str:
    return os.environ.get("MERITSTORE_BASE_URL", "http://localhost:3000").rstrip("/")


def _mst_admin() -> str:
    return os.environ.get("MERITSTORE_ADMIN_KEY", "")


def _webhook_secret() -> str:
    return os.environ.get("MERITSTORE_WEBHOOK_SECRET", "")


def _step(step_id: str, ok: bool, detail: Any) -> dict[str, Any]:
    return {"id": step_id, "ok": ok, "detail": detail}


async def combined_health() -> dict[str, Any]:
    out: dict[str, Any] = {"meritsubs": None, "meritstore": None}
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            msu = await client.get(consumer_health_url())
            body = parse_json_response(msu)
            ok = msu.status_code == 200 and isinstance(body, dict) and body.get("ok")
            out["meritsubs"] = {"ok": ok, "status": msu.status_code, "url": consumer_health_url(), "body": body}
        except Exception as exc:  # noqa: BLE001
            out["meritsubs"] = {"ok": False, "url": consumer_health_url(), "error": str(exc)}
        try:
            mst = await client.get(f"{_mst_base()}/api/v1/health")
            out["meritstore"] = {"ok": mst.status_code == 200, "status": mst.status_code, "body": mst.json()}
        except Exception as exc:  # noqa: BLE001
            out["meritstore"] = {"ok": False, "error": str(exc)}
    out["ok"] = bool(out.get("meritsubs", {}).get("ok")) and bool(out.get("meritstore", {}).get("ok"))
    out["config"] = {
        "meritsubs_public_base": _msu_base(),
        "meritsubs_consumer_ssot": "https://somatune.vercel.app/api/meritsubs",
        "meritstore_base": _mst_base(),
        "meritstore_admin_configured": bool(_mst_admin()),
        "webhook_secret_configured": bool(_webhook_secret()),
    }
    return out


async def run_square_probe(*, mode: str = "sandbox") -> dict[str, Any]:
    steps: list[dict[str, Any]] = []
    run_id = str(uuid.uuid4())
    email = f"ops-probe-{int(time.time())}@meritsubs.ops"
    subscriber_id: str | None = None
    token: str | None = None
    registration_id: str | None = None
    total_cents: int | None = None

    async with httpx.AsyncClient(timeout=45.0) as client:
        # 1 — meritstore health
        try:
            hres = await client.get(f"{_mst_base()}/api/v1/health")
            hbody = hres.json()
            sq_env = hbody.get("square_environment", "unknown")
            steps.append(_step("mst_health", hres.status_code == 200 and hbody.get("ok"), hbody))
            if not hbody.get("square"):
                return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps, "error": "meritstore square=false"}
        except Exception as exc:  # noqa: BLE001
            steps.append(_step("mst_health", False, str(exc)))
            return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps}

        # 2 — meritsubs onboard
        try:
            onboard = await client.post(
                f"{_msu_base()}/api/v1/subscribers/onboard/email",
                json={"email": email, "consumer_id": "somatune"},
            )
            obody = parse_json_response(onboard)
            ok = onboard.status_code == 200 and isinstance(obody, dict) and "token" in obody
            subscriber_id = (obody.get("subscriber") or {}).get("subscriber_id") if isinstance(obody, dict) else None
            token = obody.get("token") if isinstance(obody, dict) else None
            steps.append(
                _step(
                    "msu_onboard",
                    ok,
                    {
                        "subscriber_id": subscriber_id,
                        "tier": (obody.get("subscriber") or {}).get("tier") if isinstance(obody, dict) else None,
                        "url": f"{_msu_base()}/api/v1/subscribers/onboard/email",
                        "status": onboard.status_code,
                        "detail": obody if not ok else {"tier": (obody.get("subscriber") or {}).get("tier")},
                    },
                )
            )
            if not ok:
                return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps}
        except Exception as exc:  # noqa: BLE001
            steps.append(_step("msu_onboard", False, str(exc)))
            return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps}

        # 3 — meritstore registration (ONLY5CENT)
        reg_body = {
            "offering_ids": [_OFFERING],
            "guardian": {"parent_email": email, "subscriber_id": subscriber_id},
            "students": [{"plan": _OFFERING}],
            "promo_code": _PROMO,
        }
        try:
            reg = await client.post(f"{_mst_base()}/api/v1/tenants/{_TENANT}/registrations", json=reg_body)
            rbody = reg.json()
            registration_id = rbody.get("registration_id")
            total_cents = rbody.get("total_cents")
            steps.append(
                _step(
                    "mst_register",
                    reg.status_code == 200 and bool(registration_id),
                    {"registration_id": registration_id, "total_cents": total_cents, "promo": _PROMO},
                )
            )
            if reg.status_code != 200:
                return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps, "register_url": None}
        except Exception as exc:  # noqa: BLE001
            steps.append(_step("mst_register", False, str(exc)))
            return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps}

        register_url = (
            f"{_mst_base()}/{_TENANT}/register?"
            f"subscriber_id={subscriber_id}&plan={_OFFERING}&email={email}&promo={_PROMO}"
        )

        if mode == "production" or sq_env == "production":
            steps.append(
                _step(
                    "mst_checkout",
                    True,
                    {
                        "skipped": True,
                        "reason": "production — complete payment in meritstore UI",
                        "register_url": register_url,
                    },
                )
            )
            return {
                "ok": True,
                "partial": True,
                "run_id": run_id,
                "mode": "production",
                "steps": steps,
                "register_url": register_url,
                "registration_id": registration_id,
                "subscriber_id": subscriber_id,
                "token": token,
                "total_cents": total_cents,
            }

        # 4 — sandbox checkout
        try:
            pay = await client.post(
                f"{_mst_base()}/api/v1/tenants/{_TENANT}/checkout/square",
                json={"registration_id": registration_id, "source_id": "cnon:card-nonce-ok"},
            )
            pbody = pay.json()
            paid = pay.status_code == 200 and pbody.get("status") == "paid"
            steps.append(_step("mst_checkout", paid, pbody))
            if not paid:
                return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps}
        except Exception as exc:  # noqa: BLE001
            steps.append(_step("mst_checkout", False, str(exc)))
            return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps}

        # 5 — verify entitlements (webhook path); simulate if needed for ops debug
        certified = False
        last_ent: dict | None = None
        for attempt in range(3):
            ent_res = await client.get(
                f"{_msu_base()}/api/v1/entitlements",
                headers={"Authorization": f"Bearer {token}"},
            )
            last_ent = ent_res.json()
            tier = last_ent.get("tier")
            if tier in ("certified", "age_verified"):
                certified = True
                steps.append(_step("msu_entitlements", True, {"tier": tier, "attempt": attempt + 1}))
                break
            await _async_sleep(1.5)

        if not certified and _webhook_secret() and os.environ.get("MERITSUBS_OPS_ALLOW_WEBHOOK_SIM") == "1":
            sim = await client.post(
                f"{_msu_base()}/api/v1/webhooks/meritstore",
                headers={"x-meritstore-secret": _webhook_secret()},
                json={
                    "subscriber_id": subscriber_id,
                    "grants": {"meritsubs.tier": ["certified"]},
                    "payment_id": f"ops_sim_{run_id}",
                },
            )
            steps.append(_step("msu_webhook_sim", sim.status_code == 200, {"status": sim.status_code}))
            ent_res = await client.get(
                f"{_msu_base()}/api/v1/entitlements",
                headers={"Authorization": f"Bearer {token}"},
            )
            last_ent = ent_res.json()
            certified = last_ent.get("tier") in ("certified", "age_verified")

        if not certified:
            steps.append(
                _step(
                    "msu_entitlements",
                    False,
                    {
                        "tier": (last_ent or {}).get("tier"),
                        "hint": "meritstore notifyMeritsubsPurchase may not have fired; set MERITSUBS_OPS_ALLOW_WEBHOOK_SIM=1 to simulate",
                    },
                )
            )
            return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps, "registration_id": registration_id}

        # 6 — refund
        if not _mst_admin():
            steps.append(_step("mst_refund", False, {"error": "MERITSTORE_ADMIN_KEY not configured"}))
            return {"ok": False, "run_id": run_id, "mode": mode, "steps": steps}

        try:
            ref = await client.post(
                f"{_mst_base()}/api/v1/tenants/{_TENANT}/registrations/{registration_id}/refund",
                headers={"Authorization": f"Bearer {_mst_admin()}"},
                json={"amount_cents": total_cents},
            )
            rref = ref.json()
            steps.append(_step("mst_refund", ref.status_code == 200, rref))
            ok = ref.status_code == 200
        except Exception as exc:  # noqa: BLE001
            steps.append(_step("mst_refund", False, str(exc)))
            ok = False

        return {
            "ok": ok,
            "run_id": run_id,
            "mode": mode,
            "steps": steps,
            "registration_id": registration_id,
            "subscriber_id": subscriber_id,
        }


async def refund_registration(registration_id: str) -> dict[str, Any]:
    if not _mst_admin():
        raise ValueError("MERITSTORE_ADMIN_KEY not configured")
    async with httpx.AsyncClient(timeout=30.0) as client:
        ref = await client.post(
            f"{_mst_base()}/api/v1/tenants/{_TENANT}/registrations/{registration_id}/refund",
            headers={"Authorization": f"Bearer {_mst_admin()}"},
            json={},
        )
        ref.raise_for_status()
        return ref.json()


async def _async_sleep(seconds: float) -> None:
    import asyncio

    await asyncio.sleep(seconds)
