from dataclasses import dataclass
@dataclass
class Address:
    locality: str
    street: str
    city: str
    state: str
    zip_code: str