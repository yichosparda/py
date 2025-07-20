from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame.locals import *
from pygame import mixer
import time

alvl = 0
slvl = 0
mlvl = 0
clvl = 0
mlock = 5

window = Tk()
window.title("")
window.geometry("1200x900")
window.option_add("*Background", "#000000")
window.config(bg="#000000")
window.resizable(False,False)

def mathquiz():
    global window
    global result
    global mcount
    mcount = 15
    result = 0 
    #general class for math questions and addition
    class Maths():
        def __init__(self, number1, number2): #numbers for the math question
            self.number1 = number1
            self.number2 = number2
            
        def question(self):
            #displays questions
            return f"what is {self.number1} + {self.number2}"
        
        def answer(self):
            global result
            try:
                answer = int(manswer.get()) #get the number from the input
                if answer == (self.number1)+ (self.number2):
                    result = TRUE
                    return "correct!"
                else:
                    result = FALSE
                    return f"sorry...\nthe answer was {self.number1 + self.number2}"
            except: #for non-integer inputs
                result = FALSE
                return f"sorry...\nthe answer was {self.number1 + self.number2}"

    #category for subtraction questions
    class Subtraction(Maths):
        def question(self):
                #displays questions
                return f"what is {self.number1} - {self.number2}"
            
        def answer(self):
            global result
            try:
                answer = int(manswer.get()) #get the number from the input
                if answer == self.number1 - self.number2:
                    result = TRUE
                    return "correct!"
                else:
                    result = FALSE
                    return f"sorry...the answer was {self.number1 - self.number2}"
            except: #for non-integer inputs
                result = FALSE
                return f"sorry...the answer was {self.number1 - self.number2}"
            
    #category for multiplication questions (only allows for numbers from 1 to 5)
    class Multiplication(Maths):
        def question(self):
            #displays question
            return f"what is {self.number1} x {self.number2}"
            
        def answer(self):
            global result
            try:
                answer = int(manswer.get()) #gets number from input
                if answer == self.number1 * self.number2:
                    result = TRUE
                    return "correct!"
                else:
                    result = FALSE
                    return f"sorry...\nthe answer was {self.number1 * self.number2}"
            except: #for non-integer inputs
                result = FALSE
                return f"sorry...\nthe answer was {self.number1 * self.number2}"

    #category for division questions   
    class Division(Maths):
        def question(self):
            #displays question
            return f"what is {self.number1} / {self.number2}"
        def answer(self):
            global result
            try:
                answer = int(manswer.get()) # gets number from input
                if answer == self.number1/self.number2:
                    result = TRUE
                    return "correct!"
                else:
                    result = FALSE
                    return f"sorry...\nthe answer was {self.number1 / self.number2}"
            except: #for non-integer inputs
                result = FALSE
                return f"sorry...\nthe answer was {self.number1 / self.number2}"
            
    subjects = [Maths, Subtraction, Multiplication, Division] #lists of subjects to refer to 
            
    def askquestion():
        text1 = Label(window, text=question.question(), font=("DotGothic16", 20, "bold"))
        text1.grid(row=1, column=0, padx = 15, sticky="w")

    def checkanswer():
        global mcount
        text2 = Label(window, text=question.answer(), font=("DotGothic16", 15, "bold"), justify=LEFT)
        text2.grid(row=2, column=0, sticky="w", padx=20)
        check.config(text = "continue", command = leave)
        mcount = "done"

    def countdown():
        global mcount
        global after_id
        try :
            int(mcount)
            if mcount >= 0:
                timer.config(text=f"you have {mcount} seconds left!")
                mcount -= 1
                after_id = window.after(1000, countdown)
            else:
                checkanswer()
        except:
            timer.grid_forget

    def leave():
        global window
        global mlock
        if mlvl == 0:
            if result == TRUE:
                window.after_cancel(after_id)
                mlock -= 1
                marea()
                print(mlock)
            else: 
                window.after_cancel(after_id)
                window.destroy()
                window = Tk()
                window.title("maths question")
                window.geometry("400x150")
                window.option_add("*Background", "#000000")
                window.config(bg="#000000")
                window.resizable(False,False)
                mathquiz()
                print(mlock)

    def enterbutton(event):
        if mcount == "done":
            leave()
        else:
            checkanswer()

    def checkint(event):
        currenttext = manswer.get()
        try:
            int(currenttext)
        except:
            manswer.delete(0, 'end')

    # subject = random.randint(0,3)
    subject = 0

    if subject == 2:
        question = subjects[subject](random.randint(1,5), random.randint(1,5))
        
    elif subject == 0:
        question = subjects[subject](random.randint(1,20), random.randint(1,20))

    elif subject ==1:
        a = random.randint(1,20)
        b = random.randint(1,20)
        if a>b:
            question = subjects[subject](a,b)
        else:
            question = subjects[subject](b,a)

    while subject ==3:
        a = random.randint(1,5)
        b = random.randint(1,5)
        if a%b == 0:
            question = subjects[subject](a, b)
            break
        else:
            continue

    timer = Label(window, text=f"you have {mcount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askquestion()
    countdown()
    manswer = Entry(window, bd=3, relief="ridge", width=10)
    manswer.grid(row=1, column=1, sticky="w")
    manswer.bind("<Return>", enterbutton)
    manswer.bind("<Key>", checkint)
    check = Button(window, text="check", command=checkanswer)
    check.grid(row=3, column=0, sticky="w", padx=20)

def marea():
    global lock
    global window
    global lectern
    window.destroy()
    window = Tk()
    window.title("")
    window.geometry("1200x900")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
    if mlock > 0:
        lock_image = Image.open("sprites/lock.png")
        lock = ImageTk.PhotoImage(lock_image)
        lock1 = Button(window, image = lock, command = mtutq)
        lock1.place(x = 100, y = 100)
    else: 
        lectern_image = Image.open("sprites/lectern.png")
        lectern = ImageTk.PhotoImage(lectern_image)
        thelectern = Button(window, image=lectern, command = mfintut)
        thelectern.place(x = 200, y = 200)

def mtutq():
    global lectern
    global result
    global mlock
    global window
    window.destroy()
    window = Tk()
    window.title("maths question")
    window.geometry("400x150")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
    if mlock == 0:
        marea()
    else:
        mathquiz()

def mfintut():
    global mlvl
    mlvl = 1

door_image = Image.open("sprites/door.png")
door = ImageTk.PhotoImage(door_image)
if slvl == 0:
    sdoor = Button(window, image = door)
    sdoor.place(x = 200, y = 100)
if alvl ==0:
    adoor = Button(window, image = door)
    adoor.place(x = 50, y = 400)
if mlvl == 0:
    mdoor = Button(window, image=door, command=marea)
    mdoor.place(x = 800, y = 100)
if clvl ==0:
    cdoor = Button(window, image = door)
    cdoor.place(x = 950, y = 400)
THEdoor = Button(window, image = door)
THEdoor.place(x = 500, y = 50)

mainloop()