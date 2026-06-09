from __future__ import annotations

import time

import streamlit as st

from core.orchestrator import NexusOrchestrator
from tools.llm_client import has_llm
from tools.report_generator import build_business_plan, build_prd, build_architecture_doc

st.set_page_config(
    page_title="NexusAI — Startup Validator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg: #070d1a;
    --panel: rgba(12, 24, 45, 0.80);
    --border: rgba(0, 255, 180, 0.12);
    --accent: #00ffb4;
    --accent2: #7c3aed;
    --text: #e8f0ff;
    --muted: #7a8fb0;
    --success: #00e676;
    --warning: #ffab40;
    --danger: #ff5252;
    --card-bg: rgba(10, 22, 46, 0.85);
}

.stApp {
    background: radial-gradient(ellipse at top, rgba(0,255,180,0.06) 0%, transparent 50%),
                radial-gradient(ellipse at bottom right, rgba(124,58,237,0.08) 0%, transparent 50%),
                linear-gradient(180deg, #040a14 0%, #070d1a 100%);
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: rgba(4, 10, 22, 0.95) !important;
    border-right: 1px solid var(--border);
}

.hero-banner {
    background: linear-gradient(135deg, rgba(0,255,180,0.08), rgba(124,58,237,0.10));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0,255,180,0.1), transparent 70%);
    pointer-events: none;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00ffb4 0%, #7c3aed 60%, #00b4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    color: var(--muted);
    font-size: 1.05rem;
    margin-top: 0.2rem;
}

.score-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.1rem 1rem;
    text-align: center;
    min-height: 130px;
}

.score-label {
    color: var(--muted);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.5rem;
}

.score-value {
    font-size: 2.6rem;
    font-weight: 700;
    line-height: 1.0;
}

.score-sub {
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 0.3rem;
}

.score-green  { color: #00e676; }
.score-yellow { color: #ffab40; }
.score-red    { color: #ff5252; }

.agent-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.65rem;
    transition: border-color 0.3s;
}

.agent-card-active  { border-color: rgba(0,255,180,0.40); }
.agent-card-done    { border-color: rgba(0,230,118,0.30); }
.agent-card-error   { border-color: rgba(255,82,82,0.40); }

.agent-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 600;
    font-size: 1.0rem;
}

.agent-role {
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 0.15rem;
    margin-left: 1.65rem;
}

.agent-msg {
    font-size: 0.85rem;
    margin-top: 0.35rem;
    margin-left: 1.65rem;
    color: var(--muted);
}

.status-dot-wait    { color: var(--muted); }
.status-dot-run     { color: var(--warning); }
.status-dot-done    { color: var(--success); }
.status-dot-error   { color: var(--danger); }

.mvp-chip {
    display: inline-block;
    background: rgba(0,255,180,0.10);
    border: 1px solid rgba(0,255,180,0.22);
    color: #00ffb4;
    border-radius: 999px;
    padding: 0.28rem 0.75rem;
    font-size: 0.8rem;
    margin: 0.25rem 0.2rem;
}

.report-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 0.85rem;
}

.report-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.report-desc {
    color: var(--muted);
    font-size: 0.88rem;
    margin-bottom: 0.7rem;
}

.competitor-chip {
    display: inline-block;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.25);
    color: #c4b5fd;
    border-radius: 12px;
    padding: 0.5rem 0.8rem;
    font-size: 0.8rem;
    margin: 0.25rem;
    vertical-align: top;
    max-width: 180px;
}

.pain-point {
    background: rgba(255,82,82,0.07);
    border-left: 3px solid rgba(255,82,82,0.4);
    padding: 0.55rem 0.8rem;
    border-radius: 0 10px 10px 0;
    margin-bottom: 0.45rem;
    font-size: 0.9rem;
    color: var(--text);
}

.roadmap-phase {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
}

.roadmap-phase-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--accent);
    margin-bottom: 0.3rem;
}

.roadmap-milestone {
    font-weight: 700;
    font-size: 1.0rem;
    margin-bottom: 0.35rem;
}

.code-block {
    background: rgba(0,0,0,0.5);
    border: 1px solid rgba(0,255,180,0.15);
    border-radius: 12px;
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #a8ffde;
    overflow-x: auto;
    white-space: pre;
    max-height: 420px;
    overflow-y: auto;
}

.verdict-badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.88rem;
    letter-spacing: 0.04em;
}

