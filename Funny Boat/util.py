import pygame


# Some general utility functions here

def load_font(name, size):
    return pygame.font.Font("data/" + name + ".ttf", size)

def load_image(name):
    return pygame.image.load("data/" + name + ".png").convert_alpha()

def load_sound(name):
    return pygame.mixer.Sound("data/" + name + ".ogg")

def load_music(name):
    # The all-caps ogg is because the original file just happened to be that way
    pygame.mixer.music.load("data/" + name + ".ogg")
