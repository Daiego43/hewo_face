import copy
import math
import time
import pygame
import numpy as np
from scipy.interpolate import make_interp_spline
from game.settings import create_logger


class Lip:
    def __init__(self, size, position, settings, object_name="Lip"):
        self.logger = create_logger(object_name)
        self.size = size
        self.position = position
        self.color = tuple(settings['color'])
        self.lip_width = settings['lip_width']
        self.emotion = settings['emotion']  # 5-element vector: [x1, y1, center_y, x2, y2]

    def lip_shape(self):
        x_points = [
            self.clamp(self.emotion[0] / 100 * (self.size[0] / 2), 0, self.size[0] / 2),
            self.size[0] / 2,  # El centro en el eje X es fijo
            self.clamp(self.size[0] - (self.emotion[3] / 100 * (self.size[0] / 2)), self.size[0] / 2, self.size[0])
        ]

        y_points = [
            self.clamp(self.emotion[1] / 100 * self.size[1], self.lip_width, self.size[1] - self.lip_width),
            self.clamp(self.emotion[2] / 100 * self.size[1], self.lip_width, self.size[1] - self.lip_width),
            self.clamp(self.emotion[4] / 100 * self.size[1], self.lip_width, self.size[1] - self.lip_width)
        ]
        x_points = self.fix_x_points(x_points)
        spline = make_interp_spline(x_points, y_points, k=2)
        x_range = np.linspace(min(x_points), max(x_points), 500)
        return [(int(x), int(spline(x))) for x in x_range]

    def clamp(self, value, min_value, max_value):
        return max(min_value, min(value, max_value))

    def fix_x_points(self, x_points):
        # Detecta el duplicado y lo cambiará por un valor ligeramente diferente
        if int(x_points[0]) == int(x_points[1]):
            x_points[0] -= 1
        if int(x_points[1]) == int(x_points[2]):
            x_points[2] += 1
        return x_points

    def set_emotion(self, emotion_vector):
        """
        Establece la emoción del labio usando un vector de 5 valores: [x1, y1, center_y, x2, y2].
        """
        self.emotion = emotion_vector

    def get_emotion(self):
        """
        Obtiene el vector de emoción actual del labio.
        """
        return self.emotion

    def update(self):
        pass

    def draw(self, surface):
        points = self.lip_shape()
        pygame.draw.lines(surface, self.color, False, points, self.lip_width)

    def handle_event(self, event):
        pass


class Mouth:
    def __init__(self, size, position, settings, object_name="Mouth"):
        self.logger = create_logger(object_name)
        self.settings = copy.deepcopy(settings)
        self.size = size
        self.position = position
        self.surface = pygame.Surface(self.size)
        self.color = self.settings['bg_color']

        # Creación de los labios superior e inferior utilizando los settings
        self.top_lip = Lip(self.size, self.position, self.settings['upper_lip'], object_name=f"{object_name} - Top Lip")
        self.bot_lip = Lip(self.size, self.position, self.settings['lower_lip'], object_name=f"{object_name} - Bot Lip")

        # Talking vars
        self.talking_amplitude = self.settings['talking_amplitude']
        self.talking_speed = self.settings['talking_speed']
        self._talking_reference = {
            'top': self.top_lip.get_emotion(),
            'bot': self.bot_lip.get_emotion()
        }
        self.is_talking = False

    def set_size(self, size):
        self.size = size
        self.top_lip.size = size
        self.bot_lip.size = size

    def draw(self, surface):
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.top_lip.draw(self.surface)
        self.bot_lip.draw(self.surface)
        surface.blit(self.surface, self.position)

    def update(self):
        self.top_lip.update()
        self.bot_lip.update()
        if self.is_talking:
            self.animate_talk()

    def set_talking_reference(self):
        """
        Establece la referencia de los labios superior e inferior para la animación de hablar.
        """
        self._talking_reference = {
            'top': self.top_lip.get_emotion(),
            'bot': self.bot_lip.get_emotion()
        }

    def toggle_talk(self):
        if not self.is_talking:
            self.set_talking_reference()
            self.talking_start_time = time.time()
            self.is_talking = True
        else:
            self.is_talking = False
            self.top_lip.set_emotion(self._talking_reference['top'])
            self.bot_lip.set_emotion(self._talking_reference['bot'])

    def animate_talk(self):
        if not self.is_talking:
            return

        tick = (time.time() - self.talking_start_time) * self.talking_speed
        osc = abs(math.sin(tick)) * self.talking_amplitude

        base_top = self._talking_reference['top']
        base_bot = self._talking_reference['bot']

        center_y = (base_top[2] + base_bot[2]) / 2

        new_top = base_top[:]
        new_bot = base_bot[:]

        new_top[2] = center_y - osc
        new_bot[2] = center_y + osc

        self.top_lip.set_emotion(new_top)
        self.bot_lip.set_emotion(new_bot)

    def handle_event(self, event):
        pass

    def set_emotion(self, top_lip_percentages, bot_lip_percentages):
        """
        Establece la emoción de los labios superior e inferior usando vectores de 5 valores.
        """
        self.top_lip.set_emotion(top_lip_percentages)
        self.bot_lip.set_emotion(bot_lip_percentages)
        self.set_talking_reference()

    def get_emotion(self):
        """
        Obtiene los vectores de emoción actuales de los labios superior e inferior.
        """
        top_emotion = self.top_lip.get_emotion()
        bot_emotion = self.bot_lip.get_emotion()
        return top_emotion, bot_emotion
