from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame.locals import *
from pygame import mixer

# window = Tk()
# window.title("")
# window.geometry("300x270")
# window.option_add("*Background", "#000000")
# window.config(bg="#000000")

pygame.init()
window = pygame.display.set_mode((600, 600))
image_sprite = [pygame.image.load("sans1.png"),
                pygame.image.load("sans2.png")]
clock = pygame.time.Clock()
value = 0
run = True

while run:
    clock.tick(3)
    if value >= len(image_sprite):
        value = 0
    image = image_sprite[value]
    x = 150
    y = 150

    window.blit(image, (x,y))
    pygame.display.update()
    # sans = Label(window, image = image)
    # window.update()
    value += 1