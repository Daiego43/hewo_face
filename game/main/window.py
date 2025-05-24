import os
import logging
import pygame
import screeninfo
from typing import Any

from game.settings import SettingsLoader
from game.objects.hewo.hewo import HeWo
from game.objects.multimedia.multimedia import MultimediaLayout, MultimediaGameObj, Multimedia
from game.main.endpoint import ServerEndPoint

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] - %(name)s: %(message)s")


class MainWindow:
    """Window manager that can host multiple *layouts* and cleans up audio/video gracefully."""

    def __init__(self, settings: dict[str, Any], layout_dict: dict[str, Any] | None = None,
                 active_layout: str | None = None):
        pygame.init()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.settings = settings

        # ------------------------------------------------ monitor setup
        monitors = screeninfo.get_monitors()
        self.logger.info(f"Monitors detected → {[(m.name, m.width, m.height) for m in monitors]}")

        monitor_id = self.settings["monitor_id"]
        monitor_specs = monitors[monitor_id]

        flags = pygame.FULLSCREEN if self.settings["deploy"] else pygame.RESIZABLE
        self.window_size = (
            (monitor_specs.width, monitor_specs.height) if self.settings["deploy"] else (self.settings["width"],
                                                                                         self.settings["height"])
        )
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{monitor_specs.x},{monitor_specs.y}"

        self.logger.info(f"Window size = {self.window_size}")
        self.screen = pygame.display.set_mode(
            size=self.window_size,
            display=monitor_id,
            flags=flags,
            vsync=self.settings["vsync"],
        )
        pygame.display.set_caption(self.settings["window_title"])

        # ------------------------------------------------ layout handling
        self.layout_dict: dict[str, Any] = layout_dict or {}
        self.active_layout: str | None = active_layout
        self.background_color = tuple(self.settings["bg_color"])

        # ------------------------------------------------ misc state
        self.clock = pygame.time.Clock()
        self.fps = self.settings["fps"]

        # ------------------------------------------------ optional web endpoint
        self.web_server = ServerEndPoint(self)
        self.web_server.start()

    # ---------------------------------------------------------------- cleanup helpers
    def _shutdown_media(self):
        """Stop audio/video (ffplay or mixer) for every Multimedia object in every layout."""
        for layout in self.layout_dict.values():
            if isinstance(layout, MultimediaLayout):
                for obj in layout.objects:
                    if isinstance(obj, Multimedia):
                        obj.stop()

    # ---------------------------------------------------------------- helpers
    def get_active_layout(self):
        return self.layout_dict.get(self.active_layout)

    # ---------------------------------------------------------------- event loop
    def handle_events(self):
        for event in pygame.event.get():
            should_quit = event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            )
            if should_quit:
                self.logger.info("Shutting down…")
                self._shutdown_media()
                pygame.quit()
                raise SystemExit

            layout = self.get_active_layout()
            if layout:
                layout.handle_event(event)

    def set_active_layout(self, layout_key: str):
        if layout_key in self.layout_dict:
            self.active_layout = layout_key
            self.logger.info(f"Switched to layout → {layout_key}")
        else:
            self.logger.warning(f'Layout key "{layout_key}" not found; keeping current layout')

    # ---------------------------------------------------------------- update & draw
    def update(self, dt_ms: float):
        layout = self.get_active_layout()
        if not layout:
            return
        try:
            layout.update(dt_ms)
        except TypeError:
            layout.update()

    def draw(self):
        self.screen.fill(self.background_color)
        layout = self.get_active_layout()
        if layout:
            layout.draw(self.screen)
        pygame.display.flip()

    # ---------------------------------------------------------------- main loop
    def run(self):
        while True:
            dt_ms = self.clock.tick(self.fps)
            self.handle_events()
            self.update(dt_ms)
            self.draw()


# ---------------------------------------------------------------- launcher example

def main():
    window_settings = SettingsLoader().load_settings("game.settings.window")
    hewo_settings = SettingsLoader().load_settings("game.settings.hewo")

    main_window = MainWindow(settings=window_settings)

    # build layouts
    hewo_layout = HeWo(settings=hewo_settings)

    import pathlib, importlib.resources as res
    resources_root = res.files("game.resources") if res.is_resource else pathlib.Path("game/resources")
    mp4 = resources_root / "test.mp4"
    img = resources_root / "img.png"
    multimedia_objects: list[MultimediaGameObj] = [
        # MultimediaGameObj(mp4, audio="ffplay", loop=True),
        MultimediaGameObj(img, position=(760, 0), velocity=(0, 0), loop=False, audio=False, object_name="ImageObj",size=(200, 200)),
        MultimediaGameObj(img, position=(0, 0), velocity=(0, 0), loop=False, audio=False, object_name="ImageObj",size=(200, 200)),
        MultimediaGameObj(mp4, position=(760,200), velocity=(0, 0), loop=True, object_name = "ImageObj", size = (200,200)),
        MultimediaGameObj(mp4, position=(0,200), velocity=(0, 0), loop=True, object_name = "ImageObj", size = (200,200)),
        MultimediaGameObj(mp4, position=(0, 400), velocity=(0, 0), loop=True, object_name="ImageObj", size=(960, 240)),
        # MultimediaGameObj(mp4, position=(380, 100), velocity=(0, 0), loop=False, audio='ffplay', object_name="ImageObj",size=(200, 200)),
    ]
    multimedia_layout = MultimediaLayout(multimedia_objects, bg_color=(0, 0, 0))

    main_window.layout_dict = {"hewo": hewo_layout,
                               "media": multimedia_layout}
    main_window.active_layout = "media"
    main_window.run()


if __name__ == "__main__":
    main()
