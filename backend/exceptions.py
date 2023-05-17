from fastapi import HTTPException


class AuthError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

class AuthInvalidLogin(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

class TaskNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Task not found"
        )

class TaskMarked(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Task already marked as completed"
        )

class CodeWait(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Wait for 5 seconds before running the code again."
        )

class AuthUserExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Username already registered",
            headers={"WWW-Authenticate": "Bearer"},
        )

