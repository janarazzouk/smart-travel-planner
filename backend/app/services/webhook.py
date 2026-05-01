import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=1, max=5),
)
async def send_discord_webhook(
    webhook_url: str | None,
    content: str,
) -> None:
    if not webhook_url:
        logger.info("Discord webhook URL is not configured.")
        return

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(
                webhook_url,
                json={"content": content[:1900]},
            )
            response.raise_for_status()

        logger.info("Discord webhook sent successfully.")

    except Exception:
        logger.exception("Discord webhook delivery failed.")