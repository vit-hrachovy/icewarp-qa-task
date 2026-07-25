# First task: Frontend automation - required

With usage of Selenium/Playwright:
Prepare a code that will automate following test case on given IceWarp instance:

1. Access the login with accessing the hostname received in email.
2. Fill username received in email.
3. Click on “Continue” button.
4. Fill the password received in email.
5. Click on “Sign In” button.
6. WebClient starts loading - wait for the loading process to be finished.
7. Intial page should be Dashboard - if not, make sure the program will access it by clicking its icon in the menu on the left side (first one from the top).
8. Right click wherever on the board.
9. Hover on New -> Click on one of following:
- Documents
- Spreadsheet
- Presentation
10. Enter the name for the file (must be unique, not generic) and click on create.
11. Webdocuments editor is loading.
12. When it fully loaded, close it -> Click on “x” on the top right side.
13. Verify, that the file is on the dashboard.
14. Right click on the file again
15. Click on delete.
16. Confirmation dialogue appears.
17. Confirm the action.
18. Verify the file is no longer on the dashboard.

---

## Technical requirements:
- Your program has to be written in more than one file.
- For #9 the program should run for both options.
- Use classes, methods and functions in your code.
- Each class, method and function must have its own docstring.
- Every test run must generate detailed test report.
- Browser selection is up to you.
- This task needs to have a documentation (readme.md or documentation.html).
- Place your code in github.

## CI/CD Part:

Imagine your test needs to be executed on schedule in a gitlab pipeline.
- Prepare ‘.gitlab-ci.yaml’ file that will execute your test.
- Pipeline needs to have prepared variables – url of the website, address of remote Selenium grid.
- .yaml file has to upload test report into gitlab as artifact.

## Project setup and local test execution using debugger instance

For INITIALS use login name initials.

```
mkdir project/playwright
cd project/playwright
virtualenv .
. bin/activate
pip install pytest-playwright
playwright install
pip install psutil
pip install objgraph
pip install pytest-html

git clone https://github.com/vit-hrachovy/icewarp-qa-task plytest
cd plytest
WEBMAIL_URL='https://...' \
WEBMAIL_EMAIL='aaa@bbb' \
WEBMAIL_PASSWORD='hash' \
INITIALS='AB' \
PWDEBUG=1 pytest --headed --browser firefox --html=report.html task01.py
```

# Second task: API testing -optional

Prepare script, that would authenticate to IceWarpApi to IceWarp server mail.example.com and count all accounts on email domain example.com and log out.

API Documentation: icewarp.com/product/api/ access Maintenance API

IceWarp server has API pointed to mail.example.com/icewarpapi

## Technical requirements:

- Login credentials can not be hardcoded.
- End of the script must return count of accounts on the domain.
- Each response status code from API needs to be verified – Must be ‘200’.
- Verify, that currently logged in user is present in listed users.
  - If such condition is not met, raise exception, that tells which user is missing.  After this possible exception, logout has to be performed anyway.
- IceWarp server does not has to be secured connection destination, which may cause trouble to some usable libraries – Find a way to ignore insecure connection and print information, that connection is not secured.
- Place your code in github.

Usage:

```
ICEWARP_USERNAME='...' ICEWARP_PASSWORD='....'  ./icewarp_account_count.py  --api-url https://mail.example.com/icewarpapi/
```
