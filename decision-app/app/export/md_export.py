"""Export filled records to Markdown under data/exports/."""

import io
import zipfile
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import EXPORT_DIR

TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(),
)


def _write(decision_id: str, filename: str, content: str) -> Path:
    out_dir = EXPORT_DIR / decision_id
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    path.write_text(content, encoding="utf-8")
    return path


def export_problem_statement(problem_id: str, data: dict, author: str = "") -> Path:
    tpl = _env.get_template("problem_statement.md.j2")
    content = tpl.render(
        problem_id=problem_id,
        date=date.today().isoformat(),
        author=author,
        eb25_rank=data.get("eb25_rank", ""),
        tech_refs=data.get("tech_refs", ""),
        repos_impacted=data.get("repos_impacted", ""),
        context=data.get("context", ""),
        friction=data.get("friction", ""),
        impact=data.get("impact", ""),
        constraints=data.get("constraints", ""),
        success_criteria=data.get("success_criteria", ""),
    )
    return _write(problem_id, f"{problem_id}-problem-statement.md", content)


def export_rfc(rfc_id: str, data: dict) -> Path:
    tpl = _env.get_template("rfc.md.j2")
    options = []
    for i, opt in enumerate(data.get("options", [])):
        label = chr(ord("A") + i)
        options.append(
            {
                "label": f"Option {label}",
                "name": opt.get("name", ""),
                "description": opt.get("description", ""),
            }
        )
    content = tpl.render(
        rfc_id=rfc_id,
        problem_id=data.get("problem_id", ""),
        date=date.today().isoformat(),
        author=data.get("author", ""),
        status=data.get("status", "DRAFT"),
        proposed_solution=data.get("proposed_solution", ""),
        detailed_design=data.get("detailed_design", ""),
        cost_resources=data.get("cost_resources", ""),
        tradeoffs_risks=data.get("tradeoffs_risks", ""),
        options=options,
        reviewer_comments=data.get("reviewer_comments", ""),
    )
    return _write(data.get("problem_id", rfc_id), f"{rfc_id}-rfc.md", content)


def export_context_card(decision_id: str, ctx: dict, decision: dict) -> Path:
    tpl = _env.get_template("context_card.md.j2")
    risk_scores = ctx.get("risk_scores", {})
    formatted = {
        k: {"value": v.get("score", ""), "rationale": v.get("rationale", "")}
        for k, v in risk_scores.items()
    }
    content = tpl.render(
        decision_id=decision_id,
        date=date.today().isoformat(),
        completed_by=ctx.get("completed_by", ""),
        title=decision.get("title", ""),
        problem_id=decision.get("problem_id", ""),
        rfc_ids=decision.get("rfc_ids", ""),
        exec_signoff="YES" if decision.get("exec_signoff") else "NO",
        handoff_complete=decision.get("handoff_path", "standard").upper(),
        handoff_notes="",
        problem_alignment=ctx.get("problem_alignment", ""),
        metric_alignment=ctx.get("metric_alignment", ""),
        values_vs_tactical=ctx.get("values_vs_tactical", ""),
        alignment_notes=ctx.get("alignment_notes", ""),
        risk_scores=formatted,
        risk_total=ctx.get("risk_total", ""),
        risk_category=ctx.get("risk_category", ""),
        risk_mitigation=ctx.get("risk_mitigation", ""),
        undo_30_days="YES" if ctx.get("undo_30_days") else "NO",
        reversal_cost=ctx.get("reversal_cost", 0),
        reversal_time_weeks=ctx.get("reversal_time_weeks", 0),
        irreversible_commitments=ctx.get("irreversible_commitments", ""),
        rev_type=ctx.get("rev_type_override") or ctx.get("rev_type", ""),
        framework=ctx.get("framework_override") or ctx.get("framework_primary", ""),
        framework_rationale=ctx.get("framework_rationale", ""),
        alternatives=ctx.get("framework_alternatives", ""),
    )
    return _write(decision_id, f"{decision_id}-context-card.md", content)


def export_ice(decision_id: str, data: dict, title: str) -> Path:
    tpl = _env.get_template("ice_scorecard.md.j2")
    rows = []
    for row in data.get("scorecard", []):
        i, c, e = row.get("impact", 0), row.get("confidence", 0), row.get("ease", 0)
        rows.append(
            {
                "option": row.get("option", ""),
                "impact": i,
                "confidence": c,
                "ease": e,
                "ice_score": i * c * e,
            }
        )
    content = tpl.render(
        decision_id=decision_id,
        date=date.today().isoformat(),
        title=title,
        rows=rows,
        selected_option=data.get("selected_option", ""),
        rationale=data.get("rationale", ""),
        implementation_notes=data.get("implementation_notes", ""),
        signoff_a=data.get("signoff_a", ""),
        signoff_b=data.get("signoff_b", ""),
    )
    return _write(decision_id, f"{decision_id}-ice-scorecard.md", content)


def export_generic_framework(decision_id: str, framework: str, data: dict) -> Path:
    """Fallback markdown for non-ICE frameworks."""
    lines = [f"# {framework} — Decision Record", "", f"**Decision ID:** {decision_id}", ""]
    for key, val in data.items():
        if isinstance(val, dict):
            lines.append(f"## {key.replace('_', ' ').title()}")
            for k2, v2 in val.items():
                lines.append(f"- **{k2}:** {v2}")
            lines.append("")
        else:
            lines.append(f"**{key.replace('_', ' ').title()}:** {val}")
            lines.append("")
    slug = framework.lower().replace(" ", "-")
    return _write(decision_id, f"{decision_id}-{slug}.md", "\n".join(lines))


def zip_exports(decision_id: str) -> bytes | None:
    out_dir = EXPORT_DIR / decision_id
    if not out_dir.exists():
        return None
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in out_dir.glob("*.md"):
            zf.write(f, arcname=f.name)
    buf.seek(0)
    return buf.getvalue()
