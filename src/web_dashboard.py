from __future__ import annotations
import asyncio, logging
from aiohttp import web
from src.cheatengine import CheatEngine

log = logging.getLogger("Destiny2-Ultimate-Trainer-2026-plus.Monitor")

class Monitor:
    def __init__(self, trainer: CheatEngine, port=4201):
        self.trainer = trainer
        self.port = port
        self.app = web.Application()
        self.app.router.add_get("/", self.index)
        self.app.router.add_get("/ws", self.ws)
        self.connections = set()

    async def index(self, request):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Destiny2-Ultimate-Trainer-2026-plus Dashboard</title>
    <style>
        body { background: #1a1a2e; color: #d35400; font-family: sans-serif; }
        .card { background: #16213e; padding: 20px; margin: 10px; border-radius: 8px; }
        .on { color: #0f0; }
        .off { color: #f00; }
    </style>
</head>
<body>
    <h1>Destiny2-Ultimate-Trainer-2026-plus</h1>
    <div id="features"></div>
    <script>
        const ws = new WebSocket(`ws://${location.host}/ws`);
        ws.onmessage = event => {
            const data = JSON.parse(event.data);
            const container = document.getElementById('features');
            container.innerHTML = '';
            for (const [feat, active] of Object.entries(data)) {
                const div = document.createElement('div');
                div.className = 'card';
                div.innerHTML = `${feat}: <span class="${active ? 'on' : 'off'}">${active ? 'ON' : 'OFF'}</span>`;
                container.appendChild(div);
            }
        };
    </script>
</body>
</html>"""
        return web.Response(text=html, content_type='text/html')

    async def ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.connections.add(ws)
        try:
            while True:
                await ws.send_json(self.trainer.features)
                await asyncio.sleep(1)
        finally:
            self.connections.discard(ws)
        return ws

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        await web.TCPSite(runner, 'localhost', self.port).start()
        log.info(f"Dashboard at http://localhost:{self.port}")
        await asyncio.Event().wait()
