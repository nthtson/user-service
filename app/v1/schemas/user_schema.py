from dataclasses import dataclass
from typing import Optional


@dataclass
class UserUpdateRequest:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
