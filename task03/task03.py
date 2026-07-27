"""Fill-in customer contact form and verify resulting DB entry."""

from playwright.sync_api import Page, expect
from contact_form import ContactForm
from settings import ContactFormSettings


def test_task03(page: Page) -> None:
    """Fill in customer contact form and verify resulting DB entry."""

    form = ContactForm(page, ContactFormSettings.from_environment())
    form.fill()
    form.verify_db()
