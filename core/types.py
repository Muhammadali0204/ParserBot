from requests import Session
from typing import Optional, TypedDict, List


class RequestData(TypedDict):
    status: bool
    time_remaining: int
    load_id: int
    total_distance: float
    load_start_date: str
    load_end_date: str
    stops: List[str]
    

class MainData(TypedDict):
    session: Optional[Session]
    data: Optional[List[RequestData]]
