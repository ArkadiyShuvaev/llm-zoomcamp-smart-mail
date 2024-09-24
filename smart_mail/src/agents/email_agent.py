from common.emails import get_legitimate_emails


class EmailAgent:
    def exists(self, email: str) -> bool:
        if email in get_legitimate_emails():
            return True
        return False
