"""SQLite persistence for decision app."""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any

from app.config import DB_PATH


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with get_db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS problems (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                summary TEXT,
                eisenhower TEXT,
                owner TEXT,
                rank INTEGER,
                status TEXT DEFAULT 'raw',
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS problem_statements (
                problem_id TEXT PRIMARY KEY,
                context TEXT,
                friction TEXT,
                impact TEXT,
                constraints TEXT,
                success_criteria TEXT,
                tech_refs TEXT,
                repos_impacted TEXT,
                eb25_rank INTEGER,
                updated_at TEXT,
                FOREIGN KEY (problem_id) REFERENCES problems(id)
            );

            CREATE TABLE IF NOT EXISTS rfcs (
                id TEXT PRIMARY KEY,
                problem_id TEXT NOT NULL,
                title TEXT,
                status TEXT DEFAULT 'DRAFT',
                proposed_solution TEXT,
                detailed_design TEXT,
                cost_resources TEXT,
                tradeoffs_risks TEXT,
                options_json TEXT,
                reviewer_comments TEXT,
                updated_at TEXT,
                FOREIGN KEY (problem_id) REFERENCES problems(id)
            );

            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                problem_id TEXT,
                rfc_ids TEXT,
                title TEXT,
                status TEXT DEFAULT 'draft',
                handoff_path TEXT,
                exec_signoff INTEGER DEFAULT 1,
                handoff_complete INTEGER DEFAULT 0,
                expedited INTEGER DEFAULT 0,
                emergency INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (problem_id) REFERENCES problems(id)
            );

            CREATE TABLE IF NOT EXISTS context_cards (
                decision_id TEXT PRIMARY KEY,
                problem_alignment TEXT,
                metric_alignment TEXT,
                values_vs_tactical TEXT,
                alignment_notes TEXT,
                risk_scores_json TEXT,
                risk_total INTEGER,
                risk_category TEXT,
                risk_mitigation TEXT,
                undo_30_days INTEGER,
                reversal_cost REAL,
                reversal_time_weeks REAL,
                irreversible_commitments TEXT,
                rev_type TEXT,
                rev_type_override TEXT,
                framework_primary TEXT,
                framework_alternatives TEXT,
                framework_override TEXT,
                framework_rationale TEXT,
                flags_json TEXT,
                completed_by TEXT,
                updated_at TEXT,
                FOREIGN KEY (decision_id) REFERENCES decisions(id)
            );

            CREATE TABLE IF NOT EXISTS framework_records (
                decision_id TEXT PRIMARY KEY,
                framework_name TEXT,
                data_json TEXT,
                updated_at TEXT,
                FOREIGN KEY (decision_id) REFERENCES decisions(id)
            );

            CREATE TABLE IF NOT EXISTS retrospections (
                decision_id TEXT PRIMARY KEY,
                data_json TEXT,
                completed INTEGER DEFAULT 0,
                updated_at TEXT,
                FOREIGN KEY (decision_id) REFERENCES decisions(id)
            );

            CREATE TABLE IF NOT EXISTS register_entries (
                decision_id TEXT PRIMARY KEY,
                date TEXT,
                title TEXT,
                framework TEXT,
                risk_level TEXT,
                reversibility TEXT,
                outcome TEXT,
                status TEXT,
                document_link TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT,
                entity_id TEXT,
                action TEXT,
                actor TEXT,
                details TEXT,
                created_at TEXT
            );
            """
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def audit(entity_type: str, entity_id: str, action: str, actor: str, details: str = "") -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT INTO audit_log (entity_type, entity_id, action, actor, details, created_at) VALUES (?,?,?,?,?,?)",
            (entity_type, entity_id, action, actor, details, _now()),
        )


# --- Problems ---


def list_problems() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM problems ORDER BY rank IS NULL, rank, created_at"
        ).fetchall()
    return [dict(r) for r in rows]


def count_active_problems() -> int:
    with get_db() as conn:
        n = conn.execute(
            "SELECT COUNT(*) FROM problems WHERE status NOT IN ('avoid', 'archived')"
        ).fetchone()[0]
    return int(n)


def get_problem(problem_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM problems WHERE id = ?", (problem_id,)).fetchone()
    return dict(row) if row else None


def upsert_problem(data: dict, actor: str = "system") -> None:
    now = _now()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO problems (id, title, summary, eisenhower, owner, rank, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title, summary=excluded.summary, eisenhower=excluded.eisenhower,
                owner=excluded.owner, rank=excluded.rank, status=excluded.status, updated_at=excluded.updated_at
            """,
            (
                data["id"],
                data["title"],
                data.get("summary", ""),
                data.get("eisenhower", ""),
                data.get("owner", ""),
                data.get("rank"),
                data.get("status", "raw"),
                data.get("created_at", now),
                now,
            ),
        )
    audit("problem", data["id"], "upsert", actor)


def delete_problem(problem_id: str, actor: str = "system") -> None:
    with get_db() as conn:
        conn.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
    audit("problem", problem_id, "delete", actor)


# --- Problem statements ---


