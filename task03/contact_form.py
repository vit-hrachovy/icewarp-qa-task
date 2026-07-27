"""Playwright page object for the IceWarp Homepage Customer Contact Form workflow."""

import re
from uuid import uuid4

from playwright.sync_api import Page, expect
from settings import ContactFormSettings
from db import create_connection, execute_read_query


class ContactForm:
    """Fill and send customer contact form on central IW webpage."""

    def __init__(self, page: Page, settings: ContactFormSettings) -> None:
        """Store the Playwright page and the test's ContactForm configuration."""

        self.page = page
        self.settings = settings

    def fill(self) -> None:
        """Fill in customer contact form."""

        self.page.goto(self.settings.url)
        # check we're on homepage
        expect(self.page).to_have_title("IceWarp® - Business Email Server & Collaboration Hub")
        # open contact form
        self.page.get_by_text("Contact sales").first.click()
        expect(self.page.locator("#sitewide-contact-window")).to_be_visible()
        # fill-in data
        self.page.get_by_placeholder("Number of users *").press_sequentially(self.settings.users)
        self.page.get_by_role("textbox", name="Full name *").press_sequentially(self.settings.name)
        self.page.get_by_role("textbox", name="Email *").press_sequentially(self.settings.email)
        self.page.get_by_role("textbox", name="Phone *").press_sequentially(self.settings.phone)
        self.page.get_by_role("textbox", name="Company *").press_sequentially(self.settings.company)   # Db schema expects role, misses company
        self.page.get_by_role("textbox", name="Message").press_sequentially(self.settings.message)
        # submit
        self.page.get_by_role("button", name="Submit").click()
        # todo - there is a captcha to solve ...
        # verify no error message is present on site
        expect(self.page.locator("#form-error-red")).to_have_count(0)
        # close the customer contact form
        self.page.locator("#sitewide-contact-window").get_by_role("img", name="logotype").click()

    def verify_db(self) -> None:
        """
        Verify customer contact form entries land properly in DB.

        1. Connect to database.
        2. Verify, that all data you filled in contact form are correctly inserted into the database.
        3. Get value of column ‘cust_id’, that has been given to customer.

        DB for this test is simulated through local sqlite file.
        cust_id is printed to test stdout (pytest -s -v)

        Database name: Customer
        Table name: PotentialCustomers
        Columns: 
        - cust_id (numeric unique)
        - cust_name (string)
        - cust_email (string)
        - cust_contact_date (unix timestamp)
        - cust_no_users (numeric)
        - cust_phone_no (numeric 1-9+ digits)
        - cust_role (string)   # missing in the actual input form, company is present instead
        - cust_country (string) # actual input form lists 'Czech Republic', data expects 'Czech'

        """
        #assuming local execution, can be future path-proofed
        conn = create_connection("./customer.sqlite") 

        # focusing on functionality, no input sanitization
        select_cust_id = (
            f"SELECT cust_id FROM PotentialCustomers WHERE cust_name='{self.settings.name}' "
            f"AND cust_email='{self.settings.email}' "
            f"AND cust_contact_date={self.settings.contact_date} "
            f"AND cust_no_users={self.settings.users} "
            f"AND cust_phone_no={self.settings.phone} "
            f"AND cust_country='{self.settings.country}';"
        )
        print(select_cust_id);

        # defined in input form, unused in DB schema:   self.settings.company
        # defined in Db schema, missing in input form:  f"AND where cust_role='{self.settings.role}' "

        cust_ids = execute_read_query(conn, select_cust_id)
        assert len(cust_ids) == 1, "failed to retrieve customer_id for given input"
        for cust_id in cust_ids:
            print(f"Customer uses following customer id:'{cust_id[0]}'")
