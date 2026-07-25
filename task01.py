"""End-to-end test for creating and deleting WebClient files."""

from playwright.sync_api import Page

from settings import WebmailSettings
from webmail_page import WebmailPage


def test_task01(page: Page) -> None:
    """
    Create and delete a document, spreadsheet, and presentation after logging in.

    Minimum viable product. Robustness improvements needed for file name text input speed.
    """

    webmail = WebmailPage(page, WebmailSettings.from_environment())
    webmail.login()
    webmail.create_and_remove_file("Document", "docx")
    webmail.create_and_remove_file("Spreadsheet", "xlsx")
    webmail.create_and_remove_file("Presentation", "pptx")
    webmail.logout()
