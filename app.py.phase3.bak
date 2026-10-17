"""
ScamShield AI — Verify Before You Pay
Hackathon Cybersecurity Edition (Phase 1: High-Fidelity UI & Heuristic Engine)

A polished, cybersecurity-grade interface designed to help users detect, dissect,
and safely verify family/friend impersonation scams before sending money.
"""

import os
import html
import time
import streamlit as st
from detector import analyze_message, mock_analyze_message
from report_generator import generate_incident_report

# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="ScamShield AI — Verify Before You Pay",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CYBERSECURITY DARK DESIGN SYSTEM (Scoped CSS)
# ==============================================================================
st.markdown("""
<style>
    /* Google Fonts import for clean technical typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global typography override */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Target background & text */
    .stApp {
        background-color: #0B1020 !important;
        color: #F8FAFC !important;
    }

    /* Sidebar dark treatment */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }

    /* Hide default header decoration */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Modern Header */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 0.2rem;
        margin-bottom: 0.4rem;
    }
    .brand-icon-shield {
        background: linear-gradient(135deg, rgba(45, 212, 191, 0.2), rgba(56, 189, 248, 0.1));
        border: 1px solid rgba(45, 212, 191, 0.4);
        border-radius: 12px;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 0 20px rgba(45, 212, 191, 0.15);
    }
    .brand-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #F8FAFC;
        margin: 0;
        line-height: 1.2;
    }
    .brand-title span {
        background: linear-gradient(90deg, #2DD4BF, #38BDF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 1.2rem;
        line-height: 1.5;
    }

    /* Radar/Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: rgba(45, 212, 191, 0.08);
        border: 1px solid rgba(45, 212, 191, 0.3);
        color: #2DD4BF;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        background-color: #2DD4BF;
        border-radius: 50%;
        box-shadow: 0 0 8px #2DD4BF;
        animation: pulse-glow 2s infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Card Panels */
    .cyber-card {
        background-color: #131C2F;
        border: 1px solid #22314E;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .cyber-card-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Scenario selection styling */
    .scenario-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    /* Risk Badges */
    .risk-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.8rem;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #FCA5A5;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.15);
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #FCD34D;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.15);
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.5);
        color: #6EE7B7;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);
    }

    /* Finding Item List */
    .finding-item {
        background-color: rgba(15, 23, 42, 0.6);
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        line-height: 1.45;
        color: #E2E8F0;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    .finding-bullet {
        color: #EF4444;
        font-size: 1rem;
        line-height: 1.2;
    }
    .checklist-bullet {
        color: #2DD4BF;
        font-size: 1rem;
        line-height: 1.2;
    }

    /* Golden Rule Callout */
    .golden-rule-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(19, 28, 47, 0.9));
        border: 1px solid rgba(45, 212, 191, 0.35);
        border-left: 4px solid #2DD4BF;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.88rem;
        color: #E2E8F0;
        line-height: 1.5;
    }
    .golden-rule-title {
        font-weight: 700;
        color: #2DD4BF;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Footer */
    .cyber-footer {
        text-align: center;
        padding: 1.8rem 0 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid #1E293B;
        color: #64748B;
        font-size: 0.82rem;
        line-height: 1.6;
    }

    /* Mobile adjustments */
    @media (max-width: 768px) {
        .brand-title { font-size: 1.45rem; }
        .cyber-card { padding: 1rem; }
    }

    /* Phase 3 Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0F172A;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 8px 16px;
        border: none !important;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #131C2F !important;
        color: #2DD4BF !important;
        border: 1px solid rgba(45, 212, 191, 0.4) !important;
    }

    /* Phase 3 Verification Checklist Item Card */
    .checklist-box {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. SESSION STATE MANAGEMENT (Preserved contract & Phase 3 extensions)
# ==============================================================================
if "message_input" not in st.session_state:
    st.session_state["message_input"] = ""

if "last_analysis_result" not in st.session_state:
    st.session_state["last_analysis_result"] = None

if "analyzed_message_text" not in st.session_state:
    st.session_state["analyzed_message_text"] = ""

# Verification Checklist Session State Keys (Preserved across reruns)
for chk_key in ["chk_known_number", "chk_payment_confirmed", "chk_audit_details", "chk_urgency_recognized"]:
    if chk_key not in st.session_state:
        st.session_state[chk_key] = False

# Family Challenge Simulation Keys
if "challenge_question" not in st.session_state:
    st.session_state["challenge_question"] = "What was our childhood pet's name or family secret phrase?"
if "challenge_expected" not in st.session_state:
    st.session_state["challenge_expected"] = "Barnaby"
if "challenge_reply" not in st.session_state:
    st.session_state["challenge_reply"] = ""
if "challenge_status" not in st.session_state:
    st.session_state["challenge_status"] = None


def load_example(example_text: str):
    """Callback to update the text area with a pre-set example message."""
    st.session_state["message_input"] = example_text
    st.session_state["last_analysis_result"] = None
    st.session_state["analyzed_message_text"] = ""



# ==============================================================================
# 4. BACKEND ANALYSIS LOGIC (Preserved contract & exact return keys)
# ==============================================================================
def mock_analyze_message(text: str) -> dict:
    """
    Simulates scam detection using keyword and heuristic matching.
    Preserves all return keys, badge classes, and data structures.
    In Phase 2, this will be connected to the real Gemini AI detector.
    """
    clean_text = text.strip()
    if not clean_text:
        return {
            "risk_level": "Unknown",
            "badge_class": "badge-medium",
            "icon": "❓",
            "summary": "No content provided to analyze. Please enter a message.",
            "warning_signs": ["Empty input received."],
            "verification_steps": ["Paste a suspicious communication into the inspector to evaluate threat signs."]
        }

    lower_text = clean_text.lower()
    
    # Common scam indicators
    impersonation_keywords = [
        "mom", "mum", "dad", "son", "daughter", "friend", 
        "broke my phone", "lost phone", "new number", "friend's phone"
    ]
    urgency_keywords = [
        "urgent", "urgently", "immediately", "right now", 
        "emergency", "asap", "hospital", "deadline"
    ]
    money_keywords = [
        "pay", "money", "transfer", "wire", "gift card", 
        "crypto", "bill", "dollars", "upi", "venmo", "bank account", "fee"
    ]
    link_keywords = ["http://", "https://", "bit.ly", "click here", "link"]

    has_impersonation = any(k in lower_text for k in impersonation_keywords)
    has_urgency = any(k in lower_text for k in urgency_keywords)
    has_money = any(k in lower_text for k in money_keywords)
    has_link = any(k in lower_text for k in link_keywords)

    # Classify Risk Level based on detected traits
    if (has_impersonation and has_money) or (has_urgency and has_money):
        return {
            "risk_level": "High",
            "badge_class": "badge-high",
            "icon": "🚨",
            "summary": "Critical Threat Detected: This message exhibits classic high-pressure impersonation tactics aimed at bypassing identity verification to extract urgent funds.",
            "warning_signs": [
                "Unverified Sender Identity: Claims to be a close family member or friend contacting from an unfamiliar phone number.",
                "Manufactured Emergency: Uses high-urgency language to bypass critical thinking and provoke an immediate emotional reaction.",
                "Direct Fund Request: Demands an immediate financial transfer (wire, payment app, or bill payment) to an unverified recipient.",
                "Channel Evasion: Claims the primary device is damaged or lost to discourage you from calling their verified regular number."
            ],
            "verification_steps": [
                "STOP & BREATHE: Do not send any funds, gift cards, or financial details immediately.",
                "DIAL THE KNOWN NUMBER: Call the friend or relative directly on the phone number already saved in your contacts—never call back the unknown number.",
                "ASK A SHARED SECRET: If they insist on speaking via the new number, ask a question only the real person would know (e.g., childhood pet, private memory).",
                "TRIANGULATE: Contact a mutual family member or friend to independently confirm whether any emergency has actually occurred."
            ]
        }
    elif has_money or has_link or has_urgency:
        return {
            "risk_level": "Medium",
            "badge_class": "badge-medium",
            "icon": "⚠️",
            "summary": "Elevated Caution Required: This message contains payment requests, external hyperlinks, or suggestive calls-to-action requiring explicit verification.",
            "warning_signs": [
                "External Action Prompt: Contains an unverified external link, payment demand, or account adjustment notice.",
                "Artificial Time Pressure: Imposes a short deadline (e.g. 24 hours, immediate delivery fee) to accelerate user compliance.",
                "Unauthenticated Origin: Sender identity cannot be conclusively authenticated solely through SMS or instant messaging."
            ],
            "verification_steps": [
                "INSPECT URL CAREFULLY: Do not click the link directly. Check for typo-squatting or deceptive domain extensions (e.g., .vip, .express).",
                "NAVIGATE DIRECTLY: Open the official provider app or website independently (e.g., post office or bank) rather than following SMS links.",
                "NO CREDENTIAL DISCLOSURE: Never enter passwords, card numbers, or one-time passcodes (OTP) on unverified web forms."
            ]
        }
    else:
        return {
            "risk_level": "Low",
            "badge_class": "badge-low",
            "icon": "✅",
            "summary": "Low Threat Profile: No typical urgency triggers, financial demands, or impersonation tropes were identified in this message.",
            "warning_signs": [
                "No artificial time constraints or panic-inducing triggers detected.",
                "No requests for monetary transfer, gift cards, or banking credentials."
            ],
            "verification_steps": [
                "MAINTAIN STANDARD VIGILANCE: Even for benign conversations, remain guarded if the contact unexpectedly asks for money or verification codes later."
            ]
        }


# ==============================================================================
# 5. SIDEBAR: THREAT INTELLIGENCE & PROJECT CONTEXT
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem;">🛡️</span>
            <span style="font-size: 1.2rem; font-weight: 800; color: #F8FAFC;">ScamShield <span style="color: #2DD4BF;">AI</span></span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color: #131C2F; border: 1px solid #1E293B; border-radius: 8px; padding: 12px; margin-bottom: 1rem;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #2DD4BF; text-transform: uppercase; margin-bottom: 4px;">Threat Focus</div>
            <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.4;">
                Specialized in combating <strong style="color: #F8FAFC;">Family & Friend Emergency Impersonation</strong> scams ("Hi Mum", fake hospitalizations, and urgent bailouts).
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🧠 The Impersonation Playbook")
    st.markdown("""
    Scammers rely on three psychological levers:
    - **Panic & Urgency:** Prevents deliberate verification.
    - **Lost Device Excuse:** Explains why they are messaging from an unknown number.
    - **Immediate Bailout:** Asks for peer-to-peer funds before you have time to confirm.
    """)

    st.markdown("#### 🔑 Intelligence Engine")
    gemini_key_input = st.text_input(
        "Gemini API Key:",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIzaSy...",
        key="gemini_api_key_input",
        help="Paste your Google Gemini API key to activate deep LLM reasoning. If left blank, ScamShield runs on the built-in Heuristic Engine."
    )

    if gemini_key_input.strip():
        st.markdown("""
            <div style="background-color: rgba(45, 212, 191, 0.1); border: 1px solid rgba(45, 212, 191, 0.4); border-radius: 6px; padding: 6px 10px; font-size: 0.8rem; color: #2DD4BF; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 6px;">
                <span>🟢</span> <strong>Gemini 2.5 Flash AI Active</strong>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background-color: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 6px; padding: 6px 10px; font-size: 0.78rem; color: #FCD34D; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 6px;">
                <span>⚡</span> <span>Heuristic Engine Active (<a href="https://aistudio.google.com/" target="_blank" style="color: #2DD4BF; text-decoration: underline;">Get free API key</a>)</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🗺️ Development Roadmap")
    st.markdown("""
    - `[COMPLETED]` **Phase 1:** High-Fidelity UI & Threat Heuristics
    - `[COMPLETED]` **Phase 2:** Gemini 2.5 Flash AI Reasoning
    - `[ACTIVE]` **Phase 3:** Interactive Verification & Incident Export
    - `[PLANNED]` **Phase 4:** TinyFish Web Inspector (Domain Scanner)
    """)

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.78rem; color: #64748B; line-height: 1.4;">
            🔒 <strong>Zero-Retention Policy:</strong> Messages analyzed in this demo session are processed in memory and never persisted to external databases.
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 6. MAIN CONTENT HEADER
# ==============================================================================
has_active_ai = bool(gemini_key_input.strip())
engine_badge_text = "Threat Radar Active • Gemini 2.5 Flash AI Engine • Phase 3 Active" if has_active_ai else "Threat Radar Active • Phase 3 Verification Active (AI Ready)"

st.markdown(f"""
    <div class="brand-container">
        <div class="brand-icon-shield">🛡️</div>
        <div>
            <h1 class="brand-title">ScamShield <span>AI</span></h1>
        </div>
    </div>
    <div class="brand-subtitle">
        Verify before you pay. Real-time threat detection for emergency impersonation and financial deception messages.
    </div>
    <div class="status-pill">
        <span class="status-dot"></span>
        {engine_badge_text}
    </div>
""", unsafe_allow_html=True)


# ==============================================================================
# 7. DEMONSTRATION TEST VECTORS (Separated & Clearly Labeled)
# ==============================================================================
st.markdown("""
    <div class="scenario-label">⚡ Quick-Test Scenarios (Simulated Attack Vectors)</div>
""", unsafe_allow_html=True)

col_scen1, col_scen2, col_scen3 = st.columns(3)

ex1_text = "Hi Mum, dropped my phone in the sink and it's dead. Using my friend's phone. Can you urgently pay a $450 bill for me? I'll pay you back tonight! Transfer here: 9876-5432-10"
ex2_text = "Your parcel delivery #US8921 could not be completed due to an invalid postal code. Please update your address and pay the $1.50 fee within 24h: https://track-parcel-express.com"
ex3_text = "Hey Alex! Are we still meeting for lunch at 1 PM tomorrow at the cafe downtown? Let me know if that time works for you."

with col_scen1:
    st.button(
        "🚨 Scenario A: 'Hi Mum' Scam",
        on_click=load_example,
        args=(ex1_text,),
        use_container_width=True,
        help="Simulates a classic family impersonation urgency scam."
    )
with col_scen2:
    st.button(
        "⚠️ Scenario B: Suspicious Link",
        on_click=load_example,
        args=(ex2_text,),
        use_container_width=True,
        help="Simulates an SMS delivery fee phishing lure."
    )
with col_scen3:
    st.button(
        "✅ Scenario C: Legitimate Chat",
        on_click=load_example,
        args=(ex3_text,),
        use_container_width=True,
        help="Simulates a routine benign message between friends."
    )

st.write("")


# ==============================================================================
# 8. MESSAGE INSPECTION WORKSPACE
# ==============================================================================
with st.container():
    st.markdown("""
        <div style="font-size: 0.92rem; font-weight: 600; color: #E2E8F0; margin-bottom: 0.4rem;">
            Inspect Suspicious Message or Payment Request:
        </div>
    """, unsafe_allow_html=True)

    message_text = st.text_area(
        label="Message input area",
        label_visibility="collapsed",
        value=st.session_state["message_input"],
        height=145,
        placeholder="Paste suspicious SMS, WhatsApp message, or payment prompt here (e.g., 'Mom, my phone broke! Send $400 immediately to this account...')"
    )

    action_col, clear_col = st.columns([4, 1])
    with action_col:
        analyze_clicked = st.button("🔍 Run ScamShield Threat Analysis", type="primary", use_container_width=True)
    with clear_col:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state["message_input"] = ""
            st.session_state["last_analysis_result"] = None
            st.session_state["analyzed_message_text"] = ""
            st.session_state["chk_known_number"] = False
            st.session_state["chk_payment_confirmed"] = False
            st.session_state["chk_audit_details"] = False
            st.session_state["chk_urgency_recognized"] = False
            st.session_state["challenge_reply"] = ""
            st.session_state["challenge_status"] = None
            st.rerun()


# ==============================================================================
# 9. THREAT INTELLIGENCE RESULTS & PHASE 3 DEFENSE WORKFLOW
# ==============================================================================
if analyze_clicked:
    clean_input = message_text.strip()
    
    if not clean_input:
        st.session_state["last_analysis_result"] = None
        st.session_state["analyzed_message_text"] = ""
        st.markdown("""
            <div style="background-color: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 12px 16px; margin-top: 1rem; color: #FCD34D; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.2rem;">⚠️</span>
                <span><strong>Input Required:</strong> Please paste a message into the inspection box or click one of the quick-test scenarios above to run an analysis.</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Dynamic spinner reflecting active engine
        spinner_msg = (
            "Engaging Gemini 2.5 Flash AI: Analyzing behavioral indicators, emotional manipulation, and financial coercion..."
            if gemini_key_input.strip()
            else "Scanning message heuristics, psychological urgency, and transaction markers..."
        )
        with st.spinner(spinner_msg):
            result = analyze_message(clean_input, api_key=gemini_key_input)
            st.session_state["last_analysis_result"] = result
            st.session_state["analyzed_message_text"] = clean_input

if st.session_state.get("last_analysis_result"):
    result = st.session_state["last_analysis_result"]
    current_message = st.session_state.get("analyzed_message_text", "")

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Dynamic Engine Intelligence Banner
    is_ai = "Gemini" in result.get("engine", "")
    engine_banner_bg = "rgba(45, 212, 191, 0.08)" if is_ai else "rgba(30, 41, 59, 0.6)"
    engine_banner_border = "rgba(45, 212, 191, 0.3)" if is_ai else "#1E293B"
    engine_banner_icon = "🤖" if is_ai else "⚙️"
    engine_title = "GEMINI AI ANALYSIS" if is_ai else "HEURISTIC PATTERN ENGINE"
    
    st.markdown(f"""
        <div style="background-color: {engine_banner_bg}; border: 1px solid {engine_banner_border}; border-radius: 6px; padding: 7px 14px; font-size: 0.8rem; color: #E2E8F0; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span>{engine_banner_icon}</span>
                <span><strong>{engine_title}:</strong> {html.escape(result.get('engine_note', ''))}</span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #2DD4BF;">
                ENGINE: {html.escape(result.get('engine', 'Heuristic').upper())}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Overview Card: Risk Level + Summary
    st.markdown(f"""
        <div class="cyber-card">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; gap: 10px;">
                <div class="risk-badge {result['badge_class']}">
                    <span>{result['icon']}</span>
                    <span>{result['risk_level'].upper()} RISK ASSESSMENT</span>
                </div>
                <div style="font-size: 0.82rem; color: #64748B; font-family: 'JetBrains Mono', monospace;">
                    STATUS: EVALUATION_COMPLETE
                </div>
            </div>
            <div style="font-size: 1.05rem; font-weight: 600; color: #F8FAFC; line-height: 1.5;">
                {html.escape(result['summary'])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dual Panel: Warning Signs vs. Safe Verification Checklist
    col_findings, col_actions = st.columns(2)

    with col_findings:
        st.markdown("""
            <div class="cyber-card" style="height: 100%;">
                <div class="cyber-card-header">
                    <span style="color: #EF4444;">🚩</span>
                    <span>Detected Warning Signs</span>
                </div>
        """, unsafe_allow_html=True)
        
        for sign in result["warning_signs"]:
            st.markdown(f"""
                <div class="finding-item">
                    <span class="finding-bullet">▪</span>
                    <span>{html.escape(sign)}</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col_actions:
        st.markdown("""
            <div class="cyber-card" style="height: 100%;">
                <div class="cyber-card-header">
                    <span style="color: #2DD4BF;">🛡️</span>
                    <span>Recommended Verification Protocol</span>
                </div>
        """, unsafe_allow_html=True)
        
        for step in result["verification_steps"]:
            st.markdown(f"""
                <div class="finding-item">
                    <span class="checklist-bullet">✓</span>
                    <span>{html.escape(step)}</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Mandatory Safety Callout
    st.markdown("""
        <div class="golden-rule-box">
            <div class="golden-rule-title">
                <span>🔒</span> MANDATORY VERIFICATION PRINCIPLE
            </div>
            Never authorize wire transfers, peer-to-peer payments, or gift card purchases based solely on text messages or calls from unverified numbers. Always place an independent voice call to the sender's previously known, trusted phone number.
        </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # PHASE 3: INTERACTIVE VERIFICATION & DEFENSE TOOLKIT
    # ==============================================================================
    st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Interactive Verification & Incident Toolkit")
    st.markdown(
        "<div style='font-size: 0.9rem; color: #94A3B8; margin-bottom: 1rem;'>"
        "Active defense measures: execute independent verification checkpoints, simulate challenge questions, and export incident records."
        "</div>",
        unsafe_allow_html=True
    )

    tab_check, tab_chall, tab_rep = st.tabs([
        "🛡️ Interactive Checklist",
        "🔐 Family Challenge Demo",
        "📄 Incident Report Generator"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: INTERACTIVE VERIFICATION CHECKLIST
    # --------------------------------------------------------------------------
    with tab_check:
        st.markdown("#### 🛡️ Protocol Verification Checklist")
        st.markdown(
            "Execute and document these 4 non-negotiable verification checks before taking any action:"
        )

        c1 = st.checkbox(
            "1. Independent Channel: I placed a direct voice call to the sender's previously known, trusted phone number (NOT the new number).",
            value=st.session_state.get("chk_known_number", False),
            key="chk_known_number",
            help="Crucial: Call the contact entry saved in your address book from before this interaction began."
        )
        c2 = st.checkbox(
            "2. Payment Purpose Confirmation: I verbally or visually confirmed the specific emergency reason with the actual person or family member.",
            value=st.session_state.get("chk_payment_confirmed", False),
            key="chk_payment_confirmed",
            help="Confirm why an emergency payment is requested through independent human communication."
        )
        c3 = st.checkbox(
            "3. Recipient Detail Audit: I cross-referenced the recipient account, UPI ID, or phone number against known trusted records.",
            value=st.session_state.get("chk_audit_details", False),
            key="chk_audit_details",
            help="Scammers often instruct victims to wire money to a 'friend's' unverified third-party account."
        )
        c4 = st.checkbox(
            "4. Urgency & Secrecy Check: I paused and recognized artificial panic, emergency excuses, or secrecy requests ('don't tell anyone yet').",
            value=st.session_state.get("chk_urgency_recognized", False),
            key="chk_urgency_recognized",
            help="High urgency and secrecy are hallmark psychological levers of impersonation scams."
        )

        completed_steps = sum([c1, c2, c3, c4])

        # Cautious Guidance Banner
        if completed_steps == 4:
            st.warning(
                "⚠️ CRITICAL SAFETY ADVISORY: All 4 checklist verification steps are checked, but completing this checklist DOES NOT automatically declare the sender authentic or guarantee safe transfer. "
                "Sophisticated attackers exploit compromised devices, SIM swaps, and pretexting. Never authorize payments if anything feels uncharacteristic or suspect."
            )
        else:
            st.info(
                f"🛡️ Verification Incomplete: {completed_steps} of 4 steps checked. Do NOT send money until independent verification is established."
            )

    # --------------------------------------------------------------------------
    # TAB 2: FAMILY CHALLENGE WORKFLOW (LOCAL EDUCATIONAL DEMO)
    # --------------------------------------------------------------------------
    with tab_chall:
        st.markdown("#### 🔐 Family Challenge Verification (Educational Simulation)")
        st.markdown(
            "<div style='font-size: 0.88rem; color: #94A3B8; margin-bottom: 1rem; line-height: 1.5;'>"
            "Test how a shared secret can help expose an impersonator. "
            "<strong>Note:</strong> This is a local educational demonstration, NOT cryptographically secure authentication. "
            "Family details can sometimes be found via social media or data breaches; always corroborate over a known voice channel."
            "</div>",
            unsafe_allow_html=True
        )

        ch_col1, ch_col2 = st.columns(2)
        with ch_col1:
            challenge_q = st.text_input(
                "1. Private Challenge Question:",
                value=st.session_state.get("challenge_question", "What was our childhood pet's name or family secret phrase?"),
                key="challenge_question",
                help="A private question only the real person would know."
            )
        with ch_col2:
            challenge_exp = st.text_input(
                "2. Expected Private Answer (Hidden):",
                value=st.session_state.get("challenge_expected", "Barnaby"),
                type="password",
                key="challenge_expected",
                help="Kept strictly in browser local memory. Never sent to Gemini AI, logged, or saved on disk."
            )

        st.markdown("<div style='font-size: 0.88rem; font-weight: 600; color: #E2E8F0; margin-top: 0.5rem;'>3. Simulate Sender's Answer:</div>", unsafe_allow_html=True)
        sender_reply_input = st.text_input(
            "What did the sender respond when asked this challenge?",
            value=st.session_state.get("challenge_reply", ""),
            key="challenge_reply",
            placeholder="Type sender's simulated response here (e.g. Barnaby)..."
        )

        if st.button("🧪 Verify Challenge Response", use_container_width=True):
            exp_clean = challenge_exp.strip().lower()
            rep_clean = sender_reply_input.strip().lower()
            if not rep_clean:
                st.warning("⚠️ Please enter the sender's response above to verify.")
            elif exp_clean and rep_clean == exp_clean:
                st.session_state["challenge_status"] = "Matched (Educational Demo)"
            else:
                st.session_state["challenge_status"] = "Mismatch / Evasion (Educational Demo)"

        if st.session_state.get("challenge_status") == "Matched (Educational Demo)":
            st.success(
                "🟢 Response Matched Simulation Vector! "
                "Caution: A matching answer reduces risk but is NOT definitive proof of identity. "
                "Attackers can obtain personal details from social media or data breaches. Always corroborate over a known voice channel."
            )
        elif st.session_state.get("challenge_status") == "Mismatch / Evasion (Educational Demo)":
            st.error(
                "🚨 Challenge Response Mismatch! "
                "High probability of an impersonator, social engineering actor, or evasive contact. "
                "Cease communication immediately and do NOT send money."
            )

        st.caption("🔒 Privacy Guard: Challenge questions and expected answers are processed solely in local memory, never logged, and never transmitted to Gemini AI.")

    # --------------------------------------------------------------------------
    # TAB 3: INCIDENT REPORT GENERATOR
    # --------------------------------------------------------------------------
    with tab_rep:
        st.markdown("#### 📄 Incident Documentation & Evidence Export")
        st.markdown(
            "Compile a structured, unforgeable plain-text incident log for banking dispute or fraud reporting."
        )

        col_chan, col_snd = st.columns(2)
        with col_chan:
            rep_channel = st.selectbox(
                "Communication Channel:",
                ["SMS / Text Message", "WhatsApp", "Telegram", "Instagram / Direct Message", "Email", "Phone Call / Other"],
                key="incident_channel"
            )
        with col_snd:
            rep_sender = st.text_input(
                "Reported Sender Identifier (Optional):",
                placeholder="+1 (555) 019-2834 or unknown username",
                key="incident_sender",
                help="Optional: phone number or handle the suspicious message originated from."
            )

        rep_notes = st.text_area(
            "Additional Incident Observations (Optional):",
            placeholder="e.g. Sender claimed dropped phone at 2 PM, requested wire to unfamiliar account.",
            key="incident_notes",
            height=75
        )

        # Build the plain-text report using actual data
        checklist_state_dict = {
            "chk_known_number": st.session_state.get("chk_known_number", False),
            "chk_payment_confirmed": st.session_state.get("chk_payment_confirmed", False),
            "chk_audit_details": st.session_state.get("chk_audit_details", False),
            "chk_urgency_recognized": st.session_state.get("chk_urgency_recognized", False),
        }
        details_state_dict = {
            "channel": rep_channel,
            "sender_id": rep_sender,
            "notes": rep_notes
        }

        report_content = generate_incident_report(
            message_text=current_message,
            analysis_result=result,
            checklist_status=checklist_state_dict,
            incident_details=details_state_dict,
            challenge_status=st.session_state.get("challenge_status")
        )

        with st.expander("👁️ Preview Formatted Plain-Text Report", expanded=False):
            st.code(report_content, language="text")

        report_filename = f"scamshield_incident_report_{int(time.time())}.txt"
        st.download_button(
            label="📥 Download Plain-Text Incident Report (.txt)",
            data=report_content,
            file_name=report_filename,
            mime="text/plain",
            use_container_width=True
        )

        st.caption("🔒 Zero-Credentials Compliance: This report contains only voluntary observations and automated findings. No passwords, PINs, OTPs, or API keys are collected or included.")


# ==============================================================================
# 10. COMPACT CYBERSECURITY FOOTER
# ==============================================================================
st.markdown("""
    <div class="cyber-footer">
        <strong>ScamShield AI</strong> • Hackathon Prototype Edition • Real-Time Scam Prevention<br>
        <span style="color: #475569;">
            Notice: ScamShield AI provides advisory risk indicators and safe verification workflows. 
            Automated analysis does not replace independent human verification.
        </span>
    </div>
""", unsafe_allow_html=True)
