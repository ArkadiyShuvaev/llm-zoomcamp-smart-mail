from typing import List


def get_legitimate_emails() -> List[str]:
    return [
        get_email_without_investments(),
        get_email_with_investments_in_project1(),
        get_email_with_investments_in_project2(),
    ]


def get_email_with_investments_in_project1() -> str:
    return "customer_with_project1@gmail.com"


def get_email_with_investments_in_project2() -> str:
    return "customer_with_project2@gmail.com"


def get_email_without_investments() -> str:
    return "customer_without_investments@gmail.com"


def get_scammer_emails() -> List[str]:
    return ["scammer@example.com"]
