import random
import string
from sqlalchemy.orm import Session
from app import models

def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_short_url(db: Session, original_url: str, ip_address: str, user_id: int = None):
    short_id = generate_short_id()
    
    # Make sure it's unique (loop until safe)
    while db.query(models.ShortenedURL).filter_by(short_id=short_id).first():
        short_id = generate_short_id()

    url = models.ShortenedURL(
        original_url=original_url,
        short_id=short_id,
        owner_id=user_id,
        ip_address=ip_address
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    return url

def get_url_by_short_id(db: Session, short_id: str):
    return db.query(models.ShortenedURL).filter_by(short_id=short_id).first()
