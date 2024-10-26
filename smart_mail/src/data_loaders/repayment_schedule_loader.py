from dataclasses import dataclass
from typing import List


@dataclass
class Repayment:
    number: int
    type: str
    gross_amount: str  # in EUR
    net_amount: str   # in EUR
    date: str
    status: str

    @classmethod
    def from_string(cls, number: int, type: str, gross: str, net: str, date: str, status: str):
        return cls(
            number=number,
            type=type,
            gross_amount=gross,
            net_amount=net,
            date=date,
            status=status
        )


class RepaymentScheduleLoader:

    @staticmethod
    def get_repayment_schedule(project_id: str | None) -> List[Repayment]:
        return RepaymentSchedule().get_payments(project_id)


class RepaymentSchedule:
    def __init__(self):
        self.repayments: List[Repayment] = []
        self._initialize_repayments()

    def _initialize_repayments(self):
        # The payment data for the project id "0113C948-C9CE-4A3D-AF99-D66BDEDE7D33"
        payment_data = [
            (1, "Anfangszins", "2,64 €", "2,64 €", "2022-06-30", "Ausgezahlt"),
            (2, "Zahlung 1", "7,00 €", "7,00 €", "2022-06-30", "Ausgezahlt"),
            (3, "Zahlung 2", "14,00 €", "14,00 €", "2022-09-30", "Ausgezahlt"),
            (4, "Zahlung 3", "14,00 €", "14,00 €", "2022-12-31", "Ausgezahlt"),
            (5, "Zahlung 4", "14,00 €", "10,31 €", "2023-03-31", "Ausgezahlt"),
            (6, "Zahlung 5", "14,00 €", "10,31 €", "2023-06-30", "Ausgezahlt"),
            (7, "Zahlung 6", "14,00 €", "10,31 €", "2023-09-30", "Ausgezahlt"),
            (8, "Zahlung 7", "14,00 €", "10,31 €", "2023-12-31", "Ausgezahlt"),
            (9, "Verzugszins", "5,59 €", "4,11 €", "2023-12-31", "Verzug"),
            (10, "Zahlung 8", "14,00 €", "10,31 €", "2024-03-31", "Ausstehend"),
            (11, "Abschlussrate", "1.008,87 €", "1.006,53 €", "2024-05-27", "Ausstehend")
        ]

        for data in payment_data:
            self.repayments.append(Repayment.from_string(*data))

    def get_payments(self, project_id: str | None) -> List[Repayment]:
        if project_id is not None and project_id.upper() == "0113C948-C9CE-4A3D-AF99-D66BDEDE7D33":
            return self.repayments

        return []
