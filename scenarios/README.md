Scenarios included:

- s1_basic: checkpoint + one committed winner + one loser that updated multiple pages including overwriting a winner's page.
- s2_idempotent_redo: disk already has some updates; redo must be idempotent and skip them.
- s3_three_txs: three transactions; one committed, one aborting at crash, one running. Interleaving updates to the same page.

Each scenario folder contains:
- wal.jsonl
- disk_pages.json
- master.json
- expected_report.txt
- expected_pages.json
