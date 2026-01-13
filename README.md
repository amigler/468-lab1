# Mini-ARIES Recovery (No CLRs) — Starter Repo

This repo is a focused programming assignment: implement a tight ARIES-style recovery simulation
from a write-ahead log (WAL) with the classic phases:

- Analysis (build TT + DPT, classify winners/losers)
- Redo (repeat history, idempotent via pageLSN)
- Undo (roll back losers only; **no CLRs**, no "crash during undo" support)

## Quickstart

```bash
python -m miniaries.cli scenarios/s1_basic
```

Run tests:

```bash
python -m pip install -e .
python -m pytest -q
```

## Data model

- WAL: `wal.jsonl` (one JSON record per line)
- Disk pages at crash: `disk_pages.json`
- Master record: `master.json` containing `master_ckpt_lsn`

A page is stored as:

```json
"P1": {"value": 999, "pageLSN": 80}
```

## What you implement

Edit `src/miniaries/recovery.py` and implement:

- `analysis(wal, master_ckpt_lsn)`
- `redo(wal, dpt, pages)`
- `undo(wal, losers, pages)`
- `recover(scenario_dir)`

Your implementation must exactly match the **diff-friendly report format** produced by `format_report()`.

## Out of scope

- Compensation log records (CLRs)
- Partial rollbacks
- Crashes during undo
- Storage manager / buffer manager details
