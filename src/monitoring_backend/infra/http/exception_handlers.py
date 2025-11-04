from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from monitoring_backend.domain.exceptions.base import DomainException
from monitoring_backend.application.dto.errors import ErrorDetailDTO, ErrorResponseDTO

import traceback


async def domain_exception_handler(request: Request, exc: DomainException):
    """Handler único para exceções de domínio."""
    error_response = ErrorResponseDTO(
        errors=[
            ErrorDetailDTO(
                field=exc.field,
                message=exc.message,
                code=exc.code,
            )
        ]
    )
    return JSONResponse(
        status_code=400,
        content={
            "errors": [
                {"field": e.field, "message": e.message, "code": e.code}
                for e in error_response.errors
            ]
        },
    )


async def pydantic_validation_error_handler(request: Request, exc: ValidationError):
    """Handler para erros de validação Pydantic."""
    error_response = ErrorResponseDTO(
        errors=[
            ErrorDetailDTO(
                field=err.get("loc")[-1] if "loc" in err else "unknown",
                message=err.get("msg", "Erro de validação"),
                code=err.get("type", "validation_error").upper(),
            )
            for err in exc.errors()
        ]
    )

    return JSONResponse(
        status_code=400,
        content={
            "errors": [
                {"field": e.field, "message": e.message, "code": e.code}
                for e in error_response.errors
            ]
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para erros inesperados."""
    print("❌ Erro inesperado:", repr(exc))
    traceback.print_exc()

    error_response = ErrorResponseDTO(
        errors=[
            ErrorDetailDTO(
                field=None,
                message="Ocorreu um erro interno inesperado.",
                code="INTERNAL_SERVER_ERROR",
            )
        ]
    )
    return JSONResponse(
        status_code=500,
        content={
            "errors": [
                {"field": e.field, "message": e.message, "code": e.code}
                for e in error_response.errors
            ]
        },
    )
