from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic_core import ValidationError
from monitoring_backend.di import DependencyContainer
from monitoring_backend.domain.exceptions.base import DomainException
from monitoring_backend.infra.databases.sqlalchemy.connection import init_database

from monitoring_backend.infra.http.exception_handlers import domain_exception_handler, generic_exception_handler, pydantic_validation_error_handler
from monitoring_backend.infra.http.routers import campus, air_conditioner, monitoring_unit

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield

def create_app() -> FastAPI:
    container = DependencyContainer()

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    

    app.container = container
    app.include_router(campus.router)
    app.include_router(air_conditioner.router)
    app.include_router(monitoring_unit.router)

    return app

app = create_app()