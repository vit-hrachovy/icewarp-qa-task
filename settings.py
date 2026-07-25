"""Configuration models for the IceWarp UI test."""

import os
from dataclasses import dataclass


def required_setting(name: str) -> str:
    """Return a required environment setting or raise a helpful error."""

    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set the {name} environment variable before running this test.")
    return value


@dataclass(frozen=True)
class WebmailSettings:
    """Credentials and target URL needed by the Webmail page object."""

    url: str
    email: str
    password: str
    initials: str

    @classmethod
    def from_environment(cls) -> "WebmailSettings":
        """Build settings from the required GitLab or local environment variables."""

        return cls(
            url=required_setting("WEBMAIL_URL"),
            email=required_setting("WEBMAIL_EMAIL"),
            password=required_setting("WEBMAIL_PASSWORD"),
            initials=required_setting("INITIALS"),
        )
