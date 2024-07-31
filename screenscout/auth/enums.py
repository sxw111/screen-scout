from screenscout.enums import ScreenScoutEnum


class UserRole(ScreenScoutEnum):
    OWNER = "Owner"
    MANAGER = "Manager"
    ADMIN = "Admin"
    MEMBER = "Member"
