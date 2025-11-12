import logging

from fastapi import APIRouter, HTTPException, Request, Depends

import httpx

from src.dependencies import get_service
from src.services.incidents import IncidentService
from src.schemas.incidents import IncidentCreate
from src.config.config import settings


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["telegram"])


@router.post("/{token:path}/")
async def telegram_webhook(
    token: str,
    request: Request,
    service: IncidentService = Depends(get_service)
):
    if token != settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    data = await request.json()
    message = data.get("message", {})
    text = message.get("text")
    chat_id = message.get("chat", {}).get("id")
    user = message.get("from", {}).get("username", "unknown")

    if not text:
        return {"ok": False, "error": "no text"}

    if await handle_command(text, chat_id, service):
        return {"ok": True}

    incident = IncidentCreate( description=text, source=settings.SERVICE_SOURCE )
    await service.add(incident)

    confirmation_text = "Incident recorded."
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{settings.TELsEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": chat_id, "text": confirmation_text}
        )

    return {"ok": True}


async def handle_command(text: str, chat_id: int, service: IncidentService) -> bool:
    if text.strip() == f"/get_{settings.SERVICE_SOURCE}":
        incidents = await service.get_all()
        response_text = "\n".join([f"{i.id}: {i.description}: {i.status.value}" for i in incidents]) or "No incidents found"

        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": chat_id, "text": response_text}
            )
        return True

    return False


async def set_telegram_webhook():
    url = f"{settings.SERVICE_URL}/webhook/{settings.TELEGRAM_BOT_TOKEN}"
    print(url)
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook",
            data={"url": url}
        )
        result = resp.json()
        if result.get("ok"):
            print("Telegram webhook set successfully")
            logger.info("Telegram webhook set successfully")
        else:
            print(f"Failed to set Telegram webhook: {result}")
            logger.error(f"Failed to set Telegram webhook: {result}")