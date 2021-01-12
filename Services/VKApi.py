from base64 import b64encode
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlencode


def is_valid(query: dict, secret: str) -> bool:
    """Check VK Apps signature"""
    vk_subset = filter(
        lambda key: key.startswith("vk_"),
        query
    )
    ordered = {k: query[k] for k in sorted(vk_subset)}
    hash_code = b64encode(
        HMAC(
            secret.encode(),
            urlencode(ordered, doseq=True).encode(),
            sha256
        ).digest()
    ).decode("utf-8")
    fixed_hash = hash_code[:-1 if hash_code[-1] == "=" else None].replace('+', '-').replace('/', '_')
    return query.get("sign") == fixed_hash


def get_user_ID(query: dict, secret: str) -> bool:
    """Get VK UserID"""
    vk_subset = filter(
        lambda key: key.startswith("vk_"),
        query
    )
    ordered = {k: query[k] for k in sorted(vk_subset)}
    hash_code = b64encode(
        HMAC(
            secret.encode(),
            urlencode(ordered, doseq=True).encode(),
            sha256
        ).digest()
    ).decode("utf-8")
    fixed_hash = hash_code[:-1 if hash_code[-1] == "=" else None].replace('+', '-').replace('/', '_')
    return query.get("vk_user_id")
