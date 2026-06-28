from __future__ import annotations
import asyncio, logging
from dataclasses import dataclass
from typing import List, Optional, Dict
import pymem, pymem.process, pymem.ressources.kernel32

log = logging.getLogger("Destiny2-Ultimate-Trainer-2026-plus.ProcessMemory")

@dataclass
class PointerChain:
    base_address: int
    offsets: List[int]

class ProcessMemory:
    def __init__(self, process_name="destiny2.exe"):
        self.process_name = process_name
        self.pm: Optional[pymem.Pymem] = None
        self.base_address = 0
        self.cache: Dict[str,int] = {}

    async def attach(self) -> bool:
        try:
            self.pm = await asyncio.to_thread(pymem.Pymem, self.process_name)
            self.base_address = await asyncio.to_thread(pymem.process.base_address, self.pm.process_handle)
            log.info(f"Attached to {self.process_name} PID={self.pm.process_id}")
            return True
        except Exception as e:
            log.error(f"Attach failed: {e}")
            return False

    async def detach(self):
        if self.pm:
            self.pm.close_process()
            self.pm = None

    async def read_pointer(self, base, offsets, as_type="int32"):
        addr = await asyncio.to_thread(pymem.ressources.kernel32.resolve_pointer, self.pm.process_handle, base, offsets)
        if as_type == "int32":
            return await asyncio.to_thread(self.pm.read_int, addr)
        elif as_type == "float":
            return await asyncio.to_thread(self.pm.read_float, addr)
        elif as_type == "int64":
            return await asyncio.to_thread(self.pm.read_longlong, addr)

    async def write_pointer(self, base, offsets, value, as_type="int32"):
        addr = await asyncio.to_thread(pymem.ressources.kernel32.resolve_pointer, self.pm.process_handle, base, offsets)
        if as_type == "int32":
            await asyncio.to_thread(self.pm.write_int, addr, value)
        elif as_type == "float":
            await asyncio.to_thread(self.pm.write_float, addr, value)
        elif as_type == "int64":
            await asyncio.to_thread(self.pm.write_longlong, addr, value)

    async def aob_scan(self, pattern, module="destiny2.exe"):
        try:
            return await asyncio.to_thread(pymem.pattern.scan_pattern_module, self.pm.process_handle, module, pattern.encode())
        except:
            return None

    def process_is_running(self):
        import psutil
        return any(p.info["name"] and p.info["name"].lower() == self.process_name.lower() for p in psutil.process_iter(["name"]))

    async def start_watcher(self):
        while True:
            if self.process_is_running() and not self.pm:
                await self.attach()
            elif not self.process_is_running() and self.pm:
                await self.detach()
            await asyncio.sleep(2)
