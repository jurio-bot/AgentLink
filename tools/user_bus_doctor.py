#!/usr/bin/env python3
"""Read-only diagnostics for systemd --user / D-Bus environment problems."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

KEYS = ("XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS")


def _unix_bus_path(address: str) -> str | None:
    if not address.startswith("unix:"):
        return None
    fields = address[5:].split(",")
    for field in fields:
        if field.startswith("path="):
            return field[5:]
    return None


def diagnose_env(env: dict[str, str], exists=os.path.exists) -> list[dict]:
    checks: list[dict] = []
    runtime = env.get("XDG_RUNTIME_DIR", "").strip()
    if not runtime:
        checks.append({"check": "XDG_RUNTIME_DIR", "status": "error", "detail": "missing"})
    elif not os.path.isabs(runtime):
        checks.append({"check": "XDG_RUNTIME_DIR", "status": "error", "detail": "not absolute"})
    elif not exists(runtime):
        checks.append({"check": "XDG_RUNTIME_DIR", "status": "error", "detail": "path does not exist"})
    else:
        checks.append({"check": "XDG_RUNTIME_DIR", "status": "ok", "detail": runtime})
    bus = env.get("DBUS_SESSION_BUS_ADDRESS", "").strip()
    if not bus:
        checks.append({"check": "DBUS_SESSION_BUS_ADDRESS", "status": "error", "detail": "missing"})
    else:
        bus_path = _unix_bus_path(bus)
        if bus.startswith("unix:path=") and bus_path and not exists(bus_path):
            checks.append({"check": "DBUS_SESSION_BUS_ADDRESS", "status": "error", "detail": f"socket path missing: {bus_path}"})
        elif bus_path:
            checks.append({"check": "DBUS_SESSION_BUS_ADDRESS", "status": "ok", "detail": f"unix socket: {bus_path}"})
        elif bus.startswith("unix:abstract="):
            checks.append({"check": "DBUS_SESSION_BUS_ADDRESS", "status": "ok", "detail": "unix abstract socket"})
        else:
            checks.append({"check": "DBUS_SESSION_BUS_ADDRESS", "status": "warn", "detail": "address format not validated"})
    return checks


def probe_systemd_user(timeout: float = 3.0) -> dict:
    try:
        proc = subprocess.run(
            ["systemctl", "--user", "show-environment"],
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "error", "detail": str(exc), "environment": {}}
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or f"exit {proc.returncode}").strip()
        return {"status": "error", "detail": detail, "environment": {}}
    manager_env = {}
    for line in proc.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            manager_env[key] = value
    return {"status": "ok", "detail": "systemd user manager reachable", "environment": manager_env}


def build_report(env: dict[str, str], probe: dict | None = None, exists=os.path.exists) -> dict:
    checks = diagnose_env(env, exists=exists)
    if probe is not None:
        checks.append({"check": "systemd_user_manager", "status": probe["status"], "detail": probe["detail"]})
    errors = [c for c in checks if c["status"] == "error"]
    warnings = [c for c in checks if c["status"] == "warn"]
    return {
        "healthy": not errors,
        "checks": checks,
        "summary": {"errors": len(errors), "warnings": len(warnings)},
        "hint": (
            "If this only fails from a remote shell or service, compare the caller's "
            "XDG_RUNTIME_DIR / DBUS_SESSION_BUS_ADDRESS with a working login session."
        ),
    }


def render_text(report: dict) -> str:
    lines = []
    for check in report["checks"]:
        mark = {"ok": "OK", "warn": "WARN", "error": "ERROR"}[check["status"]]
        lines.append(f"[{mark}] {check['check']}: {check['detail']}")
    lines.append(report["hint"])
    return "\n".join(lines)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--no-systemctl", action="store_true", help="skip the read-only systemctl probe")
    args = parser.parse_args(argv)

    probe = None if args.no_systemctl else probe_systemd_user()
    report = build_report(dict(os.environ), probe=probe)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 0 if report["healthy"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
