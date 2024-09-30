from typing import List


def get_legitimate_emails() -> List[str]:
    return [
        get_email_without_investments(),
        get_email_with_investments(),
    ]


def get_email_with_investments() -> str:
    return "legitimate-user-with-investments@gmail.com"


def get_email_without_investments() -> str:
    return "legitimate-user-without-investments@gmail.com"


def get_scammer_emails() -> List[str]:
    return ["scammer@example.com"]
