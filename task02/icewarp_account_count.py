#!/usr/bin/env python3
"""Count IceWarp accounts on example.com and always close the API session.

Credentials are read from ICEWARP_USERNAME and ICEWARP_PASSWORD, or prompted for
when either variable is absent.  
"""

from __future__ import annotations

import argparse
import getpass
import os
import ssl
import sys
from html import escape
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


#DEFAULT_API_URL = "https://mail.example.com/icewarpapi"
#DEFAULT_DOMAIN = "example.com"

DEFAULT_API_URL = "https://iwqa01.onice.io/icewarpapi"
DEFAULT_DOMAIN = "iwqa01.onice.io"
PAGE_SIZE = 1_000


class IceWarpAPIError(RuntimeError):
    """The IceWarp endpoint could not complete a valid API request."""


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def text_of(element: ET.Element, name: str) -> str | None:
    for child in element.iter():
        if local_name(child) == name:
            return child.text
    return None


def api_error_message(root: ET.Element) -> str:
    message = text_of(root, "message") or text_of(root, "error")
    if message and message.strip():
        return message.strip()

    # IceWarp versions differ in their error payload. Preserve any textual
    # diagnostic/result and root attributes instead of losing it to a generic
    # error, while never echoing the request (which contains the password).
    details = [text.strip() for text in root.itertext() if text.strip()]
    attributes = ", ".join(f"{key}={value}" for key, value in root.attrib.items())
    diagnostic = "; ".join(details)
    if attributes and diagnostic:
        return f"IceWarp returned an API error ({attributes}): {diagnostic}"
    if attributes:
        return f"IceWarp returned an API error ({attributes})"
    if diagnostic:
        return f"IceWarp returned an API error: {diagnostic}"
    return "IceWarp returned an API error without a diagnostic"


def build_request(sid: str | None, command: str, params: str) -> bytes:
    sid_attribute = "" if sid is None else f' sid="{escape(sid, quote=True)}"'
    return (
        f'<iq{sid_attribute}>'
        '<query xmlns="admin:iq:rpc">'
        f"<commandname>{command}</commandname>"
        f"<commandparams>{params}</commandparams>"
        "</query></iq>"
    ).encode("utf-8")


def post_api(
    api_url: str, payload: bytes, insecure_tls: bool, operation: str
) -> ET.Element:
    request = Request(
        api_url,
        data=payload,
        headers={"Content-Type": "application/xml; charset=utf-8"},
        method="POST",
    )
    context = ssl._create_unverified_context() if insecure_tls else None
    try:
        with urlopen(request, timeout=30, context=context) as response:
            if response.status != 200:
                raise IceWarpAPIError(
                    f"{operation}: expected HTTP 200, got {response.status}"
                )
            body = response.read()
    except HTTPError as exc:
        # HTTPError is also a response: its status must be checked explicitly.
        raise IceWarpAPIError(
            f"{operation}: expected HTTP 200, got {exc.code}"
        ) from exc
    except URLError as exc:
        raise IceWarpAPIError(f"{operation}: connection failed: {exc.reason}") from exc

    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        raise IceWarpAPIError(f"{operation}: response was not valid XML") from exc

    if root.get("type", "").lower() == "error":
        raise IceWarpAPIError(f"{operation}: {api_error_message(root)}")
    return root


def authenticate(
    api_url: str, username: str, password: str, insecure_tls: bool
) -> str:
    params = (
        "<authtype>0</authtype>"
        f"<email>{escape(username)}</email>"
        f"<password>{escape(password)}</password>"
        "<digest></digest><persistentlogin>0</persistentlogin>"
    )
    root = post_api(
        api_url,
        build_request(None, "authenticate", params),
        insecure_tls,
        "Authenticate",
    )
    sid = root.get("sid")
    if not sid:
        raise IceWarpAPIError("Authenticate: IceWarp did not return a session ID")
    return sid