def get_problem_statement(problem_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM problem_statements WHERE problem_id = ?", (problem_id,)
        ).fetchone()
    return dict(row) if row else None


def upsert_problem_statement(problem_id: str, data: dict, actor: str = "system") -> None:
    now = _now()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO problem_statements (
                problem_id, context, friction, impact, constraints, success_criteria,
                tech_refs, repos_impacted, eb25_rank, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(problem_id) DO UPDATE SET
                context=excluded.context, friction=excluded.friction, impact=excluded.impact,
                constraints=excluded.constraints, success_criteria=excluded.success_criteria,
                tech_refs=excluded.tech_refs, repos_impacted=excluded.repos_impacted,
                eb25_rank=excluded.eb25_rank, updated_at=excluded.updated_at
            """,
            (
                problem_id,
                data.get("context", ""),
                data.get("friction", ""),
                data.get("impact", ""),
                data.get("constraints", ""),
                data.get("success_criteria", ""),
                data.get("tech_refs", ""),
                data.get("repos_impacted", ""),
                data.get("eb25_rank"),
                now,
            ),
        )
        conn.execute(
            "UPDATE problems SET status = ?, updated_at = ? WHERE id = ?",
            ("identification", now, problem_id),
        )
    audit("problem_statement", problem_id, "upsert", actor)


# --- RFCs ---


def list_rfcs(problem_id: str | None = None) -> list[dict]:
    with get_db() as conn:
        if problem_id:
            rows = conn.execute(
                "SELECT * FROM rfcs WHERE problem_id = ? ORDER BY updated_at DESC",
                (problem_id,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM rfcs ORDER BY updated_at DESC").fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["options"] = json.loads(d.get("options_json") or "[]")
        result.append(d)
    return result


def get_rfc(rfc_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM rfcs WHERE id = ?", (rfc_id,)).fetchone()
    if not row:
        return None
    d = dict(row)
    d["options"] = json.loads(d.get("options_json") or "[]")
    return d


def upsert_rfc(data: dict, actor: str = "system") -> None:
    now = _now()
    options_json = json.dumps(data.get("options", []))
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO rfcs (
                id, problem_id, title, status, proposed_solution, detailed_design,
                cost_resources, tradeoffs_risks, options_json, reviewer_comments, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title, status=excluded.status,
                proposed_solution=excluded.proposed_solution, detailed_design=excluded.detailed_design,
                cost_resources=excluded.cost_resources, tradeoffs_risks=excluded.tradeoffs_risks,
                options_json=excluded.options_json, reviewer_comments=excluded.reviewer_comments,
                updated_at=excluded.updated_at
            """,
            (
                data["id"],
                data["problem_id"],
                data.get("title", ""),
                data.get("status", "DRAFT"),
                data.get("proposed_solution", ""),
                data.get("detailed_design", ""),
                data.get("cost_resources", ""),
                data.get("tradeoffs_risks", ""),
                options_json,
                data.get("reviewer_comments", ""),
                now,
            ),
        )
    audit("rfc", data["id"], "upsert", actor)


def rfc_option_count(rfc_id: str) -> int:
    rfc = get_rfc(rfc_id)
    if not rfc:
        return 0
    return len([o for o in rfc.get("options", []) if o.get("name", "").strip()])


# --- Decisions ---


def list_decisions(status: str | None = None) -> list[dict]:
    with get_db() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM decisions WHERE status = ? ORDER BY updated_at DESC",
                (status,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM decisions ORDER BY updated_at DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def get_decision(decision_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,)).fetchone()
    return dict(row) if row else None


