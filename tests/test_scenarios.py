from __future__ import annotations

import json
from pathlib import Path

from miniaries.recovery import recover, format_report

SCENARIOS_DIR = Path(__file__).resolve().parents[1] / "scenarios"

def test_all_scenarios_match_expected():
    for scenario in sorted([p for p in SCENARIOS_DIR.iterdir() if p.is_dir()]):
        pages, report = recover(scenario)

        expected_report = (scenario / "expected_report.txt").read_text(encoding="utf-8").strip() + "\n"
        expected_pages = json.loads((scenario / "expected_pages.json").read_text(encoding="utf-8"))

        got_report = format_report(report).strip() + "\n"

        assert got_report == expected_report, f"Report mismatch for {scenario.name}"
        assert pages == expected_pages, f"Pages mismatch for {scenario.name}"
