import os
import pygame
import logging
import screeninfo
from game.settings import SettingsLoader
from game.objects.hewo.hewo import HeWo
from game.main.endpoint import ServerEndPoint

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(name)s: %(message)s')

class MainWindow:
    def __init__(self, settings, layout_list=None, active_layout=None):
        pygame.init()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.settings = settings
        monitors = screeninfo.get_monitors()
        self.logger.info(f"Monitors: {[(m.name, m.width, m.height) for m in monitors]}")

        if self.settings['deploy']:
            self.logger.info("Deploy mode enabled")
            flags = pygame.FULLSCREEN
            monitor_id = self.settings['monitor_id']
            monitor_specs = monitors[monitor_id]
            self.window_size = (monitor_specs.width, monitor_specs.height)
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor_specs.x},{monitor_specs.y}"
        else:
            flags = pygame.RESIZABLE
            self.logger.info("Deploy mode disabled")
            monitor_id = self.settings['monitor_id']
            monitor_specs = monitors[monitor_id]
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor_specs.x - monitor_specs.width / 2},{monitor_specs.y}"
            self.window_size = (self.settings['width'], self.settings['height'])

        self.logger.info(f"Window size: {self.window_size}")
        self.screen = pygame.display.set_mode(
            size=self.window_size,
            display=monitor_id,
            flags=flags,
            vsync=True
        )

        pygame.display.set_caption(self.settings['window_title'])
        self.layout_list = layout_list
        self.clock = pygame.time.Clock()
        self.background_color = self.settings['bg_color']
        self.active_layout = active_layout

        # Inicializa el servidor web sin afectar el flujo
        self.web_server = ServerEndPoint(self)
        self.web_server.start()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if self.active_layout is not None:
                self.layout_list[self.active_layout].handle_event(event)

    def set_active_layout(self, layout_index):
        if layout_index < len(self.layout_list):
            self.active_layout = layout_index
        else:
            self.active_layout = None
            print(f'Index {layout_index} out of range')

    def update(self):
        if self.active_layout is not None:
            self.layout_list[self.active_layout].update()

    def draw(self):
        self.screen.fill(self.background_color)
        if self.active_layout is not None:
            self.layout_list[self.active_layout].draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


def main():
    # Carga configuraciones para la ventana y HeWo
    window_settings = SettingsLoader().load_settings("game.settings.window")
    hewo_settings = SettingsLoader().load_settings("game.settings.hewo")
    print(hewo_settings)
    print(window_settings)
    # Crea la ventana principal con HeWo como layout inicial
    main_window = MainWindow(
        settings=window_settings,
        layout_list=[
            HeWo(settings=hewo_settings)
        ],
        active_layout=0
    )

    # Ejecuta el bucle principal de Pygame
    main_window.run()


if __name__ == '__main__':
    main()
