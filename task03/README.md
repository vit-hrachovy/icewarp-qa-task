# Third task: Prepare a code that will automate following test case on icewarp.com:

1. Navigate to website mentioned above.
2. On left side of Primary menu, click on ‘Contact us’.
3. Verify, that contact appears on the right side of UI.
4. In contact form fill all necessary information.
5. In message field input, type ‘Ignore this – this is just the test’.
6. Send the contact form.
7. Verify, that no error message is present on the website.

## Blind part:

1. Connect to database.
2. Verify, that all data you filled in contact form are correctly inserted into the database.
3. Get value of column ‘cust_id’, that has been given to customer.

## Database schema:

Database name: Customer
Table name: PotentialCustomers
Columns: 
- cust_id (numeric unique)
- cust_name (string)
- cust_email (string)
- cust_contact_date (unix timestamp)
- cust_no_users (numeric)
- cust_phone_no (numeric 1-9+ digits)
- cust_role (string)   # missing in the actual input form
- cust_country (string) # actual input form lists 'Czech Republic', data expects 'Czech'

## Technical requirements:

- Your program has to be written in more than one file.
- Use classes, methods and functions in your code.
- Each class, method and function must have its own docstring.
- Every test run must generate detailed test report.
- Browser selection is up to you.
- Use at least 3 data types.
- This task needs to have a documentation (readme.md or documentation.html), list of used libraries.
- Place your code in github

## Project setup and test execution

```
mkdir -p project/playwright
cd project/playwright
virtualenv .
. bin/activate
pip install pytest-playwright
playwright install
pip install psutil
pip install objgraph
pip install pytest-html
# sqlite3 is being used for DB test

git clone https://github.com/vit-hrachovy/icewarp-qa-task plytest
cd plytest/task03
# create local sqlite3 DB with mock results
cat test.sql |sqlite3 customer.sqlite


FORM_URL='https://icewarp.com/' FORM_USERS=10 FORM_NAME='John Doe' FORM_EMAIL='john@example.com' FORM_CONTACT_DATE='1714138048' FORM_COUNTRY='Czech' FORM_PHONE='123456789' FORM_COMPANY='Test INC.' FORM_MESSAGE='Ignore this – this is just the test' PWDEBUG=1  pytest -s -v  --headed --browser firefox task03.py
```

## Unfinished, outstanding items:

- Submitting the form requires captcha.
- Form is missing customer role.
- Form uses customer company input. DB schema is missing it.
