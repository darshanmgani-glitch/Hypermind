# ============================================================
#  HYPERMIND AI v3.1 – Groq-Powered Student Assistant
#  Production-Ready Streamlit App
# ============================================================

import streamlit as st
import os, re, html, time, logging, hashlib
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from styles import CSS
from prompts import PROMPTS

load_dotenv()

# ─────────────────────── LOGGING ────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────── PAGE CONFIG ────────────────────────
st.set_page_config(page_title="HyperMind AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────── GROQ CLIENT ───────────────────────
# BUG-02 FIX: Validate key OUTSIDE the cached function to avoid caching st.stop() exceptions.
_api_key = os.getenv("GROQ_API_KEY", "")
if not _api_key:
    st.error("⚠️ GROQ_API_KEY not found in .env file! Please add it and restart.")
    st.stop()

@st.cache_resource
def init_groq(api_key: str):
    return Groq(api_key=api_key)

client = init_groq(_api_key)

# ─────────────────────── RATE LIMITER ──────────────────────
# BUG-03 FIX: Prevent API abuse with per-session cooldown.
RATE_LIMIT_SECONDS = 3

def check_rate_limit() -> bool:
    """Returns True if the request is allowed, False if rate-limited."""
    now = time.time()
    last = st.session_state.get("_last_api_call", 0)
    if now - last < RATE_LIMIT_SECONDS:
        remaining = RATE_LIMIT_SECONDS - (now - last)
        st.warning(f"⏳ Please wait {remaining:.0f}s before sending another request.")
        return False
    st.session_state["_last_api_call"] = now
    return True

# ─────────────────────── AI CALLER ─────────────────────────
def ask_ai(prompt_key: str, user_msg: str) -> str:
    """Send structured prompt + user message to Groq LLaMA 3.3."""
    # BUG-05 FIX: Catch specific exceptions, log errors, don't leak internals.
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": PROMPTS[prompt_key]},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
            max_tokens=1200,
        )
        return r.choices[0].message.content
    except KeyError:
        logger.error(f"Invalid prompt key: {prompt_key}")
        return "⚠️ Configuration error. Please contact support."
    except Exception as e:
        logger.error(f"Groq API error: {e}", exc_info=True)
        return "⚠️ AI is temporarily unavailable. Please try again in a moment."

# ─────────────────────── SESSION STATE ──────────────────────
MAX_HISTORY = 100  # BUG-07 FIX: Cap history to prevent memory leak.

for k, v in [("mode","🏠 Home"), ("history",[]),
             ("stats",{"plans":0,"grades":0,"budgets":0,"decisions":0,"scans":0}),
             ("_counted_results", set())]:  # BUG-08 FIX: Track counted results.
    if k not in st.session_state:
        st.session_state[k] = v

def add_msg(role, text):
    # BUG-07 FIX: Enforce history cap.
    st.session_state.history.append({"role":role, "text":text, "mode":st.session_state.mode})
    if len(st.session_state.history) > MAX_HISTORY:
        st.session_state.history = st.session_state.history[-MAX_HISTORY:]

def truncate_clean(text, max_len=300):
    """BUG-10 FIX: Clean truncation that won't break markdown tables mid-row."""
    clean = re.sub(r'[#|*`>\-]', '', text).strip()
    if len(clean) <= max_len:
        return clean
    truncated = clean[:max_len].rsplit(' ', 1)[0]
    return truncated + "…"

def count_stat(stat_key, result_text):
    """BUG-08 FIX: Only count a result once, even across reruns."""
    result_id = hashlib.md5(result_text.encode()).hexdigest()
    if result_id not in st.session_state._counted_results:
        st.session_state.stats[stat_key] += 1
        st.session_state._counted_results.add(result_id)

