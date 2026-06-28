from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class MemoryOffsets:
    GOD_MODE: int = 0x2a4b4d6
    UNLIMITED_AMMO: int = 0x2a4b572
    ESP_ENABLED: int = 0x2a4b5f6
    SPEED_HACK: int = 0x2a4b6a8
    NO_RECOIL: int = 0x2a4b7ba
    LOOT_UNLOCKER: int = 0x2a4b819
    BOUNTY_COMPLETE: int = 0x2a4b98b
    AIMBOT_FOV: int = 0x2a4ba19
    PLAYER_BASE: int = 0x1e8a434
    PLAYER_OFFSETS: list = field(default_factory=lambda: [0x0, 0x30, 0x8, 0x20])
    VERSION_OFFSETS: Dict[str, Dict[str,int]] = field(default_factory=lambda: {
        "2026.06.28-089": {
            "GOD_MODE": 0x2a4b4d6,
            "UNLIMITED_AMMO": 0x2a4b572,
        }
    })
    def get_for_version(self, ver): return self.VERSION_OFFSETS.get(ver, {})

offsets = MemoryOffsets()
