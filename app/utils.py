# app/utils.py (create new file)

import hashlib
import base64

def generate_short_id(original_url) -> str:
    # Convert HttpUrl to string if needed
    url_str = str(original_url)
    hash_object = hashlib.sha256(url_str.encode())
    base64_hash = base64.urlsafe_b64encode(hash_object.digest()).decode()
    return base64_hash[:8]
