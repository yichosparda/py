from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame.locals import *
from pygame import mixer

alvl = 0
slvl = 0
mlvl = 0
clvl = 0

window = Tk()
window.title("")
window.geometry("1200x900")
window.option_add("*Background", "#000000")
window.config(bg="#000000")
window.resizable(False,False)

door_image = Image.open("sprites/door.png")
door = ImageTk.PhotoImage(door_image)
sdoor = Button(window, image = door)
sdoor.place(x = 200, y = 100)
adoor = Button(window, image = door)
adoor.place(x = 50, y = 400)
mdoor = Button(window, image=door)
mdoor.place(x = 800, y = 100)
cdoor = Button(window, image = door)
cdoor.place(x = 950, y = 400)



mainloop()