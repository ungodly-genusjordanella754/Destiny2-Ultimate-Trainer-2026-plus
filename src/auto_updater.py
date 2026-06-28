from __future__ import annotations
import asyncio, logging
from pathlib import Path
import aiohttp
from src.offsets import offsets as cur

log = logging.getLogger("Destiny2-Ultimate-Trainer-2026-plus.Updater")
URL = "https://api.skydock.netlify.app/updates/destiny2-trainer-plus.json"

async def check_for_updates():
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(URL) as r:
                if r.status != 200:
                    return False
                data = await r.json()
                if data.get("version") != "2026.06.28-089":
                    off_url = data.get("offsets_url")
                    if off_url:
                        async with s.get(off_url) as off:
                            if off.status == 200:
                                Path(__file__).parent.joinpath("offsets.py").write_text(await off.text())
                                log.info("Updated offsets")
                                return True
    except:
        log.exception("Update failed")
    return False
