from datetime import UTC, datetime

MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def recruiting_team(lang: str = "fr", company: str | None = None) -> str:
    """"l'équipe de recrutement de Acme" / "the Acme recruiting team"; without a company name, the plain generic phrase."""
    if company is None:
        from .config import settings
        company = settings.company_name
    if lang == "en":
        return f"the {company} recruiting team" if company else "the recruiting team"
    if not company:
        return "l'équipe de recrutement"
    elided = company[0].lower() in "aeiouyàâéèêîïôû"
    return f"l'équipe de recrutement d'{company}" if elided else f"l'équipe de recrutement de {company}"


def aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


def format_date(dt: datetime | None, lang: str = "fr") -> str:
    if not dt:
        return ""
    d = aware(dt)
    return f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}" if lang == "en" else f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}"
