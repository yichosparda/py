from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame.locals import *
from pygame import mixer
import time
import json

window = Tk()
window.title("")
window_width = 1200
window_height = 900
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
window.option_add("*Background", "#000000")
window.config(bg="#000000")
window.resizable(False,False)
textbox_image = Image.open("sprites/textbox.png")
textbox = ImageTk.PhotoImage(textbox_image)

background  = Canvas(window, width=1200, height=900)
background.pack()
bgimage = ImageTk.PhotoImage(Image.open("backgrounds/combat.png"))
background.create_image(0, 0, anchor=NW, image=bgimage)
enemy = ImageTk.PhotoImage(Image.open("sprites/slime.png"))
background.create_image(900, 100, anchor=NW, image=enemy)

mainloop()