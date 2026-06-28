from __future__ import annotations
import json
from pathlib import Path
from pydantic import BaseModel

class Config(BaseModel):
    theme: str = "dark"
    hotkey_toggle: str = "F3"
    hotkey_exit: str = "F4"
    hotkey_gui: str = "HOME"
    discord_rich_presence: bool = True
    auto_attach: bool = False
    process_name: str = "destiny2.exe"
    log_level: str = "INFO"

CONFIG_DIR = Path.home() / "Documents" / "Destiny2-Ultimate-Trainer-2026-plus"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    if CONFIG_FILE.exists():
        try:
            return Config(**json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
        except:
            pass
    cfg = Config()
    save_config(cfg)
    return cfg

def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")
