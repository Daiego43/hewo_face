import pygame
import random
from game.objects.hewo.face import Face
from game.settings import SettingsLoader, create_logger
from game.objects.hewo.logic.emotion_mapper import EmotionMapper
from game.objects.hewo.logic.input_handler import HeWoInputHandler


class HeWo(Face):
    def __init__(self, settings, object_name="HeWo"):
        super().__init__(settings=settings)
        self.logger = create_logger(object_name)
        self.settings = settings

        self.mapper = EmotionMapper()
        self.input_handler = HeWoInputHandler(self, self.mapper)

    def set_emotion_goal(self, emotion_goal):
        self.logger.debug(f"Setting emotion goal: {emotion_goal}")
        self.mapper.emotion_goal = emotion_goal
        self.update_face()

    def update(self):
        if self.input_handler.manual_mode:
            self.input_handler.handle_keypressed()
        self.mapper.update_emotion(self)
        self.update_face()

    def handle_event(self, event):
        if self.input_handler.manual_mode:
            self.input_handler.handle_event(event)


# Código de prueba
def test_component():
    pygame.init()
    settings = SettingsLoader().load_settings("game.settings.hewo")
    hewo = HeWo(settings=settings)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("HeWo Class")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            hewo.handle_event(event)
        hewo.update()
        screen.fill((255, 255, 255))
        hewo.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    test_component()
