from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    user_id : str
    date : datetime
    title : str
    content : str = ""

    