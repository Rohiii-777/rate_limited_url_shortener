from fastapi import FastAPI, Request,Depends
from app import models
from app.db import engine
from app.auth import router as auth_router
from app.exceptions import validation_exception_handler, generic_500_handler,CustomHttpException
from app.rate_limiter import rate_limiter

from app.services.metrics import router as metrics_router
from fastapi.responses import JSONResponse
from app.routers.url import router as url_router


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include auth routes
app.include_router(metrics_router, prefix="")
app.include_router(auth_router)
app.include_router(url_router)

# Global exception handlers
app.add_exception_handler(422, validation_exception_handler)
app.add_exception_handler(500, generic_500_handler)

@app.exception_handler(CustomHttpException)
async def custom_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )

@app.get("/test")
async def test_limit(request: Request):
    await rate_limiter(request)
    return {"status": "ok", "message": "You're within limit!"}

@app.get("/")
def root():
    return {"message": "URL Shortener is alive!"}
