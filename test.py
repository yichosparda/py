from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame.locals import *
from pygame import mixer
import time

mixer.init()
correct = mixer.Sound("sounds/correct.mp3")
incorrect = mixer.Sound("sounds/incorrect.mp3")

alvl = 0
slvl = 0
mlvl = 0
clvl = 0
lvls = [mlvl, alvl, slvl, clvl]

subjectindex = 'none'

mlock = 5
alock = 5
slock = 5
clock = 5
locks = [mlock, alock, slock, clock]

dialoguenum = 0
dialogue = ["hi vro u can call me v the overseer of this so called dungeon", 
            "u want to escape?"
            "\n well ur gonna have to fight that big dog cerberus past that door at the end of the hallway "
            "\n but ur definitely too weak rn so ur gonna have to learn a few combat spells from the lecterns scattered around this place", 
            "u can check ur stats by clicking ur profile on the top left "
            "\n and train your spells in the infested gardens when u learn some, "
            "\n good luck out there", "", 'well this is a surprise, i guess ill have to break the locks for u '
            '\nbut ur gonna need to lend me some of ur energy since im a bit frail in this form']

spells = ['offensive', 'defensive', 'tactical', 'supportive']
stats = ['attack', 'defence', 'luck', 'health']

image_paths = ["sprites/attack.png", "sprites/defence.png", "sprites/luck.png", "sprites/health.png"]
image_references = []

def loadicons():
    global photo
    global image_references
    global image_paths
    image_references.clear()
    for x in range(0,4):
        img = Image.open(image_paths[x])
        img = img.resize((70, 70))
        photo = ImageTk.PhotoImage(img)
        image_references.append(photo)

def windowsetup():
    global window
    window = Tk()
    window.title("")
    window.geometry("1200x900")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
windowsetup()

def vdialogue():
    global textbox
    global v
    global window
    global vtext
    v_image = Image.open("sprites/v.png")
    v = ImageTk.PhotoImage(v_image)
    vphoto = Label(window, image = v)
    vphoto.place(x = 700, y = 200)
    textbox_image = Image.open("sprites/textbox.png")
    textbox = ImageTk.PhotoImage(textbox_image)
    thetextbox = Button(window, image=textbox, command = nexttext)
    thetextbox.place(relx=0.5, y = 700 ,anchor=CENTER)
    vtext = Label(window, text = dialogue[dialoguenum])
    vtext.place(relx=0.5, y = 700 ,anchor=CENTER)

def nexttext():
    global dialoguenum
    global vtext
    dialoguenum += 1
    vtext.destroy()
    if dialoguenum == 3:
        lobby()
        dialoguenum +=1
    elif dialoguenum == 5:
        for widget in window.winfo_children():
            widget.destroy()
        profile()
        areasetup()
    else:
        vdialogue()

def mathquiz():
    global window
    global result
    global mcount
    window.destroy()
    window = Tk()
    window.title("maths question")
    window.geometry("400x150")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
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
        global result
        text2 = Label(window, text=question.answer(), font=("DotGothic16", 15, "bold"), justify=LEFT)
        text2.grid(row=2, column=0, sticky="w", padx=20)
        if result == TRUE:
            mixer.Sound.play(correct)
        else: mixer.Sound.play(incorrect)
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
        global locks
        if mlvl == 0:
            if result == TRUE:
                window.after_cancel(after_id)
                mlock -= 1
                locks = [mlock, alock, slock, clock]
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

quizes = [mathquiz]

def tutq():
    global locks
    global subjectindex
    global areas
    global quizes
    if locks[subjectindex] == 0:
        areas[subjectindex]()
    else:
        quizes[subjectindex]()

def areasetup():
    global subjectindex
    global mlock
    global lock
    global lectern
    print(locks[subjectindex])
    if locks[subjectindex] > 0:
        lock_image = Image.open("sprites/lock.png")
        lock = ImageTk.PhotoImage(lock_image)
        lock1 = Button(window, image = lock, command = tutq)
        lock1.place(relx=0.5, rely = 0.5 ,anchor=CENTER)
    else: 
        lectern_image = Image.open("sprites/lectern.png")
        lectern = ImageTk.PhotoImage(lectern_image)
        thelectern = Button(window, image=lectern, command = fintut)
        thelectern.place(relx=0.5, rely = 0.5 ,anchor=CENTER)

def profile():
    global nero
    global window
    global neropfp
    nero_image = Image.open("sprites/nero.png")
    rnero_image = nero_image.resize((100, 100))
    nero = ImageTk.PhotoImage(rnero_image)
    neropfp = Button(window, image=nero, command = showstats)
    neropfp.place(x= 30, y = 30)

def marea():
    global window
    global subjectindex
    subjectindex = 0
    window.destroy()
    windowsetup()
    profile()
    if mlock == 5 and slock ==5 and clock ==5 and alock ==5:
        vdialogue()
    else:
        areasetup()

areas = [marea]

def fintut():
    global lvls
    global subjectindex
    global textbox
    lvls[subjectindex] = 1
    print(lvls)
    textbox_image = Image.open("sprites/textbox.png")
    textbox = ImageTk.PhotoImage(textbox_image)
    thetextbox = Button(window, image=textbox, command = lobby)
    thetextbox.place(relx=0.5, y = 700 ,anchor=CENTER)
    vtext = Label(window, text = f'congrats! you have learnt {spells[subjectindex]} spells u can now use them to increase your ')
    vtext.place(relx=0.5, y = 700 ,anchor=CENTER)

def doors():
    global door
    global window
    global mlvl
    global alvl
    global clvl
    global slvl
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

def showstats():
    global window
    global statwin
    global photo
    global neropfp
    statwin = Toplevel(window)
    statwin.title("account")
    statwin.geometry("350x430")
    statwin.option_add("*Background", "#000000")
    statwin.config(bg="#000000")
    statwin.resizable(False,False)
    neropfp.config(command = closestats)
    loadicons()
    for x in range(0,4):
        frame = Frame(statwin)
        frame.pack(anchor=W)
        label = Label(frame, image=image_references[x])
        label.pack(side=LEFT,padx= 20, pady= 10)
        lvlnum = Label(frame, text = f'{stats[x]} level = {lvls[x]}', font=("DotGothic16", 20, "bold"))
        lvlnum.pack(side = LEFT)
    quitstat = Button(statwin, text = "close", command=closestats)
    quitstat.pack()

def closestats():
    global neropfp
    global statwin
    statwin.destroy()
    neropfp.config(command = showstats)

def beginning():
    profile()
    vdialogue()

def lobby():
    for widget in window.winfo_children():
        widget.destroy()
    doors()
    profile()

beginning()

mainloop()