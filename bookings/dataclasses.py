from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fields.models import FootballField
from user.models import User


@dataclass
class BookingData:
    field: FootballField
    user: User
    start_time: datetime
    end_time: Optional[datetime] = None
    total_price: int = 0
    hours: int = 1
