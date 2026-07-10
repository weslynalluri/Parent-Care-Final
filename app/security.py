import os, logging
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

logger = logging.getLogger(__name__)
_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_KEY    = os.environ.get("PARENTCARE_API_KEY", "")


async def verify_api_key(api_key: str = Security(_header)) -> str:
    if not _KEY:
        logger.warning("No API key set — running in dev mode")
        return "dev-mode"
    if api_key == _KEY:
        return api_key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or missing API key. Pass it in X-API-Key header.")
