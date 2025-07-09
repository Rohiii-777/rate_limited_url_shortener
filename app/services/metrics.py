from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

# Define metrics
url_shorten_counter = Counter("url_shorten_total", "Total URLs shortened")
url_redirect_counter = Counter("url_redirect_total", "Total URL redirects")
ip_block_counter = Counter("ip_block_total", "Total blocked IPs")

router = APIRouter()

@router.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
