from fastapi import HTTPException, status,Request
from ..client.response import CustomResponse



class CustomHttpException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)



class BadRequestException(CustomHttpException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class NotFoundException(CustomHttpException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class UnauthorizedException(CustomHttpException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code, message)