def show_history():
    msgs = [m for m in st.session_state.history if m["mode"] == st.session_state.mode][-10:]
    if not msgs:
        return
    st.markdown("---")
    st.markdown("#### 💬 Conversation History")
    for m in msgs:
        if m["role"] == "user":
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(m["text"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(m["text"])

# ─────────────────────── SIDEBAR ────────────────────────────
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:1.2rem 0 0.6rem;'>
        <span style='font-size:3rem;'>🧠</span>
        <h2 style='margin:0.2rem 0 0;background:linear-gradient(90deg,#c084fc,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;color:transparent;'>HyperMind</h2>
        <p style='color:#64748b;font-size:0.78rem;margin:0.2rem 0;'>Supercharge Your Day</p>
        <span class='groq-tag'>⚡ Groq + LLaMA 3.3 70B</span>
    </div>""", unsafe_allow_html=True)
    st.divider()

    nav = {"🏠  Home":"🏠 Home", "📅  Plan My Day":"📅 Plan My Day", "📊  Grade Predictor":"📊 Grade Predictor",
           "💰  Budget Advisor":"💰 Budget Advisor", "🤔  Decision Helper":"🤔 Decision Helper", "🛡️  Scam Checker":"🛡️ Scam Checker"}
    for label, key in nav.items():
        # BUG-19 FIX: Highlight active nav button.
        btn_type = "primary" if st.session_state.mode == key else "secondary"
        if st.button(label, key=f"nav_{key}", type=btn_type):
            st.session_state.mode = key
            st.rerun()

    st.divider()
    st.markdown("**📈 Your Activity**")
    s = st.session_state.stats
    for emoji, label, k in [("📅","Plans","plans"),("📊","Grades","grades"),("💰","Budgets","budgets"),("🤔","Decisions","decisions"),("🛡️","Scans","scans")]:
        st.markdown(f"<span style='color:#94a3b8;font-size:0.82rem;'>{emoji} {label}</span> <span class='stat-pill'>{s[k]}</span>", unsafe_allow_html=True)
    st.divider()
    if st.button("🗑️  Clear Chat", key="clear"):
        st.session_state.history = []
        st.rerun()

# ─────────────────────── HEADER ─────────────────────────────
# Animated letter-by-letter hero title
_hero_letters = ""
_title_text = "HyperMind AI"
for i, ch in enumerate(_title_text):
    if ch == " ":
        _hero_letters += "&nbsp;"
    else:
        _hero_letters += f'<span class="hero-letter" style="animation-delay:{i*0.08}s">{ch}</span>'

st.markdown(f"""
<div class="hero-container">
    <div class="hero-icon">🧠</div>
    <h1 class="hero-title">{_hero_letters}</h1>
    <p class="hero-sub">Supercharge your academics, finance & campus life <span class="groq-tag">⚡ Groq AI</span></p>
</div>
""", unsafe_allow_html=True)
mode = st.session_state.mode
st.markdown(f'<div class="mode-badge">📍 {mode}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  HOME
# ═══════════════════════════════════════════════════════════════
if mode == "🏠 Home":
    cols = st.columns(3)
    cards = [
        ("📅 Plan My Day","Enter tasks → get a smart AI-prioritized schedule with time blocks.", "📅 Plan My Day"),
        ("📊 Grade Predictor","Know exactly what marks you need in finals to hit your target grade.", "📊 Grade Predictor"),
        ("💰 Budget Advisor","Transform your allowance into a daily spending plan + savings tips.", "💰 Budget Advisor"),
    ]
    # BUG-11 FIX: Make home cards clickable with navigation buttons.
    for i, (title, desc, nav_key) in enumerate(cards):
        with cols[i]:
            st.markdown(f'<div class="glass-card"><h4>{title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Open {title.split(' ', 1)[1]}", key=f"card_{nav_key}"):
                st.session_state.mode = nav_key
                st.rerun()

    cols2 = st.columns(2)
    cards2 = [
        ("🤔 Decision Helper","Torn between two choices? Get AI-powered pros/cons + recommendation.", "🤔 Decision Helper"),
        ("🛡️ Scam Checker","Paste any suspicious link or message → instant SAFE / SCAM verdict.", "🛡️ Scam Checker"),
    ]
    for i, (title, desc, nav_key) in enumerate(cards2):
        with cols2[i]:
            st.markdown(f'<div class="glass-card"><h4>{title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Open {title.split(' ', 1)[1]}", key=f"card_{nav_key}"):
                st.session_state.mode = nav_key
                st.rerun()

    st.markdown("---")
    st.markdown("### 💬 Ask HyperMind Anything")
    q = st.text_input("Type your question…", placeholder="e.g. How do I manage exam stress?", key="home_q")
    if st.button("⚡ Send", key="home_send", type="primary") and q.strip():
        if check_rate_limit():
            add_msg("user", q)
            with st.spinner("⚡ Thinking with Groq AI…"):
                resp = ask_ai("home", q)
            add_msg("assistant", resp)
            st.rerun()
    show_history()

# ═══════════════════════════════════════════════════════════════
#  PLAN MY DAY
# ═══════════════════════════════════════════════════════════════
elif mode == "📅 Plan My Day":
    st.markdown("### 📅 Smart Daily Planner")
    st.markdown("*Enter your tasks — AI builds a prioritized, timed schedule.*")
    with st.form("plan"):
        tasks = st.text_area("📝 Tasks (one per line)", placeholder="Math assignment – due today\nRead chapter 5\nGroup meeting – 6 PM\nLaundry\nGym", height=150)
        c1, c2 = st.columns(2)
        with c1:
            wake = st.time_input("⏰ Wake-up", value=datetime.strptime("07:00","%H:%M").time())
        with c2:
            sleep = st.time_input("🌙 Sleep", value=datetime.strptime("23:00","%H:%M").time())
        hours = st.slider("📌 Free hours today", 2, 14, 6)
        go = st.form_submit_button("✨ Generate Schedule", type="primary")
    if go and tasks.strip():
        if check_rate_limit():
            msg = f"Tasks:\n{tasks}\n\nWake: {wake.strftime('%I:%M %p')}, Sleep: {sleep.strftime('%I:%M %p')}, Free hours: {hours}"
            add_msg("user", f"Plan: {tasks.strip().splitlines()[0]}… ({len(tasks.strip().splitlines())} tasks)")
            with st.spinner("🧠 AI is building your schedule…"):
                result = ask_ai("planner", msg)
            # BUG-09 FIX: Single st.markdown call so the div actually wraps the content.
            st.markdown(f'<div class="result-panel">\n\n{result}\n\n</div>', unsafe_allow_html=True)
            n = len([t for t in tasks.strip().splitlines() if t.strip()])
            c1,c2,c3 = st.columns(3)
            c1.metric("📝 Tasks", n); c2.metric("⏳ Free Hrs", hours); c3.metric("⚡ Model", "LLaMA 3.3")
            add_msg("assistant", result)
            count_stat("plans", result)
    elif go:
        st.warning("⚠️ Enter at least one task.")
    show_history()

# ═══════════════════════════════════════════════════════════════
#  GRADE PREDICTOR
# ═══════════════════════════════════════════════════════════════
elif mode == "📊 Grade Predictor":
    st.markdown("### 📊 AI Grade Predictor")
    st.markdown("*Enter your marks — AI predicts your grade and tells you what you need.*")
    with st.form("grade"):
        c1, c2 = st.columns(2)
        with c1:
            internal = st.number_input("📘 Internal Marks", 0.0, 100.0, 35.0, step=0.5)
            int_max = st.number_input("📘 Internal Maximum", 1.0, 100.0, 50.0, step=0.5)
        with c2:
            ext_max = st.number_input("📗 External Maximum", 1.0, 200.0, 100.0, step=0.5)
            passing = st.number_input("🔖 Passing Marks", 0.0, 100.0, 35.0, step=0.5)
        subject = st.text_input("📚 Subject (optional)", placeholder="e.g. Data Structures")
        go = st.form_submit_button("🔮 Predict Grade", type="primary")
    if go:
        # BUG-06 FIX: Validate that internal marks don't exceed the maximum.
        if internal > int_max:
            st.error("⚠️ Internal marks cannot exceed the internal maximum!")
        elif not check_rate_limit():
            pass  # Rate limited — do nothing.
        else:
            msg = f"Subject: {subject or 'General'}\nInternal: {internal}/{int_max}\nExternal max: {ext_max}\nPassing: {passing}"
            add_msg("user", f"Grade: {subject or 'subject'} — {internal}/{int_max}")
            with st.spinner("📐 AI crunching numbers…"):
                result = ask_ai("grade", msg)
            # BUG-09 FIX: Single st.markdown call.
            st.markdown(f'<div class="result-panel">\n\n{result}\n\n</div>', unsafe_allow_html=True)
            pct = (internal/int_max*100) if int_max else 0
            c1,c2,c3 = st.columns(3)
            c1.metric("📘 Internal %", f"{pct:.1f}%"); c2.metric("📗 Ext Max", f"{ext_max:.0f}"); c3.metric("📋 Pass", f"{passing:.0f}")
            add_msg("assistant", result)
            count_stat("grades", result)
    show_history()

# ═══════════════════════════════════════════════════════════════
#  BUDGET ADVISOR
# ═══════════════════════════════════════════════════════════════
elif mode == "💰 Budget Advisor":
    st.markdown("### 💰 Smart Budget Advisor")
    st.markdown("*Enter your budget — AI creates a complete spending plan.*")
    with st.form("budget"):
        c1, c2 = st.columns(2)
        with c1:
            budget = st.number_input("💵 Total Budget (₹)", 100.0, 500000.0, 5000.0, step=100.0)
            period = st.selectbox("📅 Period", ["Weekly (7 days)","Monthly (30 days)","Semester (150 days)"])
        with c2:
            rent = st.number_input("🏠 Rent/Hostel (₹)", 0.0, 200000.0, 0.0, step=100.0)
            fees = st.number_input("📚 Fees/Books (₹)", 0.0, 50000.0, 0.0, step=100.0)
        goal = st.text_input("🎯 Savings Goal (optional)", placeholder="e.g. Laptop, Trip to Goa")
        go = st.form_submit_button("💡 Build Budget", type="primary")
    if go and budget > 0:
        # BUG-21 FIX: Validate rent + fees don't exceed total budget.
        if rent + fees > budget:
            st.error("⚠️ Rent + Fees exceed your total budget! Please adjust the values.")
        elif not check_rate_limit():
            pass
        else:
            msg = f"Budget: ₹{budget:,.0f}, Period: {period}\nRent: ₹{rent:,.0f}, Fees: ₹{fees:,.0f}\nGoal: {goal or 'None'}"
            add_msg("user", f"Budget: ₹{budget:,.0f} ({period})")
            with st.spinner("💸 AI crafting your budget…"):
                result = ask_ai("budget", msg)
            # BUG-09 FIX: Single st.markdown call.
            st.markdown(f'<div class="result-panel">\n\n{result}\n\n</div>', unsafe_allow_html=True)
            days = {"Weekly (7 days)":7,"Monthly (30 days)":30,"Semester (150 days)":150}[period]
            rem = max(0, budget-rent-fees)
            c1,c2,c3 = st.columns(3)
            c1.metric("💵 Total", f"₹{budget:,.0f}"); c2.metric("📅 Daily", f"₹{rem/days:,.0f}"); c3.metric("🏦 Available", f"₹{rem:,.0f}")
            add_msg("assistant", result)
            count_stat("budgets", result)
    elif go:
        st.warning("⚠️ Enter a valid budget.")
    show_history()

# ═══════════════════════════════════════════════════════════════
#  DECISION HELPER
# ═══════════════════════════════════════════════════════════════
elif mode == "🤔 Decision Helper":
    st.markdown("### 🤔 AI Decision Helper")
    st.markdown("*Describe your dilemma — AI gives pros/cons and a recommendation.*")
    with st.form("decide"):
        dilemma = st.text_area("💭 Your dilemma", placeholder="Should I take a CS internship or prepare for GATE?", height=120)
        opt_a = st.text_input("🅰️ Option A", placeholder="e.g. Take the internship")
        opt_b = st.text_input("🅱️ Option B", placeholder="e.g. Prepare for GATE")
        priorities = st.multiselect("⭐ Your priorities",
            ["Career Growth","Work-Life Balance","Financial Gain","Learning","Passion","Family","Security"],
            default=["Career Growth","Learning"])
        go = st.form_submit_button("💡 Help Me Decide", type="primary")
    if go and dilemma.strip():
        if check_rate_limit():
            msg = f"Dilemma: {dilemma}\nOption A: {opt_a or 'Option A'}\nOption B: {opt_b or 'Option B'}\nPriorities: {', '.join(priorities)}"
            add_msg("user", f"Decide: {dilemma[:80]}…")
            with st.spinner("🤔 AI analyzing your options…"):
                result = ask_ai("decision", msg)
            # BUG-09 FIX: Single st.markdown call.
            st.markdown(f'<div class="result-panel">\n\n{result}\n\n</div>', unsafe_allow_html=True)
            add_msg("assistant", result)
            count_stat("decisions", result)
    elif go:
        st.warning("⚠️ Describe your dilemma first.")
    show_history()

# ═══════════════════════════════════════════════════════════════
#  SCAM CHECKER
# ═══════════════════════════════════════════════════════════════
elif mode == "🛡️ Scam Checker":
    st.markdown("### 🛡️ AI Scam Checker")
    st.markdown("*Paste any suspicious link or message — AI analyzes it instantly.*")
    with st.form("scam"):
        # BUG-20 FIX: Limit input length to prevent token waste.
        content = st.text_area("🔗 Paste link or message", placeholder="e.g. Congratulations! You won ₹50,000! Click: http://free-prize.xyz", height=150, max_chars=2000)
        go = st.form_submit_button("🔍 Analyze Now", type="primary")
    if go and content.strip():
        if check_rate_limit():
            add_msg("user", f"Scan: {content[:80]}…")
            with st.spinner("🔎 AI scanning for threats…"):
                result = ask_ai("scam", f"Analyze this message/link:\n\n{content}")
            # BUG-09 FIX: Single st.markdown call.
            st.markdown(f'<div class="result-panel">\n\n{result}\n\n</div>', unsafe_allow_html=True)
            add_msg("assistant", result)
            count_stat("scans", result)
    elif go:
        st.warning("⚠️ Paste a link or message to check.")
    show_history()

# ─────────────────────── FOOTER ─────────────────────────────
st.markdown("---")
st.markdown("""<div style='text-align:center;color:#475569;font-size:0.78rem;padding:0.5rem 0 1.5rem;'>
    🧠 <b>HyperMind AI</b> &nbsp;•&nbsp; Powered by <span style='color:#f97316;font-weight:600;'>Groq + LLaMA 3.3 70B</span>
    &nbsp;•&nbsp; <span style='color:#8b5cf6;'>v3.1 Production</span></div>""", unsafe_allow_html=True)
