from dataclasses import dataclass


@dataclass
class EmailMessage:
    to_email: str
    full_name: str
    subject: str
    body: str
