# app/routers/url.py

from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import schemas, models
from app.utils import generate_short_id
from app.rate_limiter import rate_limiter
from app.exceptions import http_error
from fastapi.responses import RedirectResponse
from typing import Optional
from app.auth import get_current_user
from app.services.metrics import url_redirect_counter, url_shorten_counter

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/shorten", response_model=schemas.URLInfo)
async def shorten_url(
    data: schemas.URLCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user),
):
    await rate_limiter(request, user_id=str(current_user.id) if current_user else None)

    ip = request.client.host
    short_id = generate_short_id(str(data.url))
    url_shorten_counter.inc()
    existing = db.query(models.ShortenedURL).filter(models.ShortenedURL.short_id == short_id).first()
    if existing:
        return existing

    new_url = models.ShortenedURL(
        original_url=str(data.url),
        short_id=short_id,
        ip_address=ip,
        owner_id=current_user.id if current_user else None
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@router.get("/{short_id}")
def redirect_url(short_id: str, db: Session = Depends(get_db)):
    url_redirect_counter.inc()
    url_entry = db.query(models.ShortenedURL).filter(models.ShortenedURL.short_id == short_id).first()
    if not url_entry:
        return http_error("Short URL not found", status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=url_entry.original_url)

@router.get("/me/urls", response_model=list[schemas.URLInfo])
def get_my_urls(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    urls = db.query(models.ShortenedURL).filter(models.ShortenedURL.owner_id == current_user.id).all()
    return urls
