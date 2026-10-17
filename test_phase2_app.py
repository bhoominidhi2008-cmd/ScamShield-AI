from streamlit.testing.v1 import AppTest

def test_app_phase2():
    print("--- Starting Comprehensive Phase 2 AppTest Suite ---")
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    assert not at.exception, f"Initial load failed: {at.exception}"
    print("[PASS] Initial app render without exception")

    # Verify Gemini API Key input
    api_inputs = [i for i in at.text_input if "Gemini" in i.label or "API" in i.label]
    assert len(api_inputs) >= 1, "API Key text input not found in sidebar"
    print("[PASS] Gemini API Key input discovered in sidebar")

    # Test Scenario A
    at.button[0].click().run()
    assert "Hi Mum" in at.session_state["message_input"]
    analyze_btn = [b for b in at.button if "Analyze" in b.label or "Run" in b.label][0]
    analyze_btn.click().run()
    assert not at.exception
    print("[PASS] Scenario A threat analysis completed with Phase 2 router")

    # Test Scenario B (re-query button tree)
    at.button[1].click().run()
    analyze_btn = [b for b in at.button if "Analyze" in b.label or "Run" in b.label][0]
    analyze_btn.click().run()
    assert not at.exception
    print("[PASS] Scenario B analysis completed")

    # Test Scenario C (re-query button tree)
    at.button[2].click().run()
    analyze_btn = [b for b in at.button if "Analyze" in b.label or "Run" in b.label][0]
    analyze_btn.click().run()
    assert not at.exception
    print("[PASS] Scenario C analysis completed")

    # Test Empty Input handling
    at2 = AppTest.from_file("app.py", default_timeout=15)
    at2.run()
    analyze_btn2 = [b for b in at2.button if "Analyze" in b.label or "Run" in b.label][0]
    analyze_btn2.click().run()
    assert not at2.exception
    print("[PASS] Empty input handled gracefully")

    # Test Custom Input & Clearing
    at3 = AppTest.from_file("app.py", default_timeout=15)
    at3.run()
    at3.button[0].click().run()
    assert at3.session_state["message_input"] != ""
    clear_btn = [b for b in at3.button if "Clear" in b.label][0]
    clear_btn.click().run()
    assert at3.session_state["message_input"] == ""
    print("[PASS] Clear functionality confirmed")

    print("--- ALL PHASE 2 TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    test_app_phase2()
