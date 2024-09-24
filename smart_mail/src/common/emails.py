from typing import List


def get_legitimate_emails() -> List[str]:
    return [
        "legitimate-user-without-investments@gmail.com",
        "legitimate-user-with-investments@gmail.com",
    ]


def get_scammer_emails() -> List[str]:
    return ["scammer@example.com"]
