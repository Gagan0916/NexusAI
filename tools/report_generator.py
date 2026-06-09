from __future__ import annotations

from datetime import datetime


def _section(title: str, content: str = "") -> str:
    bar = "=" * 60
    return f"\n{bar}\n  {title.upper()}\n{bar}\n{content}\n"


def build_business_plan(ctx: dict) -> str:
    idea = ctx.get("startup_idea", "")
    ceo = ctx.get("ceo", {})
    research = ctx.get("research", {})
    analyst = ctx.get("analyst", {})
    industry = ceo.get("industry", {})
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"NEXUSAI — BUSINESS PLAN",
        f"Generated: {now}",
        f"Startup Idea: {idea}",
        "",
        "━" * 60,
        "",
    ]

    lines.append(_section("Executive Summary", ceo.get("strategic_overview", "")))

    lines.append(_section("Market Analysis",
        f"Market Size     : {research.get('market_size', industry.get('market_size', 'N/A'))}\n"
        f"Growth Rate     : {research.get('growth_rate', '')}% CAGR\n"
        f"Market Demand   : {research.get('market_demand_score', '')}/10\n"
        f"Competition     : {research.get('competition_score', '')}/10\n"
        f"Market Gap      : {research.get('market_gap', '')}"
    ))

    tam_sam_som = research.get("tam_sam_som", {})
    if tam_sam_som:
        lines.append(_section("TAM / SAM / SOM",
            "\n".join(f"{k}: {v}" for k, v in tam_sam_som.items())
        ))

    competitors = research.get("competitors", [])
    if competitors:
        comp_lines = "\n".join(
            f"  • {c['name']} ({c['stage']}) — Weakness: {c['weakness']}"
            for c in competitors
        )
        lines.append(_section("Competitive Landscape", comp_lines))

    revenue_streams = analyst.get("revenue_streams", [])
    if revenue_streams:
        rev_lines = "\n".join(
            f"  • {r['stream']}: {r['price']} ({r['type']})"
            for r in revenue_streams
        )
        lines.append(_section("Revenue Model", rev_lines))

    ue = analyst.get("unit_economics", {})
    if ue:
        lines.append(_section("Unit Economics",
            f"CAC             : {ue.get('cac', '')}\n"
            f"LTV             : {ue.get('ltv', '')}\n"
            f"LTV/CAC Ratio   : {ue.get('ltv_cac_ratio', '')}\n"
            f"Payback Period  : {ue.get('payback_period', '')}\n"
            f"Gross Margin    : {ue.get('gross_margin', '')}"
        ))

    risks = analyst.get("risks", [])
    if risks:
        risk_lines = "\n".join(
            f"  [{r.get('severity', 'Medium'):6}] {r['risk']}\n"
            f"           Mitigation: {r['mitigation']}"
            for r in risks
        )
        lines.append(_section("Risk Register", risk_lines))

    gtm = analyst.get("go_to_market", [])
    if gtm:
        lines.append(_section("Go-To-Market", "\n".join(f"  {i+1}. {g}" for i, g in enumerate(gtm))))

    lines.append(_section("CEO Verdict",
        f"Verdict         : {ceo.get('verdict', '')}\n"
        f"Confidence Score: {ceo.get('confidence_score', '')}/10\n"
        f"Key Success Factor: {ceo.get('key_success_factor', '')}"
    ))

    return "\n".join(str(l) for l in lines)


def build_prd(ctx: dict) -> str:
    idea = ctx.get("startup_idea", "")
    pm = ctx.get("pm", {})
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"PRODUCT REQUIREMENTS DOCUMENT (PRD)",
        f"Generated: {now}",
        f"Product: {idea}",
        "",
        "━" * 60,
        "",
        _section("Problem Statement", pm.get("problem_statement", "")),
        _section("Target User", pm.get("target_user", "")),
        _section("Value Proposition", pm.get("value_proposition", "")),
    ]

    features = pm.get("mvp_features", [])
    if features:
        feat_lines = "\n".join(
            f"  [{f.get('priority', 'P1')}] {f['feature']}\n"
            f"       Description: {f.get('description', '')}\n"
            f"       Effort: {f.get('effort', 'TBD')}"
            for f in features
        )
        lines.append(_section("MVP Features", feat_lines))

    roadmap = pm.get("roadmap", [])
    if roadmap:
        rm_lines = "\n".join(
            f"  {r['phase']} — {r['milestone']}\n" +
            "\n".join(f"    ✓ {d}" for d in r.get("deliverables", []))
            for r in roadmap
        )
        lines.append(_section("90-Day Roadmap", rm_lines))

    metrics = pm.get("success_metrics", [])
    if metrics:
        m_lines = "\n".join(f"  • {m['metric']}: {m['target']}" for m in metrics)
        lines.append(_section("Success Metrics", m_lines))

    oos = pm.get("out_of_scope_v1", [])
    if oos:
        lines.append(_section("Out of Scope (V1)", "\n".join(f"  ✗ {o}" for o in oos)))

    return "\n".join(str(l) for l in lines)


def build_architecture_doc(ctx: dict) -> str:
    idea = ctx.get("startup_idea", "")
    arch = ctx.get("architect", {})
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    ts = arch.get("tech_stack", {})
    stack_lines = "\n".join(f"  {k:20}: {v}" for k, v in ts.items())

    components = arch.get("system_components", [])
    comp_lines = "\n".join(f"  ▸ {c['component']}: {c['purpose']}" for c in components)

    schema = arch.get("database_schema", [])
    schema_lines = "\n".join(
        f"  {t['table']}: ({', '.join(t['key_fields'])})"
        for t in schema
    )

    endpoints = arch.get("api_endpoints", [])
    ep_lines = "\n".join(f"  {e}" for e in endpoints)

    return "\n".join([
        "TECHNICAL ARCHITECTURE DOCUMENT",
        f"Generated: {now}",
        f"Product: {idea}",
        "",
        "━" * 60,
        _section("Tech Stack", stack_lines),
        _section("Architecture Style", arch.get("architecture_style", "")),
        _section("System Components", comp_lines),
        _section("Database Schema", schema_lines),
        _section("API Endpoints", ep_lines),
        _section("Scalability Plan", arch.get("scalability_notes", "")),
        _section("Estimated Infra Cost", arch.get("estimated_monthly_infra_cost", "")),
    ])


def save_report(content: str, filename: str, reports_dir: str = "reports") -> str:
    import os
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
