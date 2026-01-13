from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Set

from .models import LogRec, as_logrec

# --- Types ---
TxId = str
PageId = str

# Transaction Table entry: {"status": str, "lastLSN": int}
TT = Dict[TxId, Dict[str, Any]]

# Dirty Page Table entry: {"recLSN": int}
DPT = Dict[PageId, Dict[str, int]]

# Pages at crash / after recovery:
# pages[pid] = {"value": int, "pageLSN": int}
Pages = Dict[PageId, Dict[str, int]]

Report = Dict[str, Any]


def load_wal(path: Path) -> List[LogRec]:
    """Load WAL records from a JSONL file."""
    wal: List[LogRec] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            wal.append(as_logrec(json.loads(line)))
    return wal


def analysis(wal: List[LogRec], master_ckpt_lsn: int) -> Tuple[TT, DPT, Set[TxId], Set[TxId]]:
    """
    Phase 1: Analysis

    Requirements:
    - If master_ckpt_lsn > 0, begin from that LSN (inclusive) and seed TT/DPT from CHECKPOINT.
    - Build TT and DPT by scanning forward.
    - Return (TT, DPT, winners, losers).

    This assignment uses a simplified winner/loser rule:
    - A tx is a WINNER if a COMMIT record is seen for it (even if END is missing).
    - A tx is a LOSER otherwise (i.e., active/running/aborting at crash).
    """
    raise NotImplementedError


def redo(wal: List[LogRec], dpt: DPT, pages: Pages) -> List[int]:
    """
    Phase 2: Redo (repeat history)

    Requirements:
    - redo_start_lsn = min(recLSN) across the DPT; if DPT empty, return [].
    - Scan forward from redo_start_lsn and consider UPDATE records.
    - Apply UPDATE if and only if pages[page].pageLSN < rec.LSN (idempotent redo).
    - Record redone LSNs in order and return them.
    """
    raise NotImplementedError


def undo(wal: List[LogRec], losers: Set[TxId], pages: Pages) -> List[int]:
    """
    Phase 3: Undo (losers only; no CLRs)

    Requirements:
    - Scan log backward.
    - For each UPDATE belonging to a loser tx, apply before-image to the page.
    - This starter expects the following check before undo:
        undo only if pages[page].pageLSN == rec.LSN
      (i.e., only undo updates that are still reflected on disk after redo).

    - Return undone LSNs in the order they were undone (backward order).
    """
    raise NotImplementedError


def format_report(report: Report) -> str:
    """Produce a deterministic, diff-friendly report text."""
    lines: List[str] = []
    lines.append("== Analysis ==")
    lines.append(f"winners: {sorted(report['winners'])}")
    lines.append(f"losers: {sorted(report['losers'])}")
    lines.append("TT:")
    for tx in sorted(report["TT"].keys()):
        e = report["TT"][tx]
        lines.append(f"  {tx}: status={e['status']} lastLSN={e['lastLSN']}")
    lines.append("DPT:")
    for p in sorted(report["DPT"].keys()):
        lines.append(f"  {p}: recLSN={report['DPT'][p]['recLSN']}")
    lines.append("")
    lines.append("== Redo ==")
    lines.append(f"redoneLSNs: {report['redoneLSNs']}")
    lines.append("")
    lines.append("== Undo ==")
    lines.append(f"undoneLSNs: {report['undoneLSNs']}")
    lines.append("")
    lines.append("== Final Pages ==")
    for p in sorted(report["final_pages"].keys()):
        v = report["final_pages"][p]["value"]
        lsn = report["final_pages"][p]["pageLSN"]
        lines.append(f"{p}: value={v} pageLSN={lsn}")
    lines.append("")
    return "\n".join(lines)


def recover(scenario_dir: Path) -> Tuple[Pages, Report]:
    """
    Load scenario files, run analysis/redo/undo, and return final pages + report.

    Scenario directory must contain:
    - wal.jsonl
    - disk_pages.json
    - master.json  (with key master_ckpt_lsn)
    """
    scenario_dir = Path(scenario_dir)
    wal = load_wal(scenario_dir / "wal.jsonl")
    pages: Pages = json.loads((scenario_dir / "disk_pages.json").read_text(encoding="utf-8"))
    master = json.loads((scenario_dir / "master.json").read_text(encoding="utf-8"))
    master_ckpt_lsn = int(master.get("master_ckpt_lsn", 0))

    TT, DPT, winners, losers = analysis(wal, master_ckpt_lsn)
    redone = redo(wal, DPT, pages)
    undone = undo(wal, losers, pages)

    report: Report = {
        "winners": sorted(winners),
        "losers": sorted(losers),
        "TT": TT,
        "DPT": DPT,
        "redoneLSNs": redone,
        "undoneLSNs": undone,
        "final_pages": pages,
    }
    return pages, report
