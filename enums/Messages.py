from enum import Enum

class Messages(str, Enum):
    NOT_FOUND = "Item Not Found"
    INVALID_EMAIL = "Invalid Email Format"
    NO_USERS_FOUND = "No Users Found"
    NO_ITEMS_FOUND = "No Items Found"