def upsert_decision(data: dict, actor: str = "system") -> None:
    now = _now()
    rfc_ids = data.get("rfc_ids", "")
    if isinstance(rfc_ids, list):
        rfc_ids = ",".join(rfc_ids)
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO decisions (
                id, problem_id, rfc_ids, title, status, handoff_path,
                exec_signoff, handoff_complete, expedited, emergency, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                problem_id=excluded.problem_id, rfc_ids=excluded.rfc_ids, title=excluded.title,
                status=excluded.status, handoff_path=excluded.handoff_path,
                exec_signoff=excluded.exec_signoff, handoff_complete=excluded.handoff_complete,
                expedited=excluded.expedited, emergency=excluded.emergency, updated_at=excluded.updated_at
            """,
            (
                data["id"],
                data.get("problem_id"),
                rfc_ids,
                data.get("title", ""),
                data.get("status", "draft"),
                data.get("handoff_path", "standard"),
                int(data.get("exec_signoff", 1)),
                int(data.get("handoff_complete", 0)),
                int(data.get("expedited", 0)),
                int(data.get("emergency", 0)),
                data.get("created_at", now),
                now,
            ),
        )
    audit("decision", data["id"], "upsert", actor)


# --- Context cards ---


def get_context_card(decision_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM context_cards WHERE decision_id = ?", (decision_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["risk_scores"] = json.loads(d.get("risk_scores_json") or "{}")
    d["flags"] = json.loads(d.get("flags_json") or "{}")
    return d


def upsert_context_card(decision_id: str, data: dict, actor: str = "system") -> None:
    now = _now()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO context_cards (
                decision_id, problem_alignment, metric_alignment, values_vs_tactical,
                alignment_notes, risk_scores_json, risk_total, risk_category, risk_mitigation,
                undo_30_days, reversal_cost, reversal_time_weeks, irreversible_commitments,
                rev_type, rev_type_override, framework_primary, framework_alternatives,
                framework_override, framework_rationale, flags_json, completed_by, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(decision_id) DO UPDATE SET
                problem_alignment=excluded.problem_alignment,
                metric_alignment=excluded.metric_alignment,
                values_vs_tactical=excluded.values_vs_tactical,
                alignment_notes=excluded.alignment_notes,
                risk_scores_json=excluded.risk_scores_json,
                risk_total=excluded.risk_total,
                risk_category=excluded.risk_category,
                risk_mitigation=excluded.risk_mitigation,
                undo_30_days=excluded.undo_30_days,
                reversal_cost=excluded.reversal_cost,
                reversal_time_weeks=excluded.reversal_time_weeks,
                irreversible_commitments=excluded.irreversible_commitments,
                rev_type=excluded.rev_type,
                rev_type_override=excluded.rev_type_override,
                framework_primary=excluded.framework_primary,
                framework_alternatives=excluded.framework_alternatives,
                framework_override=excluded.framework_override,
                framework_rationale=excluded.framework_rationale,
                flags_json=excluded.flags_json,
                completed_by=excluded.completed_by,
                updated_at=excluded.updated_at
            """,
            (
                decision_id,
                data.get("problem_alignment"),
                data.get("metric_alignment"),
                data.get("values_vs_tactical"),
                data.get("alignment_notes", ""),
                json.dumps(data.get("risk_scores", {})),
                data.get("risk_total"),
                data.get("risk_category"),
                data.get("risk_mitigation", ""),
                int(data.get("undo_30_days", 0)),
                data.get("reversal_cost", 0),
                data.get("reversal_time_weeks", 0),
                data.get("irreversible_commitments", ""),
                data.get("rev_type"),
                data.get("rev_type_override"),
                data.get("framework_primary"),
                data.get("framework_alternatives"),
                data.get("framework_override"),
                data.get("framework_rationale", ""),
                json.dumps(data.get("flags", {})),
                data.get("completed_by", ""),
                now,
            ),
        )
    audit("context_card", decision_id, "upsert", actor)


# --- Framework records ---


def get_framework_record(decision_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM framework_records WHERE decision_id = ?", (decision_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["data"] = json.loads(d.get("data_json") or "{}")
    return d


def upsert_framework_record(
    decision_id: str, framework_name: str, data: dict[str, Any], actor: str = "system"
) -> None:
    now = _now()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO framework_records (decision_id, framework_name, data_json, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(decision_id) DO UPDATE SET
                framework_name=excluded.framework_name,
                data_json=excluded.data_json,
                updated_at=excluded.updated_at
            """,
            (decision_id, framework_name, json.dumps(data), now),
        )
    audit("framework_record", decision_id, "upsert", actor)


# --- Retrospection ---


def get_retrospection(decision_id: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM retrospections WHERE decision_id = ?", (decision_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["data"] = json.loads(d.get("data_json") or "{}")
    return d


def upsert_retrospection(decision_id: str, data: dict, completed: bool, actor: str = "system") -> None:
    now = _now()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO retrospections (decision_id, data_json, completed, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(decision_id) DO UPDATE SET
                data_json=excluded.data_json, completed=excluded.completed, updated_at=excluded.updated_at
            """,
            (decision_id, json.dumps(data), int(completed), now),
        )
    audit("retrospection", decision_id, "upsert", actor)


# --- Register ---


def list_register() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM register_entries ORDER BY date DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def upsert_register_entry(data: dict, actor: str = "system") -> None:
    now = _now()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO register_entries (
                decision_id, date, title, framework, risk_level, reversibility,
                outcome, status, document_link, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(decision_id) DO UPDATE SET
                date=excluded.date, title=excluded.title, framework=excluded.framework,
                risk_level=excluded.risk_level, reversibility=excluded.reversibility,
                outcome=excluded.outcome, status=excluded.status,
                document_link=excluded.document_link, updated_at=excluded.updated_at
            """,
            (
                data["decision_id"],
                data.get("date"),
                data.get("title"),
                data.get("framework"),
                data.get("risk_level"),
                data.get("reversibility"),
                data.get("outcome", ""),
                data.get("status", "ACTIVE"),
                data.get("document_link", ""),
                now,
            ),
        )
    audit("register", data["decision_id"], "upsert", actor)


def register_stats() -> dict:
    entries = list_register()
    stats: dict = {"total": len(entries), "by_framework": {}, "by_risk": {}}
    for e in entries:
        fw = e.get("framework") or "unknown"
        stats["by_framework"][fw] = stats["by_framework"].get(fw, 0) + 1
        rk = e.get("risk_level") or "unknown"
        stats["by_risk"][rk] = stats["by_risk"].get(rk, 0) + 1
    return stats
