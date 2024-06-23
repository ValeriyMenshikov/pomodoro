class UserNotFoundException(Exception):
    details = "User not found"


class UserNotCorrectPasswordException(Exception):
    details = "Not correct password"
