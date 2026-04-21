from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError as PydanticValidationError
from bot.exceptions import BinanceAPIError, ValidationError
from .routes import router
from bot.logging_config import logger

app = FastAPI(
    title="Trading Bot API",
    description="API for Binance Futures Testnet Trading Bot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.exception_handler(BinanceAPIError)
async def binance_api_exception_handler(request, exc: BinanceAPIError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "type": "BinanceAPIError"}
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "type": "ValidationError"}
    )

@app.exception_handler(PydanticValidationError)
async def pydantic_validation_exception_handler(request, exc: PydanticValidationError):
    errors = exc.errors()
    error_msg = ", ".join([f"{err['loc'][-1]}: {err['msg']}" for err in errors])
    return JSONResponse(
        status_code=422,
        content={"error": error_msg, "type": "InputValidationError"}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "type": "ValueError"}
    )

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application")
