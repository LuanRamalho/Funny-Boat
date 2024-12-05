import pygame
from pygame.locals import *
import numpy as np  # Importando NumPy
import util

def init():
    Health.heart_full = util.load_image("sydan")
    Health.heart_empty = util.load_image("sydan-tyhja")

class Health(pygame.sprite.Sprite):
    heart_full = None
    heart_empty = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not Health.heart_full or not Health.heart_empty:
            init()

        self.rect = pygame.Rect(10, 0, Health.heart_full.get_width() * 5 + 4, Health.heart_full.get_height() * 2)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.set_colorkey((255, 255, 255))

        self.max_hearts = 5
        self.hearts_left = self.max_hearts  # Número inicial de corações
        self.death_counters = np.zeros(self.max_hearts, dtype=int)  # Array para animações de morte

        self.update()

    def update(self):
        # Limpa a superfície
        self.image.fill((255, 255, 255))

        # Usa NumPy para cálculos e indexação
        full_hearts = np.arange(min(self.hearts_left, self.max_hearts))
        empty_hearts = np.arange(self.max_hearts, self.hearts_left, -1) - 1

        # Blita corações cheios
        for i in full_hearts:
            rect = pygame.Rect(i * (Health.heart_full.get_width() + 1), Health.heart_full.get_height(), Health.heart_full.get_width(), Health.heart_full.get_height())
            self.image.blit(Health.heart_full, rect)

        # Blita corações vazios
        for i in empty_hearts:
            rect = pygame.Rect(i * (Health.heart_full.get_width() + 1), Health.heart_full.get_height(), Health.heart_full.get_width(), Health.heart_full.get_height())
            self.image.blit(Health.heart_empty, rect)

        # Animação dos corações morrendo
        dying_hearts = np.where(self.death_counters > 0)[0]
        for i in dying_hearts:
            rect = pygame.Rect(i * (Health.heart_full.get_width() + 1), Health.heart_full.get_height(), Health.heart_full.get_width(), Health.heart_full.get_height())
            rect.top -= self.death_counters[i]
            # Superfície temporária para efeito de fading
            temp_surface = pygame.Surface((rect.width, rect.height))
            temp_surface.blit(util.load_image("sydan-rikki"), (0, 0))
            temp_surface.set_alpha(255 - self.death_counters[i] * 10)
            self.image.blit(temp_surface, rect)
            self.death_counters[i] += 1
            if self.death_counters[i] == 25:
                self.death_counters[i] = 0  # Reseta o contador

    def damage(self):
        if self.hearts_left > 0:
            self.hearts_left -= 1
            self.death_counters[self.hearts_left] = 1  # Inicia a animação de morte

    def add(self):
        if self.hearts_left < self.max_hearts:
            self.hearts_left += 1
            self.death_counters[self.hearts_left - 1] = 0  # Não anima corações adicionados
