import os
import re
import time

from playwright.sync_api import Page, expect

WEBMAIL_URL = os.environ.get("WEBMAIL_URL")
WEBMAIL_EMAIL = os.environ.get("WEBMAIL_EMAIL")
WEBMAIL_PASSWORD = os.environ.get("WEBMAIL_PASSWORD")
INITIALS = os.environ.get("INITIALS")
login_header="Sign in to WebClient"

def required_setting(name: str, value: str | None) -> str:
    '''Check mandatory shell env input values are defined or raise RuntimeError.'''

    if not value:
        raise RuntimeError(f"Set the {name} environment variable before running this test.")
    return value

def login(page: Page) -> None:
    '''
    Use env variables to log in to the tested instance.

    Mandatory shell env variables are:
    WEBMAIL_URL
    WEBMAIL_EMAIL
    WEBMAIL_PASSWORD
    '''

    url = required_setting("WEBMAIL_URL", WEBMAIL_URL)
    email = required_setting("WEBMAIL_EMAIL", WEBMAIL_EMAIL)
    password = required_setting("WEBMAIL_PASSWORD", WEBMAIL_PASSWORD)

    dashboard='[id="gui.frm_main.filter#D"]'
    avatar_xpath='"a").filter(has_text="'+INITIALS+'")'
    login_title='IceWarp WebClient'

    page.goto(url)

    expect(page).to_have_title(re.compile(login_title))
    expect(page.locator("h2.o-header__title")).to_contain_text(login_header)

    page.locator('input[name="email-address"]').press_sequentially(email)
    page.locator('button[name="next"]').click();

    page.locator('input[name="password"]').press_sequentially(password)
    page.locator('button[name="next"]').click();

    expect(page.locator(dashboard)).to_be_visible()
    page.locator(dashboard).click()

def logout(page: Page) -> None:
    '''
    Log out of the tested instance.

    Mandatory shell env variable is:
    INITIALS - user name initials to click at to get logout dialog

    TBD - improve to avoid initials at all
    '''

    initials = required_setting("INITIALS", INITIALS)

    avatar_button = page.locator("a").filter(has_text=initials)
    avatar_button.click()
    page.locator("div.button.logout").click()
    expect(page.locator("h2.o-header__title")).to_contain_text(login_header)

def create_remove_doc(page: Page, doctype: str, docsuffix: str) -> None:
    '''
    Create and then remove document of specified type.
    Valid inputs for doctype = (Document|Presentation|Spreadsheet)
    Valid inputs for docsuffix = (docs|pptx|xlsx)
    '''

    react_grid_loc='div.react-grid-layout'
    page.locator(react_grid_loc).click(button='right') # right click the react grid
    page.get_by_role("menuitem",name="New").hover()
    page.get_by_text(doctype).click()
    page.locator('input[id="gui.gw#name"]').press_sequentially("sample-doc")
    page.get_by_role("button", name="Create Document").click()

    expect(page.locator('div[id="gui.doc"]')).to_be_visible()
    page.locator('div[id="gui.doc#rem"]').click()
    expect(page.locator('div[id="gui.doc"]')).to_have_count(0) # wait for editor no longer visible
    expect(page.locator('span:has-text("sample-doc.' + docsuffix +'")')).to_be_visible() # wait for new file being visible (pptx/xlsx)
    page.locator('span:has-text("sample-doc.' + docsuffix +'")').click(button='right')
    page.get_by_text("Delete").click()
    expect(page.locator('h4:has-text("Delete confirmation")')).to_be_visible()
    page.get_by_role("button", name="Delete").click()
    expect(page.locator('span:has-text("sample-doc.docx")')).to_have_count(0) # wait for new file no longer visible

def test_task01(page: Page) -> None:
    '''
    Implement QA test task using calls to login/logout methods and parametrized calls to create_remove_doc() method.
    See README.md for details.
    '''
    
    login(page)
    create_remove_doc(page, "Document", "docx")
    create_remove_doc(page, "Spreadsheet", "xlsx")
    create_remove_doc(page, "Presentation", "pptx")
    logout(page)
