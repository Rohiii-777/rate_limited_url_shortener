from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status
from fastapi import HTTPException

def http_error(message: str, code: int):
    return JSONResponse(
        status_code=code,
        content={
            "status": "error",
            "message": message
        }
    )

async def validation_exception_handler(request: Request, exc):
    return http_error("Validation failed", status.HTTP_422_UNPROCESSABLE_ENTITY)

async def generic_500_handler(request: Request, exc):
    return http_error("Something went wrong", status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomHttpException(HTTPException):
    def __init__(self, message: str, status_code: int):
        super().__init__(status_code=status_code, detail=message)