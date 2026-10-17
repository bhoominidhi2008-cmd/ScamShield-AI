"""
report_generator.py — Plain-Text Incident Documentation Generator
Phase 3: Incident Report Export Engine

Generates standardized, plain-text incident reports combining:
- The actual verbatim suspicious message
- Actual detector threat results (Gemini AI or Heuristic)
- The user's verification checklist state
- Voluntarily supplied incident metadata
- Family challenge demonstration status (without exposing private answers)

SAFETY GUARANTEES:
- Does NOT fabricate any findings or detection metrics.
- Excludes all API keys, passwords, OTPs, or sensitive banking credentials.
- Reminds the recipient that checklist completion does NOT certify authenticity.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional


def generate_incident_report(
    message_text: str,
    analysis_result: Dict[str, Any],
    checklist_status: Dict[str, bool],
    incident_details: Dict[str, str],
    challenge_status: Optional[str] = None
) -> str:
    """
    Compiles an incident report as a formatted plain-text document.
    """
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Extract metadata safely
    channel = incident_details.get("channel", "Not specified").strip() or "Not specified"
    sender_id = incident_details.get("sender_id", "Unknown / Not provided").strip() or "Unknown / Not provided"
    notes = incident_details.get("notes", "None provided").strip() or "None provided"

    # Extract detector findings
    risk_level = analysis_result.get("risk_level", "Unknown").upper()
    engine = analysis_result.get("engine", "ScamShield Threat Engine")
    summary = analysis_result.get("summary", "No summary available.")
    warning_signs = analysis_result.get("warning_signs", [])
    verification_steps = analysis_result.get("verification_steps", [])

    # Checklist items & completion count
    chk_known_number = checklist_status.get("chk_known_number", False)
    chk_payment_confirmed = checklist_status.get("chk_payment_confirmed", False)
    chk_audit_details = checklist_status.get("chk_audit_details", False)
    chk_urgency_recognized = checklist_status.get("chk_urgency_recognized", False)

    completed_count = sum([chk_known_number, chk_payment_confirmed, chk_audit_details, chk_urgency_recognized])

    # Family challenge outcome (without leaking secrets)
    challenge_outcome = challenge_status if challenge_status else "Not attempted during this session"

    report_lines = [
        "=" * 80,
        "SCAMSHIELD AI — SUSPICIOUS COMMUNICATION INCIDENT REPORT",
        f"Generated Timestamp : {now_utc}",
        "Document Purpose    : Advisory Documentation & Fraud Record",
        "=" * 80,
        "",
        "--- SECTION 1: INCIDENT METADATA ---",
        f"Communication Channel : {channel}",
        f"Sender Identifier     : {sender_id}",
        f"Recipient Action      : Report generated prior to authorizing funds transfer",
        f"Additional Context    : {notes}",
        "",
        "--- SECTION 2: SUSPICIOUS MESSAGE CONTENT (VERBATIM) ---",
        "\"\"\"",
        message_text.strip(),
        "\"\"\"",
        "",
        "--- SECTION 3: AUTOMATED THREAT ASSESSMENT ---",
        f"Detection Engine  : {engine}",
        f"Assessed Risk     : {risk_level} RISK",
        f"Executive Summary : {summary}",
        "",
        "Detected Warning Signs:",
    ]

    if warning_signs:
        for idx, sign in enumerate(warning_signs, 1):
            report_lines.append(f"  {idx}. {sign}")
    else:
        report_lines.append("  (None flagged)")

    report_lines.extend([
        "",
        "Recommended Safety Protocol:",
    ])

    if verification_steps:
        for idx, step in enumerate(verification_steps, 1):
            report_lines.append(f"  {idx}. {step}")
    else:
        report_lines.append("  (Standard vigilance advised)")

    report_lines.extend([
        "",
        "--- SECTION 4: RECIPIENT VERIFICATION AUDIT ---",
        f"Verification Progress: {completed_count} of 4 steps completed",
        "",
        f"  [{'X' if chk_known_number else ' '}] 1. Placed independent voice call to sender's previously known, trusted number",
        f"  [{'X' if chk_payment_confirmed else ' '}] 2. Verbally/visually confirmed the legitimate emergency reason",
        f"  [{'X' if chk_audit_details else ' '}] 3. Cross-referenced recipient bank/UPI/phone details against trusted records",
        f"  [{'X' if chk_urgency_recognized else ' '}] 4. Paused execution on artificial panic, emergency claims, or secrecy demands",
        "",
        "CRITICAL SAFETY ADVISORY:",
        "Completing this checklist does NOT guarantee authentic identity. Attackers frequently",
        "exploit compromised accounts, voice-cloning AI, and pretexting. Never transfer money",
        "if any doubt persists.",
        "",
        "--- SECTION 5: FAMILY CHALLENGE PROTOCOL STATUS ---",
        f"Protocol Status : {challenge_outcome}",
        "Privacy Notice  : Challenge questions, expected answers, and response payloads are strictly",
        "                  excluded from this report to protect confidential family secrets.",
        "",
        "--- SECTION 6: RESPONSIBLE USE & COMPLIANCE NOTICE ---",
        "1. This report is an educational, advisory risk evaluation and does not constitute legal or",
        "   forensic certification.",
        "2. Zero Credentials Policy: ScamShield AI does not collect, request, or store passwords,",
        "   PINs, OTPs, or financial account credentials.",
        "3. If financial loss has occurred, contact your banking institution and local law enforcement",
        "   fraud desk immediately.",
        "=" * 80,
        "END OF INCIDENT REPORT — SCAMSHIELD AI",
        "=" * 80,
    ])

    return "\n".join(report_lines)
