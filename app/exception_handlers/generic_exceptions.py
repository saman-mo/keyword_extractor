import traceback

from fastapi import status, Request, HTTPException
from fastapi.responses import JSONResponse


async def handle_internal_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": str(exc),
            "trace": traceback.format_exc().split("\n")
        })
