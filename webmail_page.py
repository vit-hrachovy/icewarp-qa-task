"""Playwright page object for the IceWarp WebClient workflow."""

import re
from uuid import uuid4

from playwright.sync_api import Page, expect

from settings import WebmailSettings


class WebmailPage:
    """Encapsulate login, dashboard document, and logout interactions."""

    login_heading = "Sign in to WebClient"
    dashboard_selector = '[id="gui.frm_main.filter#D"]'
    dashboard_grid_selector = "div.react-grid-layout"

    def __init__(self, page: Page, settings: WebmailSettings) -> None:
        """Store the Playwright page and the test's Webmail configuration."""

        self.page = page
        self.settings = settings

    def login(self) -> None:
        """Sign in and open the dashboard."""

        self.page.goto(self.settings.url)
        expect(self.page).to_have_title(re.compile("IceWarp WebClient"))
        expect(self.page.locator("h2.o-header__title")).to_contain_text(self.login_heading)
        self.page.locator('input[name="email-address"]').press_sequentially(self.settings.email)
        self.page.locator('button[name="next"]').click()
        self.page.locator('input[name="password"]').press_sequentially(self.settings.password)
        self.page.locator('button[name="next"]').click()
        #expect(self.page.locator('div[role="progressbar"]')).to_be_visible()
        expect(self.page.locator(self.dashboard_selector)).to_be_visible()
        expect(self.page.locator('div[role="progressbar"]')).to_have_count(0)
        self.page.locator(self.dashboard_selector).click()

    def create_and_remove_file(self, document_type: str, extension: str) -> None:
        """Create a uniquely named document, verify it, then delete and verify removal."""

        #filename = f"task01-{uuid4().hex[:8]}"
        filename = f"task01"
        displayed_filename = f"{filename}.{extension}"
        self.page.locator(self.dashboard_grid_selector).click(button="right")
        self.page.get_by_role("menuitem", name="New").hover()
        self.page.get_by_text(document_type, exact=True).click()
        self.page.locator('input[id="gui.gw#name"]').press_sequentially(filename)
        self.page.get_by_role("button", name="Create Document").click()

        expect(self.page.locator('div[id="gui.doc"]')).to_be_visible()
        self.page.locator('div[id="gui.doc#rem"]').click()
        expect(self.page.locator('div[id="gui.doc"]')).to_have_count(0)

        file_entry = self.page.locator("span").filter(has_text=displayed_filename)
        expect(file_entry).to_be_visible()
        file_entry.click(button="right")
        self.page.get_by_text("Delete", exact=True).click()
        expect(self.page.locator('h4:has-text("Delete confirmation")')).to_be_visible()
        self.page.get_by_role("button", name="Delete").click()
        expect(file_entry).to_have_count(0)

    def logout(self) -> None:
        """Sign out and verify that the login heading appears again."""

        self.page.locator("a").filter(has_text=self.settings.initials).click()
        self.page.locator("div.button.logout").click()
        expect(self.page.locator("h2.o-header__title")).to_contain_text(self.login_heading)
