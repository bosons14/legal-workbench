#!/usr/bin/env python3
"""Smoke tests for legal-workbench scripts. Run: python3 tests/test_scripts.py"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "plugins" / "legal-workbench"
sys.path.insert(0, str(ROOT / "scripts"))

import limitation  # noqa: E402
import redact  # noqa: E402
import conflicts  # noqa: E402


def test_limitation():
    # 3 months from 31 Aug -> 30 Nov (month-end clamp), Monday, no roll
    raw, final, _ = limitation.compute(dt.date(2026, 8, 31), "3m")
    assert raw == dt.date(2026, 11, 30) == final
    # 30 days ending on a Saturday rolls to Monday
    raw, final, skipped = limitation.compute(dt.date(2026, 10, 1), "30d")
    assert raw == dt.date(2026, 10, 31) and final == dt.date(2026, 11, 2) and len(skipped) == 2
    # holiday roll
    _, final, _ = limitation.compute(dt.date(2026, 1, 1), "1d", holidays={dt.date(2026, 1, 2)})
    assert final == dt.date(2026, 1, 5)
    # leap year clamp
    assert limitation.add_period(dt.date(2024, 2, 29), "1y") == dt.date(2025, 2, 28)


def test_redact():
    assert redact.verhoeff_ok("234123412346") and not redact.verhoeff_ok("234123412345")
    assert redact.luhn_ok("4111111111111111") and not redact.luhn_ok("4111111111111112")
    r = redact.Redactor("pseudo", terms=[("person", "Ravi Kumar")])
    out = r.run("Ravi Kumar emailed ravi@x.com; RAVI KUMAR called 9876543210. PAN ABCPK1234F.")
    assert "Ravi" not in out and "RAVI" not in out
    assert out.count("PERSON_1") == 2 and "EMAIL_1" in out and "PHONE_1" in out and "PAN_1" in out
    # invalid Aadhaar-like number is left alone
    assert "2341 2341 2345" in redact.Redactor("mask").run("ref 2341 2341 2345")


def test_conflicts():
    assert conflicts.score("ACME Holdings Private Limited", "Acme Holdings Pvt. Ltd.") == 1.0
    assert conflicts.score("Zephyr Ltd", "Acme Holdings Pvt Ltd") < 0.5


def test_hook():
    hook = ROOT / "hooks" / "confidentiality_guard.py"
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / ".legal").mkdir()
        (Path(d) / ".legal" / "confidential-terms.txt").write_text("client=Nimbus Software\n")
        env = {**os.environ, "CLAUDE_PROJECT_DIR": d}

        def run(event):
            p = subprocess.run([sys.executable, str(hook)], input=json.dumps(event),
                               capture_output=True, text=True, env=env)
            return p.stdout.strip()
        blocked = run({"tool_name": "WebSearch", "tool_input": {"query": "nimbus software lawsuit"}})
        assert json.loads(blocked)["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert run({"tool_name": "WebSearch", "tool_input": {"query": "software licence fee recovery"}}) == ""
        assert run({"tool_name": "Bash", "tool_input": {"command": "grep 'Nimbus Software' notes.md"}}) == ""
        assert run({"tool_name": "Bash", "tool_input": {"command": "curl 'https://x.com/?q=Nimbus Software'"}}) != ""


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all tests passed")
