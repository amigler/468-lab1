from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class LogRec:
    LSN: int
    type: str
    tx: Optional[str] = None
    page: Optional[str] = None
    before: Optional[int] = None
    after: Optional[int] = None
    # CHECKPOINT payloads:
    DPT: Optional[Dict[str, int]] = None
    TT: Optional[Dict[str, Dict[str, Any]]] = None

def as_logrec(obj: Dict[str, Any]) -> LogRec:
    return LogRec(**obj)