.verdict-strong    { background: rgba(0,230,118,0.15); color: #00e676; border: 1px solid rgba(0,230,118,0.3); }
.verdict-promising { background: rgba(255,171,64,0.15); color: #ffab40; border: 1px solid rgba(255,171,64,0.3); }
.verdict-risky     { background: rgba(255,82,82,0.15); color: #ff5252; border: 1px solid rgba(255,82,82,0.3); }

.stButton > button {
    background: linear-gradient(135deg, #00ffb4, #7c3aed) !important;
    color: #040a14 !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.6rem !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px);
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(10, 22, 46, 0.9) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--muted) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,255,180,0.12) !important;
    color: var(--accent) !important;
    border-color: rgba(0,255,180,0.3) !important;
}

[data-testid="stExpander"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def _score_color(score: float) -> str:
    if score >= 7.5:
        return "score-green"
    if score >= 5.5:
        return "score-yellow"
    return "score-red"


def _verdict_class(verdict: str) -> str:
    v = (verdict or "").lower()
    if "strong" in v:
        return "verdict-strong"
    if "risk" in v:
        return "verdict-risky"
    return "verdict-promising"


def render_score_card(label: str, value: float, note: str = "/ 10"):
    color = _score_color(value)
    st.markdown(
        f"""<div class="score-card">
          <div class="score-label">{label}</div>
          <div class="score-value {color}">{value}</div>
          <div class="score-sub">{note}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_agent_card(status, is_current: bool = False):
    card_cls = {
        "waiting": "",
        "running": "agent-card-active",
        "done": "agent-card-done",
        "error": "agent-card-error",
    }.get(status.status, "")

    dot = {
        "waiting": "⬜",
        "running": "🟡",
        "done": "✅",
        "error": "❌",
    }.get(status.status, "⬜")

    st.markdown(
        f"""<div class="agent-card {card_cls}">
          <div class="agent-header">{dot} {status.emoji} {status.name}</div>
          <div class="agent-role">{status.role}</div>
          <div class="agent-msg">{status.message}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def page_dashboard():
    st.markdown(
        """<div class="hero-banner">
          <div class="hero-title">🚀 NexusAI</div>
          <div class="hero-subtitle">
            Multi-Agent Startup Validator — Drop your idea, get a full business plan, tech architecture,
            MVP roadmap, and starter code in under 60 seconds.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    if has_llm():
        st.success("LLM connected — agents will use AI-generated analysis.", icon="🤖")
    else:
        st.info(
            "Running in **Smart Offline Mode** (no API key). "
            "Add `GROQ_API_KEY` or `GEMINI_API_KEY` to `.env` for AI-powered analysis.",
            icon="⚡",
        )

    idea = st.text_area(
        "Describe your startup idea",
        placeholder="e.g. AI-powered Interview Preparation Platform for software engineers",
        height=90,
        key="startup_idea_input",
    )

    col_btn, col_example = st.columns([1, 3])
    with col_btn:
        validate_clicked = st.button("⚡ Validate Idea", use_container_width=True)
    with col_example:
        if st.button("Try Example Idea", use_container_width=False):
            st.session_state["startup_idea_input"] = "AI-powered Interview Preparation Platform for software engineers"
            st.rerun()

    if validate_clicked:
        if not idea.strip():
            st.warning("Please enter a startup idea first.")
            return

        st.session_state["results"] = None
        st.session_state["logs"] = []
        st.session_state["idea"] = idea.strip()

        orch = NexusOrchestrator()
        progress_ph = st.empty()
        agents_ph = st.empty()
        status_text = st.empty()

        total = len(orch.agents)
        logs = []

        for i, (agent_name, ctx) in enumerate(orch.run_streaming(idea.strip())):
            pct = int((i + 1) / total * 100)
            progress_ph.progress(pct, text=f"Running {agent_name}...")

            with agents_ph.container():
                cols = st.columns(min(4, len(orch.agents)))
                for j, status in enumerate(orch.agent_statuses):
                    with cols[j % 4]:
                        dot = {"waiting": "⬜", "running": "🟡", "done": "✅", "error": "❌"}.get(status.status, "⬜")
                        st.markdown(f"{dot} **{status.emoji} {status.name.split()[0]}**")

            logs.append({"agent": agent_name, "status": "done", "message": orch.agents[i].status.message})
            status_text.caption(f"✓ {agent_name} completed")

        st.session_state["results"] = ctx
        st.session_state["logs"] = logs
        st.session_state["orchestrator"] = orch

        progress_ph.empty()
        agents_ph.empty()
        status_text.empty()
        st.success("All agents completed! View results below or navigate to Reports.", icon="🎉")
        st.rerun()

    results = st.session_state.get("results")
    if not results:
        st.markdown("---")
        st.markdown("### How it works")
        cols = st.columns(4)
        steps = [
            ("1️⃣", "Enter Idea", "Describe your startup concept in plain English"),
            ("2️⃣", "Agents Activate", "8 specialist AI agents analyse every angle"),
            ("3️⃣", "Validation Scores", "Get market, competition, and feasibility scores"),
            ("4️⃣", "Download Reports", "Business plan, PRD, architecture, and code"),
        ]
        for col, (icon, title, desc) in zip(cols, steps):
            with col:
                st.markdown(
                    f"""<div class="score-card">
                      <div style="font-size:1.8rem">{icon}</div>
                      <div style="font-weight:700;margin:0.4rem 0">{title}</div>
                      <div class="score-sub">{desc}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
        return

    ceo = results.get("ceo", {})
    research = results.get("research", {})
    analyst = results.get("analyst", {})
    sentiment = results.get("sentiment", {})
    pm = results.get("pm", {})
    arch = results.get("architect", {})
    engineer = results.get("engineer", {})

    st.markdown("---")
    st.markdown(f"### Results for: *{st.session_state.get('idea', '')}*")

    verdict = ceo.get("verdict", "Promising")
    verdict_cls = _verdict_class(verdict)
    st.markdown(
        f"""<span class="verdict-badge {verdict_cls}">CEO Verdict: {verdict}</span>
        &nbsp;&nbsp;<span style="color:var(--muted);font-size:0.9rem">
        Confidence: {ceo.get('confidence_score', '')} / 10</span>""",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_score_card("Market Score", research.get("market_demand_score", 7.5))
    with s2:
        render_score_card("Competition", research.get("competition_score", 6.0), "/ 10 (lower = tougher)")
    with s3:
        render_score_card("Feasibility", analyst.get("feasibility_score", 8.0))
    with s4:
        render_score_card("Sentiment", sentiment.get("sentiment_score", 7.0), f"/ 10 ({sentiment.get('overall_sentiment', '')})")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown("#### Strategic Overview")
        st.markdown(
            f"""<div class="agent-card agent-card-done" style="padding:1.1rem">
              {ceo.get('strategic_overview', '')}
            </div>""",
            unsafe_allow_html=True,
        )

        st.markdown("#### Recommended MVP Features")
        mvp_features = pm.get("mvp_features", [])
        if mvp_features:
            chips = "".join(
                f'<span class="mvp-chip">{f["feature"]}</span>'
                for f in mvp_features
            )
            st.markdown(chips, unsafe_allow_html=True)
        else:
            industry = ceo.get("industry", {})
            for feat in industry.get("mvp_features", []):
                st.markdown(f'<span class="mvp-chip">{feat}</span>', unsafe_allow_html=True)

        st.markdown("#### Customer Pain Points")
        for pp in sentiment.get("pain_points", [])[:4]:
            st.markdown(f'<div class="pain-point">⚡ {pp}</div>', unsafe_allow_html=True)

    with right:
        st.markdown("#### Market Snapshot")
        industry = ceo.get("industry", {})
        st.markdown(
            f"""<div class="score-card" style="text-align:left;padding:1rem 1.2rem">
              <div style="margin-bottom:0.5rem">
                <span style="color:var(--muted);font-size:0.8rem">INDUSTRY</span><br>
                <strong>{industry.get('name', '')}</strong>
              </div>
              <div style="margin-bottom:0.5rem">
                <span style="color:var(--muted);font-size:0.8rem">MARKET SIZE</span><br>
                <strong style="color:#00ffb4">{research.get('market_size', industry.get('market_size', ''))}</strong>
              </div>
              <div style="margin-bottom:0.5rem">
                <span style="color:var(--muted);font-size:0.8rem">GROWTH RATE</span><br>
                <strong>{research.get('growth_rate', industry.get('growth_rate', ''))}% CAGR</strong>
              </div>
              <div>
                <span style="color:var(--muted);font-size:0.8rem">BUSINESS MODEL</span><br>
                <strong>{analyst.get('business_model', industry.get('business_model', ''))}</strong>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )

        st.markdown("#### Top Competitors")
        for comp in research.get("competitors", industry.get("competitors", []))[:4]:
            st.markdown(
                f"""<div class="competitor-chip">
                  <strong>{comp['name']}</strong><br>
                  <span style="color:var(--muted)">{comp['stage']}</span><br>
                  <span style="font-size:0.74rem">Gap: {comp['weakness']}</span>
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown("#### Unit Economics")
        ue = analyst.get("unit_economics", {})
        if ue:
            for k, v in ue.items():
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:0.25rem 0;"
                    f"border-bottom:1px solid var(--border)'>"
                    f"<span style='color:var(--muted);font-size:0.83rem'>{k.upper().replace('_',' ')}</span>"
                    f"<strong style='font-size:0.85rem'>{v}</strong></div>",
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 90-Day Roadmap")
    roadmap = pm.get("roadmap", [])
    if roadmap:
        rm_cols = st.columns(len(roadmap))
        for col, phase in zip(rm_cols, roadmap):
            with col:
                deliverables = "".join(f"<li style='color:var(--muted);font-size:0.82rem'>{d}</li>" for d in phase.get("deliverables", []))
                st.markdown(
                    f"""<div class="roadmap-phase">
                      <div class="roadmap-phase-label">{phase['phase']}</div>
                      <div class="roadmap-milestone">{phase['milestone']}</div>
                      <ul style='margin:0.35rem 0 0 0;padding-left:1.1rem'>{deliverables}</ul>
                    </div>""",
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Tech Stack")
    ts = arch.get("tech_stack", industry.get("tech_stack", {}))
    ts_cols = st.columns(len(ts))
    for col, (layer, tech) in zip(ts_cols, ts.items()):
        with col:
            st.markdown(
                f"""<div class="score-card" style="min-height:90px">
                  <div class="score-label">{layer.replace('_',' ').upper()}</div>
                  <div style="font-size:0.9rem;font-weight:600;color:var(--text)">{tech}</div>
                </div>""",
                unsafe_allow_html=True,
            )


def page_agent_logs():
    st.markdown(
        """<div class="hero-banner">
          <div class="hero-title">🤖 Agent Activity</div>
          <div class="hero-subtitle">Real-time logs from all 8 specialist agents</div>
        </div>""",
        unsafe_allow_html=True,
    )

    results = st.session_state.get("results")
    orch: NexusOrchestrator | None = st.session_state.get("orchestrator")

    if not results or not orch:
        st.info("No analysis run yet. Go to Dashboard and validate an idea first.")
        return

    for status in orch.agent_statuses:
        render_agent_card(status)

        if status.status == "done" and status.output:
            with st.expander(f"View {status.name} Output", expanded=False):
                _render_agent_detail(status.name, status.output, results)


def _render_agent_detail(name: str, output: dict, results: dict):
    if name == "CEO Agent":
        st.markdown(f"**Strategic Overview:** {output.get('strategic_overview', '')}")
        st.markdown(f"**Verdict:** {output.get('verdict', '')} | **Confidence:** {output.get('confidence_score', '')}/10")
        st.markdown(f"**Key Success Factor:** {output.get('key_success_factor', '')}")
        if output.get("top_risks"):
            st.markdown("**Top Risks:**")
            for r in output["top_risks"]:
                st.markdown(f"- {r}")
        st.markdown("**Task Plan Dispatched:**")
        for task in output.get("task_plan", []):
            st.markdown(f"- **{task['agent']}**: {task['task']}")

    elif name == "Market Research Agent":
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Market Size", output.get("market_size", ""))
            st.metric("Growth Rate", f"{output.get('growth_rate', '')}% CAGR")
        with c2:
            st.metric("Demand Score", f"{output.get('market_demand_score', '')}/10")
            st.metric("Competition", f"{output.get('competition_score', '')}/10")
        st.markdown(f"**Market Gap:** {output.get('market_gap', '')}")
        tam_sam_som = output.get("tam_sam_som", {})
        if tam_sam_som:
            for k, v in tam_sam_som.items():
                st.markdown(f"**{k}**: {v}")
        st.markdown("**Key Trends:**")
        for t in output.get("key_trends", []):
            st.markdown(f"- {t}")

    elif name == "Sentiment Agent":
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Sentiment Score", f"{output.get('sentiment_score', '')}/10")
        with c2:
            st.metric("Overall Sentiment", output.get("overall_sentiment", ""))
        with c3:
            st.metric("WTP", output.get("willingness_to_pay", ""))
        st.markdown("**Pain Points:**")
        for pp in output.get("pain_points", []):
            st.markdown(f'<div class="pain-point">⚡ {pp}</div>', unsafe_allow_html=True)
        st.markdown("**Community Signals:**")
        for sig in output.get("reddit_signals", []):
            st.markdown(f"> {sig}")
        personas = output.get("target_personas", [])
        if personas:
            st.markdown("**Target Personas:**")
            for p in personas:
                st.markdown(f"- **{p['persona']}**: {p['description']} — Pain: *{p['pain']}*")

    elif name == "Business Analyst Agent":
        st.metric("Feasibility Score", f"{output.get('feasibility_score', '')}/10")
        st.markdown(f"**Business Model:** {output.get('business_model', '')}")
        st.markdown(f"**Break-even:** ~{output.get('break_even_months', '')} months")
        st.markdown("**Revenue Streams:**")
        for r in output.get("revenue_streams", []):
            st.markdown(f"- {r['stream']}: {r['price']} ({r['type']})")
        st.markdown("**Go-To-Market:**")
        for g in output.get("go_to_market", []):
            st.markdown(f"- {g}")
        risks = output.get("risks", [])
        if risks:
            st.markdown("**Risks:**")
            for r in risks:
                severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(r.get("severity", "Medium"), "🟡")
                st.markdown(f"{severity_color} **{r['risk']}** — *Mitigation: {r['mitigation']}*")

    elif name == "Technical Architect Agent":
        ts = output.get("tech_stack", {})
        if ts:
            st.markdown("**Tech Stack:**")
            for layer, tech in ts.items():
                st.markdown(f"- **{layer}**: {tech}")
        st.markdown(f"**Architecture Style:** {output.get('architecture_style', '')}")
        st.markdown(f"**Infra Cost:** {output.get('estimated_monthly_infra_cost', '')}")
        st.markdown(f"**Scale Plan:** {output.get('scalability_notes', '')}")
        st.markdown("**API Endpoints:**")
        for ep in output.get("api_endpoints", []):
            st.markdown(f"`{ep}`")

    elif name == "Product Manager Agent":
        st.markdown(f"**Problem:** {output.get('problem_statement', '')}")
        st.markdown(f"**Value Prop:** {output.get('value_proposition', '')}")
        st.markdown(f"**Target User:** {output.get('target_user', '')}")
        st.markdown("**MVP Features:**")
        for f in output.get("mvp_features", []):
            st.markdown(f"- [{f.get('priority', 'P1')}] **{f['feature']}** ({f.get('effort', '')}): {f.get('description', '')}")

    elif name == "Software Engineer Agent":
        st.markdown("**Starter Code:**")
        st.markdown(
            f'<div class="code-block">{output.get("starter_code", "").replace("<","&lt;").replace(">","&gt;")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Repository Structure:**")
        for line in output.get("repo_structure", {}).get("files", []):
            st.markdown(f"`{line}`" if line.strip() else "")
        st.markdown("**Implementation Steps:**")
        for step in output.get("implementation_steps", []):
            st.markdown(f"- {step}")

    elif name == "Documentation Agent":
        tab1, tab2, tab3 = st.tabs(["README", "Deployment Guide", "Pitch Summary"])
        with tab1:
            st.markdown(output.get("readme", ""))
        with tab2:
            st.markdown(output.get("deployment_guide", ""))
        with tab3:
            st.markdown(output.get("pitch_summary", ""))


def page_reports():
    st.markdown(
        """<div class="hero-banner">
          <div class="hero-title">📑 Generated Reports</div>
          <div class="hero-subtitle">Download all deliverables generated by the agent team</div>
        </div>""",
        unsafe_allow_html=True,
    )

    results = st.session_state.get("results")
    if not results:
        st.info("No analysis run yet. Go to Dashboard and validate an idea first.")
        return

    idea = st.session_state.get("idea", "startup")
    safe_name = "".join(c if c.isalnum() else "_" for c in idea[:30]).strip("_")

    pm = results.get("pm", {})
    docs = results.get("docs", {})
    arch = results.get("architect", {})
    engineer = results.get("engineer", {})

    reports = [
        {
            "title": "📊 Business Plan",
            "desc": "Full market analysis, competitive landscape, unit economics, risk register, and go-to-market strategy.",
            "content": build_business_plan(results),
            "filename": f"business_plan_{safe_name}.md",
            "key": "bp",
        },
        {
            "title": "📋 Product Requirements Document (PRD)",
            "desc": "Problem statement, MVP features with priorities and effort, 90-day roadmap, and success metrics.",
            "content": build_prd(results),
            "filename": f"prd_{safe_name}.md",
            "key": "prd",
        },
        {
            "title": "🏗️ Technical Architecture",
            "desc": "Full tech stack, system components, database schema, API endpoint list, and scalability notes.",
            "content": build_architecture_doc(results),
            "filename": f"architecture_{safe_name}.md",
            "key": "arch",
        },
        {
            "title": "📄 README",
            "desc": "Professional README file with overview, quick start guide, env variables, and deployment instructions.",
            "content": docs.get("readme", ""),
            "filename": f"README_{safe_name}.md",
            "key": "readme",
        },
        {
            "title": "🚀 Deployment Guide",
            "desc": "Step-by-step deployment to Railway, Render, and Streamlit Cloud with production checklist.",
            "content": docs.get("deployment_guide", ""),
            "filename": f"deployment_guide_{safe_name}.md",
            "key": "deploy",
        },
        {
            "title": "🎤 Investor Pitch Summary",
            "desc": "One-page pitch with problem, solution, market, business model, and traction targets.",
            "content": docs.get("pitch_summary", ""),
            "filename": f"pitch_summary_{safe_name}.md",
            "key": "pitch",
        },
        {
            "title": "💻 Starter Code",
            "desc": "Production-ready FastAPI + Python starter code with OpenAI integration.",
            "content": engineer.get("starter_code", ""),
            "filename": f"starter_code_{safe_name}.py",
            "key": "code",
        },
    ]

    st.markdown("### Download Individual Reports")
    for report in reports:
        if not report["content"]:
            continue
        st.markdown(
            f"""<div class="report-card">
              <div class="report-title">{report['title']}</div>
              <div class="report-desc">{report['desc']}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns([1, 4])
        with col1:
            st.download_button(
                label="⬇ Download",
                data=report["content"],
                file_name=report["filename"],
                mime="text/plain",
                key=f"dl_{report['key']}",
                use_container_width=True,
            )
        with col2:
            with st.expander("Preview"):
                if report["key"] == "code":
                    st.code(report["content"][:1500], language="python")
                else:
                    st.markdown(report["content"][:1200] + ("\n\n*[truncated — download for full report]*" if len(report["content"]) > 1200 else ""))

    st.markdown("---")
    st.markdown("### Download Full Bundle")
    all_content = "\n\n" + ("=" * 80 + "\n").join(
        [f"\n\n# {r['title']}\n\n{r['content']}" for r in reports if r["content"]]
    )
    st.download_button(
        label="⬇ Download All Reports (Single File)",
        data=all_content,
        file_name=f"nexusai_full_bundle_{safe_name}.md",
        mime="text/plain",
        key="dl_all",
        use_container_width=False,
    )


def main():
    if "results" not in st.session_state:
        st.session_state["results"] = None
    if "logs" not in st.session_state:
        st.session_state["logs"] = []
    if "idea" not in st.session_state:
        st.session_state["idea"] = ""
    if "orchestrator" not in st.session_state:
        st.session_state["orchestrator"] = None

    with st.sidebar:
        st.markdown(
            """<div style="padding:1rem 0.5rem">
              <div style="font-size:1.5rem;font-weight:700;background:linear-gradient(90deg,#00ffb4,#7c3aed);
                          -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                🚀 NexusAI
              </div>
              <div style="color:var(--muted);font-size:0.8rem;margin-top:0.2rem">
                Multi-Agent Startup Validator
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        page = st.radio(
            "Navigate",
            ["Dashboard", "Agent Logs", "Reports"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.markdown(
            """<div style="color:var(--muted);font-size:0.78rem;padding:0.5rem">
              <strong style="color:var(--text)">Agents</strong><br>
              👔 CEO &nbsp;&nbsp; 📊 Research<br>
              💬 Sentiment &nbsp; 📈 Analyst<br>
              🏗️ Architect &nbsp; 📋 PM<br>
              💻 Engineer &nbsp; 📄 Docs
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        llm_status = "🟢 LLM Active" if has_llm() else "⚡ Offline Mode"
        st.caption(llm_status)
        if not has_llm():
            st.caption("Add GROQ_API_KEY to .env for AI-powered analysis")

    if page == "Dashboard":
        page_dashboard()
    elif page == "Agent Logs":
        page_agent_logs()
    elif page == "Reports":
        page_reports()


if __name__ == "__main__":
    main()
