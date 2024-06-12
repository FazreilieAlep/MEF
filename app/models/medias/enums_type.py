from enum import Enum

class EnumsType(str, Enum):
    GENRE = "genre"
    STATUS = "status"
    SHOW_TYPE = "show_type"
    PREMIER = "premier"
    RATED = "rated"