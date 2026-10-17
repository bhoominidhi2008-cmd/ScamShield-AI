"""
test_phase3_app.py — Phase 3 Test Suite
Tests:
- Interactive Verification Checklist (state persistence & cautious safety guidance)
- Family Challenge Simulation Workflow (matching & mismatch detection without leaking answers)
- Incident Report Generator (plain-text compilation with actual findings & zero credentials)
- Reset & Session State Integrity
"""

import time
from streamlit.testing.v1 import AppTest
from report_generator import generate_incident_report


def test_report_generator_direct():
    """Unit test for report_generator.py logic."""
    print("--- Testing report_generator.py directly ---")
    msg = "Hi Mum, broke my phone! Send $450 urgently!"
    analysis = {
        "risk_level": "High",
        "engine": "Gemini 2.5 Flash AI",
        "summary": "Urgent family impersonation detected.",
        "warning_signs": ["Unverified phone number", "Artificial urgency", "Direct transfer request"],
        "verification_steps": ["Call original known phone number", "Ask private shared question"]
    }
    checklist = {
        "chk_known_number": True,
        "chk_payment_confirmed": True,
        "chk_audit_details": False,
        "chk_urgency_recognized": True
    }
    details = {
        "channel": "WhatsApp",
        "sender_id": "+1-555-0199",
        "notes": "Sender claimed phone dropped in water."
    }
    
    report = generate_incident_report(
        message_text=msg,
        analysis_result=analysis,
        checklist_status=checklist,
        incident_details=details,
        challenge_status="Matched (Educational Demo)"
    )

    # Verifications
    assert "SCAMSHIELD AI" in report
    assert "WhatsApp" in report
    assert "+1-555-0199" in report
    assert "Gemini 2.5 Flash AI" in report
    assert "HIGH RISK" in report
    assert "3 of 4 steps completed" in report
    assert "Matched (Educational Demo)" in report
    assert "Zero Credentials Policy" in report
    assert "Completing this checklist does NOT guarantee authentic identity" in report
    
    # Negative assertions (Safety): Ensure no API keys or secret prompts are leaked
    assert "GEMINI_API_KEY" not in report
    assert "does not collect, request, or store passwords" in report.lower()
    
    print("[PASS] Direct report generator tests passed!")


def test_app_phase3_ui():
    """Integration AppTest for Phase 3 UI, checklist, challenge, and report generation."""
    print("--- Starting Phase 3 Streamlit AppTest Suite ---")
    at = AppTest.from_file("app.py", default_timeout=20)
    at.run()
    assert not at.exception, f"Initial load failed: {at.exception}"
    print("[PASS] Initial render without exception")

    # Step 1: Select Scenario A and run analysis
    scen1_btn = at.button[0]
    scen1_btn.click().run()
    assert "Hi Mum" in at.session_state["message_input"]
    
    analyze_btn = [b for b in at.button if "Analyze" in b.label or "Run" in b.label][0]
    analyze_btn.click().run()
    assert not at.exception
    assert at.session_state["last_analysis_result"] is not None
    print("[PASS] Analysis executed; Phase 3 dashboard rendered")

    # Step 2: Checkboxes exist and update
    checkboxes = at.checkbox
    assert len(checkboxes) >= 4, f"Expected 4 checklist checkboxes, found {len(checkboxes)}"
    
    # Toggle first checkbox
    checkboxes[0].check().run()
    assert not at.exception
    assert at.session_state["chk_known_number"] is True
    print("[PASS] Checkbox state preserved across rerun")

    # Toggle all 4 checkboxes to test cautious advisory
    for i in range(4):
        at.checkbox[i].check()
    at.run()
    assert not at.exception
    
    # Check that warning alert exists (advising that 4/4 checks still does not declare authentic)
    warning_elements = [w.value for w in at.warning if "DOES NOT automatically declare" in w.value or "CRITICAL SAFETY ADVISORY" in w.value]
    assert len(warning_elements) > 0, "Expected cautious guidance advisory in at.warning when all 4 checks are marked"
    print("[PASS] Cautious advisory rendered when checklist is fully checked")

    # Step 3: Family Challenge Demo
    challenge_btn = [b for b in at.button if "Verify Challenge" in b.label]
    assert len(challenge_btn) >= 1, "Verify Challenge Response button not found"
    
    # Test Mismatch
    at.session_state["challenge_reply"] = "wrong_answer"
    challenge_btn[0].click().run()
    assert not at.exception
    assert "Mismatch" in at.session_state.get("challenge_status", "")
    print("[PASS] Challenge mismatch properly handled")

    # Test Match
    at.session_state["challenge_reply"] = "Barnaby"
    challenge_btn = [b for b in at.button if "Verify Challenge" in b.label][0]
    challenge_btn.click().run()
    assert not at.exception
    assert "Matched" in at.session_state.get("challenge_status", "")
    print("[PASS] Challenge match properly handled without leaking secrets")

    # Step 4: Incident Report Download button exists
    download_btns = at.download_button
    assert len(download_btns) >= 1, "Download button for incident report not found"
    assert "Incident Report" in download_btns[0].label
    print("[PASS] Incident report download button verified")

    # Step 5: Test Clear functionality resets all Phase 3 states
    clear_btn = [b for b in at.button if "Clear" in b.label][0]
    clear_btn.click().run()
    assert not at.exception
    assert at.session_state["message_input"] == ""
    assert at.session_state["last_analysis_result"] is None
    assert at.session_state["chk_known_number"] is False
    assert at.session_state["challenge_status"] is None
    print("[PASS] Complete reset of all Phase 3 states verified")

    print("--- ALL PHASE 3 TESTS COMPLETED AND PASSED! ---")


if __name__ == "__main__":
    test_report_generator_direct()
    test_app_phase3_ui()
