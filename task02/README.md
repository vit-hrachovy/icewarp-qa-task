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
ICEWARP_USERNAME='...' \
ICEWARP_PASSWORD='....'  \
./icewarp_account_count.py  --api-url https://mail.example.com/icewarpapi/  [--insecure-tls]
```

