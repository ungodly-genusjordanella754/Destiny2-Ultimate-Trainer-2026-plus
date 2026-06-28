import asyncio
import logging
import sys
from rich.logging import RichHandler
from src.config import load_config
from src.cheatengine import CheatEngine
from src.gui import launch_gui

logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger("Destiny2-Ultimate-Trainer-2026-plus")

async def main():
    log.info("Starting Destiny2-Ultimate-Trainer-2026-plus 1.0.0...")
    config = load_config()
    trainer = CheatEngine(config)
    from src.web_dashboard import Monitor
    dashboard = Monitor(trainer, port=4201)
    asyncio.create_task(dashboard.start())
    launch_gui(trainer)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        log.exception(f"Fatal: {e}")
        sys.exit(1)
