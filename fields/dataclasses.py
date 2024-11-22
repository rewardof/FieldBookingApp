from dataclasses import dataclass
from typing import Optional, List

from base.models import District
from user.models import User


@dataclass
class AddressData:
    district: District
    address_line: str = ''
    zipcode: str = ''
    longitude: Optional[float] = None
    latitude: Optional[str] = None


@dataclass
class FootballFieldData:
    owner: Optional[User]
    name: str
    contact_number: str
    hourly_price: int
    width: float
    length: float
    contact_number2: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    address_data: Optional[AddressData] = None
