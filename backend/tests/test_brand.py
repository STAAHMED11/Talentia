"""White label: the company name comes from COMPANY_NAME, and nothing breaks (or leaks a default name) without it."""
from backend.app.config import settings
from backend.app.emailtpl import build_html
from backend.app.interview.service import agent_variables, first_message
from backend.app.util import recruiting_team


def test_recruiting_team_phrase():
    assert recruiting_team("fr", "") == "l'équipe de recrutement"
    assert recruiting_team("en", "") == "the recruiting team"
    assert recruiting_team("fr", "Acme") == "l'équipe de recrutement d'Acme"   # vowel: elision
    assert recruiting_team("fr", "Bolt") == "l'équipe de recrutement de Bolt"
    assert recruiting_team("en", "Acme") == "the Acme recruiting team"


def test_brand_endpoint_is_public(client, monkeypatch):
    monkeypatch.setattr(settings, "company_name", "Acme")
    anon = client.application.test_client()          # no session cookie: the login page needs it
    assert anon.get("/api/brand").get_json() == {"company": "Acme"}
    monkeypatch.setattr(settings, "company_name", "")
    assert anon.get("/api/brand").get_json() == {"company": ""}


def test_interview_texts_follow_the_company(monkeypatch):
    monkeypatch.setattr(settings, "company_name", "")
    assert "Acme" not in first_message("Léa", "fr") and "l'équipe de recrutement" in first_message("Léa", "fr")
    monkeypatch.setattr(settings, "company_name", "Acme")
    assert "l'équipe de recrutement d'Acme" in first_message("Léa", "fr")
    assert "the Acme recruiting team" in first_message("Léa", "en")


def test_agent_variables_carry_the_team(monkeypatch):
    class _Job:
        title = "Poste"
    class _C:
        job, profile, lang = _Job(), {"name": "Léa Martin"}, "fr"
    class _Iv:
        language, plan = "fr", {"questions": []}
    monkeypatch.setattr(settings, "company_name", "Bolt")
    assert agent_variables(_C(), _Iv())["recruiting_team"] == "l'équipe de recrutement de Bolt"


def test_email_header_and_footer(monkeypatch):
    monkeypatch.setattr(settings, "company_name", "")
    html_ = build_html("Bonjour")
    assert "Acme" not in html_ and ">Recrutement</td>" in html_ and "à un poste." in html_
    monkeypatch.setattr(settings, "company_name", "Acme")
    html_ = build_html("Bonjour")
    assert "Acme · Recrutement" in html_ and "à un poste chez Acme." in html_
