import detector

def test_detector():
    # Test 1: Family Impersonation + Money -> High Risk
    msg1 = "Hi Mum, broke my phone! Send $500 urgently!"
    res1 = detector.analyze_message(msg1)
    print("Test 1 Result:", res1["risk_level"], "| Engine:", res1["engine"])
    assert res1["risk_level"] == "High", f"Expected High, got {res1['risk_level']}"

    # Test 2: Delivery Link -> Medium Risk
    msg2 = "Your parcel delivery could not be completed. Pay $1.50 fee at https://track.com"
    res2 = detector.analyze_message(msg2)
    print("Test 2 Result:", res2["risk_level"], "| Engine:", res2["engine"])
    assert res2["risk_level"] == "Medium", f"Expected Medium, got {res2['risk_level']}"

    # Test 3: Normal Chat -> Low Risk
    msg3 = "Hey Alex, are we meeting for coffee tomorrow?"
    res3 = detector.analyze_message(msg3)
    print("Test 3 Result:", res3["risk_level"], "| Engine:", res3["engine"])
    assert res3["risk_level"] == "Low", f"Expected Low, got {res3['risk_level']}"

    # Test 4: Empty -> Unknown
    res4 = detector.analyze_message("")
    print("Test 4 Result:", res4["risk_level"], "| Engine:", res4["engine"])
    assert res4["risk_level"] == "Unknown", f"Expected Unknown, got {res4['risk_level']}"

    print("--- ALL DETECTOR TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    test_detector()
