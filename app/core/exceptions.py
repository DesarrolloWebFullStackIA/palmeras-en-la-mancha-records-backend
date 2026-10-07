from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        error_message = str(exc.orig).lower()

        if "foreign key constraint failed" in error_message:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "Related resource not found. Check that album_id, format_id, or branch_id exists."
                },
            )

        if (
            "check constraint failed" in error_message
            or "ck_album_formats_stock_non_negative" in error_message
        ):
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Stock cannot be negative."
                },
            )

        return JSONResponse(
            status_code=400,
            content={
                "detail": "Database integrity error. A record with conflicting data (such as a duplicate entry) already exists."
            },
        )