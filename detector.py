"""
detector.py — Scam Detection Intelligence Engine
Phase 2: Google Gemini AI Integration with Heuristic Fallback

This module interfaces with the Google Gemini API (via google-genai SDK)
to perform behavioral, psychological, and linguistic fraud analysis on suspicious messages.
If the API is unavailable or an API key is missing, it automatically falls back
to the rule-based heuristic engine to ensure 100% uptime.
"""

import os
import re
import json
import logging
from typing import Optional, List, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env if present
load_dotenv()

# Configure logging
logger = logging.getLogger("ScamShieldDetector")


# ==============================================================================
# 1. STRUCTURED OUTPUT SCHEMA FOR GEMINI AI
# ==============================================================================
class ScamAnalysisSchema(BaseModel):
    """Guarantees strict JSON schema conformance from Gemini models."""
    risk_level: Literal["High", "Medium", "Low"] = Field(
        description="Assessed risk level: High (clear manipulation/impersonation/wire scam), Medium (caution/unverified link/fee), Low (benign/routine chat)"
    )
    summary: str = Field(
        description="A concise 1-2 sentence executive assessment of the threat nature."
    )
    warning_signs: List[str] = Field(
        description="2 to 4 concrete red flags or psychological pressure tactics identified in the text."
    )
    verification_steps: List[str] = Field(
        description="3 to 4 actionable, safe steps the recipient must take before sending money or clicking links."
    )


# ==============================================================================
# 2. HEURISTIC RULE ENGINE (Rock-Solid Fallback & Baseline)
# ==============================================================================
def mock_analyze_message(text: str) -> dict:
    """
    Simulates scam detection using keyword matching and heuristics.
    Preserves exact keys, badge classes, and data structures.
    """
    clean_text = text.strip()
    if not clean_text:
        return {
            "risk_level": "Unknown",
            "badge_class": "badge-medium",
            "icon": "❓",
            "summary": "No content provided to analyze. Please enter a message.",
            "warning_signs": ["Empty input received."],
            "verification_steps": ["Paste a suspicious communication into the inspector to evaluate threat signs."],
            "engine": "Heuristic Engine",
            "engine_note": "Awaiting valid input."
        }

    lower_text = clean_text.lower()
    
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
        "crypto", "bill", "dollars", "upi", "venmo", "bank account", "fee",
        "$", "£", "€", "cash", "send money", "funds"
    ]
    link_keywords = ["http://", "https://", "bit.ly", "click here", "link"]

    def _matches_keyword(target: str, keyword: str) -> bool:
        if keyword in ["$", "£", "€", "http://", "https://"]:
            return keyword in target
        return bool(re.search(r'\b' + re.escape(keyword) + r'\b', target))

    has_impersonation = any(_matches_keyword(lower_text, k) for k in impersonation_keywords)
    has_urgency = any(_matches_keyword(lower_text, k) for k in urgency_keywords)
    has_money = any(_matches_keyword(lower_text, k) for k in money_keywords)
    has_link = any(_matches_keyword(lower_text, k) for k in link_keywords)

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
            ],
            "engine": "Heuristic Engine",
            "engine_note": "Evaluated using built-in fraud pattern matching."
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
            ],
            "engine": "Heuristic Engine",
            "engine_note": "Evaluated using built-in fraud pattern matching."
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
            ],
            "engine": "Heuristic Engine",
            "engine_note": "Evaluated using built-in fraud pattern matching."
        }


# ==============================================================================
# 3. GEMINI AI ANALYSIS PIPELINE
# ==============================================================================
def analyze_with_gemini(text: str, api_key: str) -> dict:
    """
    Invokes Google Gemini with structured Pydantic schema enforcement.
    """
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    system_prompt = (
        "You are an expert fraud investigation and cybersecurity intelligence system specializing in "
        "emergency impersonation and social engineering scam detection (such as 'Hi Mum', fake lost phone tropes, "
        "urgent hospital bailouts, fake delivery fees, and phishing lures).\n\n"
        "Analyze the provided message. Evaluate:\n"
        "1. Impersonation indicators (claims of broken phones, new SIMs, unknown numbers).\n"
        "2. Psychological manipulation (artificial urgency, panic, secrecy, discouragement of normal contact).\n"
        "3. Financial vectors (wire transfers, payment apps, gift cards, crypto, courier fees).\n"
        "4. Legitimate vs fraudulent context.\n\n"
        "Provide: risk level ('High', 'Medium', or 'Low'), a clear executive summary, 2-4 concrete warning signs, "
        "and 3-4 actionable verification steps."
    )

    prompt = f"Analyze this received message for scam and fraud indicators:\n\n\"\"\"\n{text}\n\"\"\""

    # Attempt models in order of capability
    candidate_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    last_err = None

    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=ScamAnalysisSchema,
                    temperature=0.1
                )
            )

            if response and response.text:
                data = json.loads(response.text)
                risk = data.get("risk_level", "Medium")

                badge_mapping = {
                    "High": ("badge-high", "🚨"),
                    "Medium": ("badge-medium", "⚠️"),
                    "Low": ("badge-low", "✅")
                }
                badge_class, icon = badge_mapping.get(risk, ("badge-medium", "⚠️"))

                return {
                    "risk_level": risk,
                    "badge_class": badge_class,
                    "icon": icon,
                    "summary": data.get("summary", "Analysis completed."),
                    "warning_signs": data.get("warning_signs", []),
                    "verification_steps": data.get("verification_steps", []),
                    "engine": f"Gemini AI ({model_name})",
                    "engine_note": "Deep contextual reasoning & linguistic fraud analysis."
                }
        except Exception as e:
            last_err = e
            logger.warning(f"Model {model_name} failed: {e}. Trying next candidate...")
            continue

    # If all models failed, raise the error to trigger heuristic fallback
    raise RuntimeError(f"All Gemini models failed. Last error: {last_err}")


# ==============================================================================
# 4. MASTER ANALYSIS ROUTER
# ==============================================================================
def analyze_message(text: str, api_key: Optional[str] = None) -> dict:
    """
    Main entry point for analysis.
    Checks for API key (argument or GEMINI_API_KEY environment variable).
    Routes to Gemini AI when possible; gracefully falls back to Heuristic Engine on error.
    """
    clean_text = text.strip()
    if not clean_text:
        return mock_analyze_message("")

    # Determine effective API key
    effective_key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()

    if effective_key:
        try:
            return analyze_with_gemini(clean_text, effective_key)
        except Exception as err:
            logger.error(f"Gemini AI analysis error: {err}. Falling back to Heuristics.")
            fallback_res = mock_analyze_message(clean_text)
            fallback_res["engine"] = "Heuristic Fallback"
            fallback_res["engine_note"] = f"Gemini API could not be reached ({str(err)[:60]}...). Rule-based analysis provided."
            return fallback_res
    else:
        # No key available — use Heuristic Engine
        res = mock_analyze_message(clean_text)
        res["engine"] = "Heuristic Engine"
        res["engine_note"] = "Running in Heuristic Mode (No Gemini API key supplied). Enter your API key in the sidebar to activate AI reasoning."
        return res
