"""Configuration models for the IceWarp UI webform test."""

import os
from dataclasses import dataclass

def required_setting(name: str) -> str:
    """Return a required environment setting or raise a helpful error."""

    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set the {name} environment variable before running this test.")
    return value

@dataclass(frozen=True)
class ContactFormSettings:
    """Input data needed by the WebForm page object."""

    url: str
    users: str
    name: str
    email: str
    contact_date: str
    country: str
    phone: str
    company: str
    message: str

    @classmethod
    def from_environment(cls) -> "ContactFormSettings":
        """Build settings from the required GitLab or local environment variables."""

        return cls(
            url = required_setting("FORM_URL"),
            users = required_setting("FORM_USERS"),
            name = required_setting("FORM_NAME"),
            email = required_setting("FORM_EMAIL"),
            contact_date = required_setting("FORM_CONTACT_DATE"),
            country = required_setting("FORM_COUNTRY"),
            phone = required_setting("FORM_PHONE"),
            company = required_setting("FORM_COMPANY"),
            message = required_setting("FORM_MESSAGE"),
        )
