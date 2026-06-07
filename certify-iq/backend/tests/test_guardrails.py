import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from responsible_ai.guardrails import ResponsibleAIGuardrails, TRANSPARENCY_NOTE

g = ResponsibleAIGuardrails()


# Input validation tests
def test_rule1_email_blocked():
    r = g.validate_input("My email is test@example.com")
    assert 1 in r["rules_triggered"]


def test_rule2_phone_blocked():
    r = g.validate_input("Call me at 1234567890123")
    assert 2 in r["rules_triggered"]


def test_rule3_ssn_blocked():
    r = g.validate_input("SSN: 123-45-6789")
    assert 3 in r["rules_triggered"]


def test_rule4_length():
    r = g.validate_input("x" * 2001)
    assert 4 in r["rules_triggered"]


def test_rule5_empty():
    r = g.validate_input("")
    assert 5 in r["rules_triggered"]


def test_rule6_sql_injection():
    r = g.validate_input("SELECT * FROM users")
    assert 6 in r["rules_triggered"]


def test_rule7_script_injection():
    r = g.validate_input("<script>alert('xss')</script>")
    assert 7 in r["rules_triggered"]


def test_rule8_credentials():
    r = g.validate_input("password=secret123")
    assert 8 in r["rules_triggered"]


def test_clean_input_passes():
    r = g.validate_input("Alex Chen is studying for AZ-204")
    assert r["safe"] == True
    assert r["rules_triggered"] == []


# Output validation tests
def test_rule11_citation_required():
    r = g.validate_output(
        "This is a recommendation without any citation. Schedule your exam today. "
        "Very specific actionable advice here."
    )
    assert 11 in r["rules_triggered"]


def test_rule12_i_dont_know():
    r = g.validate_output(
        "I don't know the answer. [Source: Test] Schedule practice exams today for better results. " + "x" * 100
    )
    assert 12 in r["rules_triggered"]


def test_rule13_i_cannot():
    r = g.validate_output(
        "I cannot provide that information. [Source: Test] Please schedule your exam today for best results. " + "x" * 100
    )
    assert 13 in r["rules_triggered"]


def test_rule14_too_short():
    r = g.validate_output("Too short")
    assert 14 in r["rules_triggered"]


def test_valid_output_passes():
    r = g.validate_output(
        "Complete the Azure fundamentals module this week. [Source: Engineering Certification Guide] "
        "Schedule practice exams on weekends. Focus on weak areas daily. CertifyIQ recommends targeted study. "
        + "x" * 50
    )
    assert r["grounding_verified"] == True


# Bias detection tests
def test_rule22_gender_language():
    r = g.check_bias(["He should complete the module"])
    assert 22 in r["rules_triggered"]


def test_no_bias_in_clean_text():
    r = g.check_bias(["Complete the module by Friday", "Schedule a practice exam"])
    assert r["bias_detected"] == False


# validate_all tests
def test_validate_all_clean():
    result = g.validate_all(
        "Alex Chen studies AZ-204",
        "Complete Azure App Service module this week. [Source: Engineering Certification Guide] Schedule exam. " + "x" * 100,
        ["Complete the module", "Schedule practice exams"],
    )
    assert "rules_passed_count" in result
    assert result["rules_total"] == 25


def test_validate_all_returns_overall():
    result = g.validate_all(
        "test input valid",
        "test output [Source: Doc] schedule practice exam today review module " + "x" * 100,
        [],
    )
    assert result["overall"] in ["PASS", "WARN", "FAIL"]