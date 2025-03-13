import pygame
import random
from game.objects.hewo.face import Face
from game.settings import SettingsLoader, create_logger


class HeWo(Face):
    def __init__(self, settings, object_name="HeWo"):
        super().__init__(settings=settings)
        self.logger = create_logger(object_name)
        self.settings = settings

        # Configuración de estado inicial
        self.initial_emotion = [
            0, 0, 0,
            100,
            100, 100, 100,
            0, 0, 0,
            100,
            100, 100, 100,
            0, 0, 100, 0, 0,
            0, 0, 100, 0, 0
        ]
        self.emotion_goal = self.emotion_dict_from_values(self.initial_emotion)
        self.emotion_step = 5
        self.move_step = 10
        self.increase_mode = True  # Alterna entre aumentar y disminuir valores
        self.manual_mode = True  # Modo manual para ajustar emociones
        # Mapeos de teclas
        self.key_down_mappings = {
            pygame.K_SPACE: self.toggle_mode

        }
        self.key_pressed_mappings = {
            pygame.K_m: self.set_random_emotion,
            pygame.K_n: self.reset_emotion,
            pygame.K_v: lambda: self.adjust_size(self.move_step),
            pygame.K_b: lambda: self.adjust_size(-self.move_step),
            pygame.K_UP: lambda: self.adjust_position(0, -self.move_step),
            pygame.K_DOWN: lambda: self.adjust_position(0, self.move_step),
            pygame.K_LEFT: lambda: self.adjust_position(-self.move_step, 0),
            pygame.K_RIGHT: lambda: self.adjust_position(self.move_step, 0),
        }
        self.map_emotion_keys()

    def update(self):
        """ Llamado en cada frame, maneja teclas pulsadas y actualiza emociones """
        if self.manual_mode:
            self.handle_keypressed()
        self.update_emotion()
        self.update_face()

    def handle_event(self, event):
        """ Maneja eventos como teclas presionadas una vez (KEYDOWN) """
        if self.manual_mode:
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_down_mappings:
                    self.key_down_mappings[event.key]()

    def handle_keypressed(self):
        """ Maneja teclas pulsadas continuamente """
        keys = pygame.key.get_pressed()
        for key, action in self.key_pressed_mappings.items():
            if keys[key]:
                action()

    def map_emotion_keys(self):
        """ Mapea teclas (qwerty...) para cada parámetro del emotion_goal """
        keys = [
            pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y,
            pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_a, pygame.K_s,
            pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k,
            pygame.K_l, pygame.K_z, pygame.K_x, pygame.K_c
        ]
        parameters = list(self.emotion_goal.keys())

        for key, param in zip(keys, parameters):
            self.key_pressed_mappings[key] = lambda p=param: self.adjust_emotion(p)

    def toggle_mode(self):
        """ Alterna entre aumentar o disminuir valores """
        self.increase_mode = not self.increase_mode
        mode = "Increase" if self.increase_mode else "Decrease"
        self.logger.info(f"Mode toggled to: {mode}")

    def adjust_emotion(self, param):
        """ Ajusta el valor de un parámetro en emotion_goal """
        if self.increase_mode:
            self.emotion_goal[param] = min(100, self.emotion_goal[param] + self.emotion_step)
        else:
            self.emotion_goal[param] = max(0, self.emotion_goal[param] - self.emotion_step)
        self.logger.info(f"Adjusted {param} to {self.emotion_goal[param]}")

    def set_emotion_goal(self, emotion_dict):
        self.emotion_goal = emotion_dict

    def adjust_position(self, dx, dy):
        """ Ajusta la posición de HeWo """
        position = self.position
        position[0] += dx
        position[1] += dy
        self.set_position(position)
        self.logger.info(f"Position adjusted to: {position}")

    def adjust_size(self, ds):
        size_factor = self.size_factor
        size_factor += ds
        self.set_size(size_factor)
        self.adjust_position(0, 0)

    def update_emotion(self):
        """ Aplica la transición progresiva hacia el emotion_goal """
        new_emotion, _ = self.transition(self.emotion_goal)
        self.set_emotion(new_emotion)

    def emotion_dict_from_values(self, values):
        """ Convierte una lista de valores en un diccionario de emociones """
        keys = [
            'letl_a', 'letl_b', 'letl_c',
            'lps',
            'lebl_a', 'lebl_b', 'lebl_c',
            'retl_a', 'retl_b', 'retl_c',
            'rps',
            'rebl_a', 'rebl_b', 'rebl_c',
            'tl_a', 'tl_b', 'tl_c', 'tl_d', 'tl_e',
            'bl_a', 'bl_b', 'bl_c', 'bl_d', 'bl_e'
        ]
        return dict(zip(keys, values))

    def transition(self, emotion_b_dict):
        """ Realiza la transición progresiva hacia emotion_goal """
        start = self.get_emotion()
        diffs = []
        for key in start.keys():
            diff = emotion_b_dict[key] - start[key]
            if diff > 0:
                start[key] += min(diff, self.emotion_step)
            elif diff < 0:
                start[key] += max(diff, -self.emotion_step)
            diffs.append(emotion_b_dict[key] - start[key])
        return start, diffs

    def get_emotion(self):
        """ Obtiene el estado actual de la emoción desde los componentes de la cara """
        letl, lps, lebl = self.left_eye.get_emotion()
        retl, rps, rebl = self.right_eye.get_emotion()
        tl, bl = self.mouth.get_emotion()
        return {
            'letl_a': letl[0], 'letl_b': letl[1], 'letl_c': letl[2],
            'lps': lps,
            'lebl_a': lebl[0], 'lebl_b': lebl[1], 'lebl_c': lebl[2],
            'retl_a': retl[0], 'retl_b': retl[1], 'retl_c': retl[2],
            'rps': rps,
            'rebl_a': rebl[0], 'rebl_b': rebl[1], 'rebl_c': rebl[2],
            'tl_a': tl[0], 'tl_b': tl[1], 'tl_c': tl[2], 'tl_d': tl[3], 'tl_e': tl[4],
            'bl_a': bl[0], 'bl_b': bl[1], 'bl_c': bl[2], 'bl_d': bl[3], 'bl_e': bl[4]
        }

    def set_emotion(self, emotion_dict):
        """ Configura los valores de emoción para los componentes de la cara """
        letl = [emotion_dict['letl_a'], emotion_dict['letl_b'], emotion_dict['letl_c']]
        lps = emotion_dict['lps']
        lebl = [emotion_dict['lebl_a'], emotion_dict['lebl_b'], emotion_dict['lebl_c']]
        retl = [emotion_dict['retl_a'], emotion_dict['retl_b'], emotion_dict['retl_c']]
        rps = emotion_dict['rps']
        rebl = [emotion_dict['rebl_a'], emotion_dict['rebl_b'], emotion_dict['rebl_c']]
        tl = [emotion_dict['tl_a'], emotion_dict['tl_b'], emotion_dict['tl_c'], emotion_dict['tl_d'],
              emotion_dict['tl_e']]
        bl = [emotion_dict['bl_a'], emotion_dict['bl_b'], emotion_dict['bl_c'], emotion_dict['bl_d'],
              emotion_dict['bl_e']]
        self.left_eye.set_emotion(letl, lps, lebl)
        self.right_eye.set_emotion(retl, rps, rebl)
        self.mouth.set_emotion(tl, bl)
        self.logger.debug(f"Setting emotion to: {emotion_dict}")

    def set_random_emotion(self):
        """ Configura una emoción aleatoria en emotion_goal """
        random_emotion = [random.randint(0, 100) for _ in range(len(self.emotion_goal))]
        self.emotion_goal = self.emotion_dict_from_values(random_emotion)
        self.logger.info(f"Random emotion set: {self.emotion_goal}")

    def reset_emotion(self):
        self.set_size(300)
        self.emotion_goal = self.emotion_dict_from_values(self.initial_emotion)


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
