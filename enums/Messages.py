from enum import Enum

class Messages(str, Enum):
    ITEM_NOT_FOUND = "Item Not Found"
    NO_ITEMS_FOUND = "No Items Found"

    INVALID_EMAIL = "Invalid Email Format"

    NO_USERS_FOUND = "No Users Found"
    USER_NOT_FOUND = "User Not Found"