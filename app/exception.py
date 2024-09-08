class UserNotFoundException(Exception):
    details = "User not found"


class UserNotCorrectPasswordException(Exception):
    details = "Not correct password"


class TokenExpired(Exception):
    details = "Token expired"


class TokenNotCorrect(Exception):
    details = "Token not correct"


class TaskNotFound(Exception):
    details = "Task not found"


