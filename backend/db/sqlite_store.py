"""Small SQLite store for auditable AEGIS AI records."""

import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "aegis_ai.sqlite3"


def initialize_sqlite() -> None:
    """Create the audit table if it does not exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                record_json TEXT NOT NULL,
                record_hash TEXT NOT NULL,
                approved INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        connection.commit()


def write_audit_log(record: dict[str, Any]) -> str:
    """Persist an audit record and return its stable audit identifier."""
    initialize_sqlite()
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO audit_logs
            (id, created_at, status, record_json, record_hash, approved)
            VALUES (?, ?, ?, ?, ?, ?)
            """ ,
            (
                record["audit_log_id"],
                record["timestamp"],
                record["status"],
                json.dumps(record, sort_keys=True),
                record["record_hash"],
                int(record.get("approved", False)),
            ),
        )
        connection.commit()
    return record["audit_log_id"]


def approve_audit_log(audit_log_id: str) -> bool:
    """Mark a human-reviewed audit record as approved."""
    initialize_sqlite()
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "UPDATE audit_logs SET approved = 1, status = 'approved' WHERE id = ?",
            (audit_log_id,),
        )
        connection.commit()
        return cursor.rowcount > 0
