from __future__ import annotations

import json
from pathlib import Path
import sys

from .recovery import recover, format_report

def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("Usage: python -m miniaries.cli <scenario_dir>")
        return 2
    scenario_dir = Path(argv[0])
    pages, report = recover(scenario_dir)
    print(format_report(report))
    # Also write outputs (handy for manual diff)
    (scenario_dir / "out_report.txt").write_text(format_report(report), encoding="utf-8")
    (scenario_dir / "out_pages.json").write_text(json.dumps(pages, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
