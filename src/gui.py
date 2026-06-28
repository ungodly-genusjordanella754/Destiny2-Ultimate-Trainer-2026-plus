from __future__ import annotations
import asyncio, threading, logging
from typing import Dict
import customtkinter as ctk
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem
from src.cheatengine import CheatEngine

log = logging.getLogger("Destiny2-Ultimate-Trainer-2026-plus.GUI")

class TrainerGUI(ctk.CTk):
    def __init__(self, trainer: CheatEngine):
        super().__init__()
        self.trainer = trainer
        self.title("Destiny2-Ultimate-Trainer-2026-plus 1.0.0")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color="#1a1a2e")
        self.feature_vars: Dict[str, ctk.BooleanVar] = {}
        self.status_text = ctk.StringVar(value="Not attached")
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(100, self._update_status)

    def create_widgets(self):
        ctk.CTkLabel(self, text="Destiny2-Ultimate-Trainer-2026-plus", font=("Segoe UI", 24, "bold")).pack(pady=20)
        status_frame = ctk.CTkFrame(self, fg_color="#16213e")
        status_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(status_frame, textvariable=self.status_text, text_color="white").pack(side="left", padx=10)
        self.attach_btn = ctk.CTkButton(status_frame, text="Attach", command=self.attach_process)
        self.attach_btn.pack(side="right", padx=10)

        features_frame = ctk.CTkScrollableFrame(self, fg_color="#0f3460")
        features_frame.pack(fill="both", expand=True, padx=10, pady=10)
        feature_names = ['invincibility', 'infinite_ammo', 'wallhack', 'super_speed', 'no_spread', 'unlock_all', 'auto_bounty', 'auto_aim']
        for name in feature_names:
            var = ctk.BooleanVar(value=False)
            self.feature_vars[name] = var
            frame = ctk.CTkFrame(features_frame, fg_color="#1a1a2e")
            frame.pack(fill="x", padx=5, pady=5)
            ctk.CTkLabel(frame, text=name.replace("_", " ").title(), font=("Segoe UI", 16)).pack(side="left", padx=10)
            ctk.CTkSwitch(frame, variable=var, command=lambda n=name: self.toggle_feature(n)).pack(side="right", padx=10)

        self.console = ctk.CTkTextbox(self, height=100, fg_color="#0f3460", text_color="white")
        self.console.pack(fill="x", padx=10, pady=10)
        self.console.insert("end", "Trainer ready.\n")

    def attach_process(self):
        asyncio.run_coroutine_threadsafe(self._attach(), asyncio.get_event_loop())

    async def _attach(self):
        if await self.trainer.memory.attach():
            self.status_text.set("Attached")
            self.attach_btn.configure(state="disabled")
            await self.trainer.start()
        else:
            self.status_text.set("Attach failed")

    def toggle_feature(self, feature: str):
        asyncio.run_coroutine_threadsafe(
            self.trainer.toggle_feature(feature, self.feature_vars[feature].get()),
            asyncio.get_event_loop()
        )

    def _update_status(self):
        self.status_text.set("Attached" if self.trainer.memory.pm else "Not attached")
        self.after(1000, self._update_status)

    def on_close(self):
        self.trainer.stop()
        self.quit()

def create_tray_icon(gui):
    img = Image.new('RGB', (64,64), color=(211, 84, 0))
    ImageDraw.Draw(img).rectangle([16,16,48,48], fill=(255,255,255))
    menu = pystray.Menu(MenuItem('Show', lambda: gui.deiconify()), MenuItem('Exit', lambda: gui.quit()))
    return pystray.Icon("trainer", img, "Destiny2-Ultimate-Trainer-2026-plus", menu)

def launch_gui(trainer):
    app = TrainerGUI(trainer)
    threading.Thread(target=create_tray_icon(app).run, daemon=True).start()
    app.mainloop()
