import pygame
import copy
import random
from game.objects.hewo.eye import Eye
from game.objects.hewo.mouth import Mouth
from game.settings import SettingsLoader, create_logger

PHI = ((1 + 5 ** (1 / 2)) / 2)  # Proporción áurea

class Face:
    def __init__(self, settings=None, object_name="Face"):
        self.settings = copy.deepcopy(settings)
        self.logger = create_logger(object_name)
        self.size_factor = self.settings['face']['size']
        self.size = [PHI * self.size_factor, self.size_factor]
        self.position = self.settings['face']['position']
        self.color = tuple(self.settings['face']['bg_color'])
        self.max_size = self.settings['face']['max_size']

        # Superficie de la cara
        self.face_surface = pygame.Surface(self.size)

        # Tamaños proporcionales de ojos y boca
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]

        # Posiciones de los elementos en la cara
        self.left_eye_pos = [0, 0]
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]

        # Inicialización de los ojos y la boca usando settings correspondientes
        self.mouth_settings = copy.deepcopy(self.settings['mouth'])
        self.left_eye_settings = copy.deepcopy(self.settings['eye'])
        self.right_eye_settings = copy.deepcopy(self.settings['eye'])

        self.mouth = Mouth(self.mouth_size, self.mouth_pos, settings=self.mouth_settings, object_name="Mouth")
        self.left_eye = Eye(self.eye_size, self.left_eye_pos, settings=self.left_eye_settings, object_name="Left Eye")
        self.right_eye = Eye(self.eye_size, self.right_eye_pos, settings=self.right_eye_settings, object_name="Right Eye")

        self.set_position(self.position)

        # Blink timer
        self.blink_timer = 0
        self.blink_interval = random.randint(300, 700)
        self.is_talking = True


    def update_layout(self):
        self.face_surface = pygame.Surface(self.size)
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]

        self.left_eye_pos = [0, 0]
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]

        self.left_eye.position = self.left_eye_pos
        self.right_eye.position = self.right_eye_pos
        self.mouth.position = self.mouth_pos
        self.left_eye.size = self.eye_size
        self.right_eye.size = self.eye_size
        self.mouth.size = self.mouth_size

    def update_elements(self):
        self.left_eye.update()
        self.right_eye.update()
        self.mouth.update()

    def set_size(self, size_factor):
        self.size_factor = size_factor
        size = [PHI * self.size_factor, size_factor]
        self.size = [max(1, size[0]), max(1, size[1])]
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]
        self.left_eye.set_size(self.eye_size)
        self.right_eye.set_size(self.eye_size)
        self.mouth.set_size(self.mouth_size)

    def set_position(self, pos):
        self.position[0] = max(0, min(pos[0], self.max_size[0] - self.size[0]))
        self.position[1] = max(0, min(pos[1], self.max_size[1] - self.size[1]))
        self.left_eye.set_position([0, 0])
        self.right_eye.set_position([self.eye_size[0] / 100 - 1, 0])
        self.mouth.position = [self.eye_size[0], self.eye_size[1]]

    def update_face(self):
        self.blink_timer += 1
        if self.blink_timer >= self.blink_interval:
            self.left_eye.trigger_blink()
            self.right_eye.trigger_blink()
            self.blink_timer = 0
            self.blink_interval = random.randint(300, 700)  # Randomize blink interval

        self.update_layout()
        self.left_eye.animate_blink()
        self.right_eye.animate_blink()
        self.update_elements()

    def handle_event(self, event):
        self.left_eye.handle_event(event)
        self.right_eye.handle_event(event)
        self.mouth.handle_event(event)

    def draw(self, surface):
        self.face_surface = pygame.Surface(self.size)
        self.face_surface.fill(self.color)
        self.left_eye.draw(self.face_surface)
        self.right_eye.draw(self.face_surface)
        self.mouth.draw(self.face_surface)
        surface.blit(self.face_surface, dest=self.position)


# Test face object
def test_component():
    pygame.init()
    settings = SettingsLoader().load_settings("game.settings.hewo")
    print(settings)
    screen = pygame.display.set_mode((800, 600))
    face = Face()
    clock = pygame.time.Clock()

    while True:
        screen.fill((255, 255, 255))
        face.update()
        face.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            face.handle_event(event)


if __name__ == '__main__':
    test_component()