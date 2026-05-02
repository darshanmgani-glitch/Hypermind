"""Custom CSS for HyperMind AI — Premium Dark Theme"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── BASE ── */
html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
.stApp {
    background: linear-gradient(160deg, #0a0a1a 0%, #1a0a2e 30%, #0d1b2a 60%, #0a0a1a 100%);
    min-height: 100vh;
}
/* hide default header/footer */
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { display: none; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1f 0%, #111827 50%, #0d0d1f 100%);
    border-right: 1px solid rgba(139,92,246,0.15);
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] div { color: #c4b5fd !important; }

/* sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(139,92,246,0.08);
    color: #c4b5fd !important;
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 12px;
    padding: 0.65rem 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 6px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    text-align: left;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(59,130,246,0.25));
    border-color: #8b5cf6;
    transform: translateX(6px);
    box-shadow: 0 0 20px rgba(139,92,246,0.15);
}

/* ── HERO CONTAINER ── */
.hero-container {
    text-align: center;
    padding: 1rem 0 0.5rem;
}
.hero-icon {
    font-size: 4rem;
    animation: iconPulse 3s ease-in-out infinite;
    margin-bottom: 0.3rem;
}
@keyframes iconPulse {
    0%, 100% { transform: scale(1); filter: drop-shadow(0 0 8px rgba(192,132,252,0.4)); }
    50% { transform: scale(1.08); filter: drop-shadow(0 0 20px rgba(192,132,252,0.7)); }
}

/* ── TYPOGRAPHY ── */
.hero-title {
    text-align: center;
    font-size: 3.6rem;
    font-weight: 800;
    margin-bottom: 0.1rem;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.hero-letter {
    display: inline-block;
    background: linear-gradient(135deg, #c084fc, #818cf8, #60a5fa, #34d399);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    animation: letterDrop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards,
               gradient-shift 4s ease infinite;
    opacity: 0;
    transform: translateY(-30px);
}
@keyframes letterDrop {
    0% { opacity: 0; transform: translateY(-30px) scale(0.8); filter: blur(4px); }
    60% { opacity: 1; transform: translateY(4px) scale(1.02); filter: blur(0); }
    100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}
@keyframes gradient-shift {
    0%,100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
.hero-sub {
    text-align: center;
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 1.5rem;
    font-weight: 400;
    animation: fadeUp 0.8s ease 1s forwards;
    opacity: 0;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── MODE BADGE ── */
.mode-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white !important;
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3);
    margin-bottom: 1.5rem;
}
.groq-tag {
    display: inline-block;
    background: linear-gradient(135deg, #f97316, #ef4444);
    color: white;
    padding: 0.2rem 0.7rem;
    border-radius: 50px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-left: 8px;
    vertical-align: middle;
}

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    margin: 0.6rem 0;
    backdrop-filter: blur(12px);
    color: #e2e8f0;
    line-height: 1.8;
    transition: all 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(139,92,246,0.35);
    box-shadow: 0 8px 32px rgba(139,92,246,0.1);
    transform: translateY(-2px);
}
.glass-card h4 {
    background: linear-gradient(90deg, #c084fc, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.glass-card p { color: #94a3b8; font-size: 0.88rem; margin: 0; }

/* ── CHAT BUBBLES ── */
.chat-user {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(59,130,246,0.12));
    border-left: 3px solid #8b5cf6;
    border-radius: 4px 16px 16px 4px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    color: #e2e8f0;
    font-size: 0.92rem;
}
.chat-bot {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #34d399;
    border-radius: 4px 16px 16px 4px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    color: #e2e8f0;
    font-size: 0.92rem;
}

/* ── RESULT PANEL ── */
.result-panel {
    background: linear-gradient(135deg, rgba(139,92,246,0.06), rgba(59,130,246,0.04));
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(12px);
    color: #e2e8f0;
    line-height: 1.85;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ── FORM INPUTS ── */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    background: rgba(139,92,246,0.06) !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    transition: border-color 0.3s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.15) !important;
}
.stSelectbox > div > div { background: rgba(139,92,246,0.06) !important; border-radius: 12px !important; }

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: rgba(139,92,246,0.08);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    border: 1px solid rgba(139,92,246,0.15);
}
[data-testid="stMetricValue"] { color: #c084fc !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }

/* ── PRIMARY BUTTONS ── */
.stFormSubmitButton > button, button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.55rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.25) !important;
}
.stFormSubmitButton > button:hover, button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}

/* ── DIVIDERS ── */
hr { border-color: rgba(139,92,246,0.12) !important; }

/* ── STAT PILLS ── */
.stat-pill {
    display: inline-block;
    background: rgba(139,92,246,0.15);
    color: #c084fc;
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 50px;
    padding: 0.15rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 700;
}

/* ── LABELS ── */
.stTextInput label, .stTextArea label, .stNumberInput label,
.stSelectbox label, .stMultiSelect label, .stSlider label,
.stTimeInput label {
    color: #c4b5fd !important;
    font-weight: 500 !important;
}

/* ── MARKDOWN TEXT ── */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
    color: #cbd5e1;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #e2e8f0;
}
.stMarkdown strong { color: #c084fc; }

/* ── TABLES ── */
.stMarkdown table { border-collapse: collapse; width: 100%; }
.stMarkdown th {
    background: rgba(139,92,246,0.15) !important;
    color: #c084fc !important;
    padding: 0.6rem 1rem;
    border: 1px solid rgba(139,92,246,0.2);
}
.stMarkdown td {
    padding: 0.5rem 1rem;
    border: 1px solid rgba(139,92,246,0.1);
    color: #cbd5e1;
}

/* ── CHAT MESSAGES (st.chat_message) ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(139,92,246,0.12);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(139,92,246,0.25);
    box-shadow: 0 4px 20px rgba(139,92,246,0.08);
}
/* User messages — purple accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid #8b5cf6;
    background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(59,130,246,0.06)) !important;
}
/* Assistant messages — green accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 3px solid #34d399;
    background: rgba(255,255,255,0.04) !important;
}
/* Chat message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #e2e8f0 !important;
    font-size: 0.92rem;
    line-height: 1.7;
}
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
    color: #c4b5fd !important;
    margin-top: 0.8rem;
}
[data-testid="stChatMessage"] strong {
    color: #c084fc !important;
}
[data-testid="stChatMessage"] blockquote {
    border-left: 3px solid #8b5cf6;
    background: rgba(139,92,246,0.06);
    padding: 0.5rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0;
}
[data-testid="stChatMessage"] blockquote p {
    color: #c4b5fd !important;
}
/* Chat tables */
[data-testid="stChatMessage"] table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.5rem 0;
}
[data-testid="stChatMessage"] th {
    background: rgba(139,92,246,0.12) !important;
    color: #c084fc !important;
    padding: 0.5rem 0.8rem;
    border: 1px solid rgba(139,92,246,0.2);
    font-size: 0.85rem;
}
[data-testid="stChatMessage"] td {
    padding: 0.4rem 0.8rem;
    border: 1px solid rgba(139,92,246,0.1);
    color: #cbd5e1;
    font-size: 0.85rem;
}

/* ── RESULT PANEL ENTRANCE ── */
.result-panel {
    animation: fadeSlideIn 0.5s ease-out;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
"""
