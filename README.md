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

## Project setup and test execution

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
WEBMAIL_URL='https://...' WEBMAIL_EMAIL='aaa@bbb' WEBMAIL_PASSWORD='hash' INITIALS='AB' PWDEBUG=1 pytest --headed --browser firefox --html=report.html task01.py