def get_logged_in_email(api_url: str, sid: str, insecure_tls: bool) -> str:
    root = post_api(
        api_url,
        build_request(sid, "getsessioninfo", ""),
        insecure_tls,
        "GetSessionInfo",
    )
    email = text_of(root, "email")
    if not email:
        raise IceWarpAPIError("GetSessionInfo: IceWarp did not return the logged-in email")
    print("Logged in as:" + email)
    return email


def account_emails(root: ET.Element) -> Iterable[str]:
    for item in root.iter():
        if local_name(item) != "item":
            continue
        email = text_of(item, "email")
        if email:
            yield email


def list_accounts(api_url: str, sid: str, insecure_tls: bool) -> list[str]:
    emails: list[str] = []
    offset = 0
    while True:
        params = (
            f"<domainstr>{DEFAULT_DOMAIN}</domainstr>"
            # Older IceWarp API builds reject an empty TAccountListFilter.
            # Explicit masks select every account without narrowing by type,
            # service, administrator role, or plan.
            "<filter><namemask>*</namemask><typemask>*</typemask>"
            "<servicemask>*</servicemask><adminmask>*</adminmask>"
            "<planmask>*</planmask></filter>"
            f"<offset>{offset}</offset><count>{PAGE_SIZE}</count>"
        )
        root = post_api(
            api_url,
            build_request(sid, "getaccountsinfolist", params),
            insecure_tls,
            "GetAccountsInfoList",
        )
        page = list(account_emails(root))
        emails.extend(page)
        if len(page) < PAGE_SIZE:
            return emails
        offset += len(page)


def logout(api_url: str, sid: str, insecure_tls: bool) -> None:
    post_api(
        api_url,
        build_request(sid, "logout", ""),
        insecure_tls,
        "Logout",
    )


def credentials() -> tuple[str, str]:
    username = os.environ.get("ICEWARP_USERNAME") or input("IceWarp username: ")
    password = os.environ.get("ICEWARP_PASSWORD") or getpass.getpass("IceWarp password: ")
    if not username or not password:
        raise ValueError("An IceWarp username and password are required")
    return username, password


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--api-url",
        default=os.environ.get("ICEWARP_API_URL", DEFAULT_API_URL),
        help=f"IceWarp API URL (default: {DEFAULT_API_URL})",
    )
    parser.add_argument(
        "--api-domain",
        default=os.environ.get("ICEWARP_DOMAIN", DEFAULT_DOMAIN),
        help=f"IceWarp API URL (default: {DEFAULT_DOMAIN})",
    )
    parser.add_argument(
        "--insecure-tls",
        action="store_true",
        help="do not verify the TLS certificate (only use for a trusted self-signed server)",
    )
    args = parser.parse_args()

    print(f"Domain: '{DEFAULT_DOMAIN}', api url:'{DEFAULT_API_URL}'")
    if args.api_url.lower().startswith("http://"):
        print("WARNING: connection is not secured (using HTTP).", file=sys.stderr)
    elif args.insecure_tls:
        print("WARNING: TLS certificate verification is disabled.", file=sys.stderr)

    username, password = credentials()
    sid = authenticate(args.api_url, username, password, args.insecure_tls)
    primary_error: BaseException | None = None
    try:
        logged_in_email = get_logged_in_email(args.api_url, sid, args.insecure_tls)
        emails = list_accounts(args.api_url, sid, args.insecure_tls)
        if logged_in_email.casefold() not in {email.casefold() for email in emails}:
            raise IceWarpAPIError(
                f"Logged-in user is missing from the {DEFAULT_DOMAIN} account list: "
                f"{logged_in_email}"
            )
        return len(emails)
    except BaseException as exc:
        primary_error = exc
        raise
    finally:
        # This runs even when the required logged-in-user check raises an error.
        try:
            logout(args.api_url, sid, args.insecure_tls)
        except IceWarpAPIError as logout_error:
            if primary_error is None:
                raise
            # Preserve the required missing-user error while still reporting that
            # the Logout response failed the HTTP-200 verification.
            print(f"WARNING: {logout_error}", file=sys.stderr)


if __name__ == "__main__":
    try:
        print(main())
    except (IceWarpAPIError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
