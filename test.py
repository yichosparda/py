from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame.locals import *
from pygame import mixer
import time
import json

mixer.init()
correct = mixer.Sound("sounds/correct.mp3")
incorrect = mixer.Sound("sounds/incorrect.mp3")

alvl = 0
slvl = 0
mlvl = 0
clvl = 0
lvls = [mlvl, alvl, slvl, clvl]

xpmultiplier = 1

subjectindex = 'none'

mlock = 3
alock = 3
slock = 3
clock = 3
locks = [mlock, alock, slock, clock]

qsubjects = ["maths", "animal", "shape", "colour"]

dialoguenum = 0
dialogue = ["hi vro u can call me v the overseer of this so called dungeon", 
            "u want to escape?"
            "\n well ur gonna have to fight that big dog cerberus past that door at the end of the hallway "
            "\n but ur definitely too weak rn so ur gonna have to learn a few combat spells from the lecterns scattered around this place", 
            "u can check ur stats by clicking ur profile on the top left "
            "\n and train your spells at the training grounds when u learn some, "
            "\n good luck out there", 
            "", 
            'well this is a surprise, i guess ill have to break the locks for u '
            '\nbut ur gonna need to lend me some of ur energy since im a bit frail in this form',
            "this is the training grounds, i'd say u need to be at least level 20 in all ur stats to face cerberus",
            "u could also find some stray demons around to test ur abilities by pressing the combat trial button"]

spells = ['offensive', 'defensive', 'tactical', 'supportive']
stats = ['attack', 'defence', 'luck', 'health']

image_paths = ["sprites/attack.png", "sprites/defence.png", "sprites/luck.png", "sprites/health.png"]
image_references = []

tg = TRUE

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
    global textbox
    window = Tk()
    window.title("")
    window.geometry("1200x900")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
    textbox_image = Image.open("sprites/textbox.png")
    textbox = ImageTk.PhotoImage(textbox_image)
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
    elif dialoguenum == 4:
        for widget in window.winfo_children():
            widget.destroy()
        profile()
        areasetup()
    elif dialoguenum == 7:
        dialoguenum +=1
        for widget in window.winfo_children():
            widget.destroy()
        tgsetup()
    else:
        vdialogue()

def mathquiz():
    global window
    global result
    global mcount
    global manswer
    window.destroy()
    window = Tk()
    window.title("maths question")
    window.geometry("400x150")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
    mcount = 15
    result = 0 

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
        check.config(text = "continue", command = question.leave)
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

    def enterbutton(event):
        if mcount == "done":
            question.leave()
        else:
            checkanswer()

    def checkint(event):
        currenttext = manswer.get()
        try:
            int(currenttext)
        except:
            manswer.delete(0, 'end')

    subject = random.randint(0,3)
    # subject = 0

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
    
    def leave(self):
        global window
        global mlock
        global locks
        global lvls
        global xpmultiplier
        global after_id
        if lvls[0] == 0:
            if result == TRUE:
                window.after_cancel(after_id)
                mlock -= 1
                locks = [mlock, alock, slock, clock]
                marea()
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
        else: 
            if result == TRUE:
                window.after_cancel(after_id)
                lvls[0] += 1 * xpmultiplier
                locks = [mlock, alock, slock, clock]
                window.destroy()
                windowsetup()
                traininggrounds()
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

def animalsquiz():
    global window
    global result
    global acount
    window.destroy()
    window = Tk()
    window.title("animal question")
    window.geometry("300x270")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)

    animals = ['Bear','Bird','Cat','Dog','Fox','Horse', 'Penguin', 'Raccoon']
    animal = random.randint(0,7)

    acount = 15
    result = 0 

    def leave():
        global window
        global alock
        global locks
        global lvls
        global xpmultiplier
        if lvls[1] == 0:
            if result == TRUE:
                window.after_cancel(after_id)
                alock -= 1
                locks = [mlock, alock, slock, clock]
                aarea()
            else: 
                window.after_cancel(after_id)
                window.destroy()
                window = Tk()
                window.title("animal question")
                window.geometry("300x270")
                window.option_add("*Background", "#000000")
                window.config(bg="#000000")
                window.resizable(False,False)
                animalsquiz()
        else: 
            if result == TRUE:
                window.after_cancel(after_id)
                lvls[1] += 1 * xpmultiplier
                locks = [mlock, alock, slock, clock]
                window.destroy()
                windowsetup()
                traininggrounds()
            else:
                window.after_cancel(after_id)
                window.destroy()
                window = Tk()
                window.title("animal question")
                window.geometry("300x270")
                window.option_add("*Background", "#000000")
                window.config(bg="#000000")
                window.resizable(False,False)
                animalsquiz()

    def countdown():
        global acount
        global after_id
        try :
            int(acount)
            if acount >= 0:
                timer.config(text=f"you have {acount} seconds left!")
                acount -= 1
                after_id = window.after(1000, countdown)
            else:
                animalanswer()
        except:
            timer.grid_forget

    def enterbutton(event):
        if acount == "done":
            leave()
        else:
            animalanswer()

    def animalanswer():
        global result
        global acount
        text2 = 0
        answer = (qanswer.get()).upper()
        if answer == animals[animal].upper():
            text2=Label(window, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(correct)
            acount = "done"
            result = TRUE

        else:
            text2=Label(window, text=f"sorry... it's {animals[animal].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(incorrect)
            acount = "done"
            result = FALSE

    timer = Label(window, text=f"you have {acount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)

    def askanimal():
        global photo
        question = Label(window, text="what animal is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        image = Image.open(f"animals/{animals[animal]}.png")
        resized_image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(resized_image)
        theshape = Label(window, image=photo)
        theshape.grid(row=2, column=0)

    askanimal()
    countdown()
    qanswer = Entry(window, bd=3, relief="ridge", width=10)
    qanswer.grid(row=3, column=0, sticky="w", padx=20)
    qanswer.bind("<Return>", enterbutton)
    check = Button(window, text="check", command=animalanswer)
    check.grid(row=4, column=0, sticky="w", padx=20)

def shapesquiz():
    global scount
    global window
    global result
    window.destroy()
    window = Tk()
    window.title("shape question")
    window.geometry("300x270")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
    result = 0
    shapes = ['Rectangle','Square','Circle','Pentagon','Hexagon','Octagon']
    scount = 15

    def leave():
        global window
        global slock
        global locks
        global lvls
        global xpmultiplier
        if lvls[2] == 0:
            if result == TRUE:
                window.after_cancel(after_id)
                slock -= 1
                locks = [mlock, alock, slock, clock]
                sarea()
            else: 
                window.after_cancel(after_id)
                window.destroy()
                window = Tk()
                window.title("shape question")
                window.geometry("300x270")
                window.option_add("*Background", "#000000")
                window.config(bg="#000000")
                window.resizable(False,False)
                shapesquiz()
        else: 
            if result == TRUE:
                window.after_cancel(after_id)
                lvls[2] += 1 * xpmultiplier
                locks = [mlock, alock, slock, clock]
                window.destroy()
                windowsetup()
                traininggrounds()
            else:
                window.after_cancel(after_id)
                window.destroy()
                window = Tk()
                window.title("shape question")
                window.geometry("300x270")
                window.option_add("*Background", "#000000")
                window.config(bg="#000000")
                window.resizable(False,False)
                shapesquiz()

    def countdown():
        global scount
        global after_id
        try :
            int(scount)
            if scount >= 0:
                timer.config(text=f"you have {scount} seconds left!")
                scount -= 1
                after_id = window.after(1000, countdown)
            else:
                shapeanswer()
        except:
            timer.grid_forget

    shape = random.randint(0,5)

    def enterbutton(event):
        if scount == "done":
            leave()
        else:
            shapeanswer()

    def shapeanswer():
        global scount
        global answer
        global result
        text2 = 0
        answer = (sanswer.get()).upper()
        if answer == "RECTANGLE" and shapes[shape].upper() == "SQUARE":
            text2=Label(window, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(correct)
            scount = "done"
            result = TRUE
            
        elif answer == shapes[shape].upper():
            text2=Label(window, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(correct)
            scount = "done"
            result = TRUE

        else:
            text2=Label(window, text=f"sorry... it's {shapes[shape].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(incorrect)
            scount = "done"
            result = FALSE

    def askshape():
        global photo
        question = Label(window, text="what shape is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        image = Image.open(f"shapes/{shapes[shape]}.png")
        if shape == 0:
            resized_image = image.resize((200, 100))
            photo = ImageTk.PhotoImage(resized_image)
            theshape = Label(window, image=photo)
            theshape.grid(row=2, column=0)
        else: 
            resized_image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(resized_image)
            theshape = Label(window, image=photo)
            theshape.grid(row=2, column=0)

    timer = Label(window, text=f"you have {scount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askshape()
    countdown()
    sanswer = Entry(window, bd=3, relief="ridge", width=10)
    sanswer.grid(row=3, column=0, sticky="w", padx=20)
    sanswer.bind("<Return>", enterbutton)
    check = Button(window, text="check", command=shapeanswer)
    check.grid(row=4, column=0, sticky="w", padx=20)

def coloursquiz():
    global ccount
    global window
    global result
    window.destroy()
    window = Tk()
    window.title("colour question")
    window.geometry("300x160")
    window.option_add("*Background", "#000000")
    window.config(bg="#000000")
    window.resizable(False,False)
    result = 0
    colours = ['Red','Blue','Green','Pink','Black','Yellow','Orange','White','Purple','Brown']
    ccount = 15

    def leave():
        global window
        global clock
        global locks
        global lvls
        global xpmultiplier
        if lvls[3] == 0:
            if result == TRUE:
                window.after_cancel(after_id)
                clock -= 1
                locks = [mlock, alock, slock, clock]
                carea()
            else: 
                window.after_cancel(after_id)
                window.destroy()
                window = Tk()
                window.title("colour question")
                window.geometry("300x160")
                window.option_add("*Background", "#000000")
                window.config(bg="#000000")
                window.resizable(False,False)
                coloursquiz()
        else: 
            if result == TRUE:
                window.after_cancel(after_id)
                lvls[3] += 1 * xpmultiplier
                locks = [mlock, alock, slock, clock]
                window.destroy()
                windowsetup()
                traininggrounds()
            else:
                window.after_cancel(after_id)
                window.destroy()
                window = Tk()
                window.title("colour question")
                window.geometry("300x160")
                window.option_add("*Background", "#000000")
                window.config(bg="#000000")
                window.resizable(False,False)
                coloursquiz()

    def countdown():
        global ccount
        global after_id
        try :
            int(ccount)
            if ccount >= 0:
                timer.config(text=f"you have {ccount} seconds left!")
                ccount -= 1
                after_id = window.after(1000, countdown)
            else:
                colouranswer()
        except:
            timer.grid_forget

    colour = random.randint(0,9)

    def enterbutton(event):
        global ccount
        if ccount == "done":
            leave()
        else:
            colouranswer()

    def askcolour():
        question = Label(window, text="what colour is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        thecolour = Label(window, text="---", fg=colours[colour], bg=colours[colour], font=("DotGothic16", 12, "bold"), relief="raised")
        thecolour.grid(row=1, column=1)

    def colouranswer():
        global ccount
        global answer
        global result
        text2 = 0
        answer = (canswer.get()).upper()
        if answer == colours[colour].upper():
            text2=Label(window, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=3, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 4, column=0)
            mixer.Sound.play(correct)
            result = TRUE
            ccount = "done"
        else:
            text2=Label(window, text=f"sorry... it's {colours[colour].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=3, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 4, column=0)
            mixer.Sound.play(incorrect)
            result = FALSE
            ccount = "done"

    timer = Label(window, text=f"you have {ccount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askcolour()
    countdown()
    canswer = Entry(window, bd=3, relief="ridge", width=10)
    canswer.grid(row=2, column=0, sticky="w", padx=20)
    canswer.bind("<Return>", enterbutton)
    check = Button(window, text="check", command=colouranswer)
    check.grid(row=3, column=0, sticky="w", padx=20)

quizes = [mathquiz, animalsquiz, shapesquiz, coloursquiz]

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
    global lock
    global lectern
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
    global neropfp
    global window
    nero_image = Image.open("sprites/nero.png")
    rnero_image = nero_image.resize((100, 100))
    nero = ImageTk.PhotoImage(rnero_image)
    neropfp = Button(window, image=nero, command = showstats)
    neropfp.place(x= 30, y = 30)
    nerotext = Label(window, text="stats")
    nerotext.place(x=30, y=150)

def marea():
    global window
    global subjectindex
    subjectindex = 0
    window.destroy()
    windowsetup()
    profile()
    if mlock == 1 and slock ==1 and clock ==1 and alock ==1:
        vdialogue()
    else:
        areasetup()

def aarea():
    global window
    global subjectindex
    subjectindex = 1
    window.destroy()
    windowsetup()
    profile()
    if mlock == 1 and slock ==1 and clock ==1 and alock ==1:
        vdialogue()
    else:
        areasetup()

def sarea():
    global window
    global subjectindex
    subjectindex = 2
    window.destroy()
    windowsetup()
    profile()
    if mlock == 1 and slock ==1 and clock ==1 and alock ==1:
        vdialogue()
    else:
        areasetup()

def carea():
    global window
    global subjectindex
    subjectindex = 3
    window.destroy()
    windowsetup()
    profile()
    if mlock == 1 and slock ==1 and clock ==1 and alock ==1:
        vdialogue()
    else:
        areasetup()

areas = [marea, aarea, sarea, carea]

def fintut():
    global lvls
    global subjectindex
    global textbox
    global mlvl
    textbox_image = Image.open("sprites/textbox.png")
    textbox = ImageTk.PhotoImage(textbox_image)
    thetextbox = Button(window, image=textbox, command = tgunlock)
    thetextbox.place(relx=0.5, y = 700 ,anchor=CENTER)
    if lvls[subjectindex] == 0:
        vtext = Label(window, text = f'congrats! you have learnt {spells[subjectindex]} spells u can now use them to increase your {stats[subjectindex]} stat')
        vtext.place(relx=0.5, y = 700 ,anchor=CENTER)
        lvls[subjectindex] = 1
        print(lvls[subjectindex])
    else: 
        vtext = Label(window, text = 'spell already learnt')
        vtext.place(relx=0.5, y = 700 ,anchor=CENTER)

def doors():
    global door
    global window
    door_image = Image.open("sprites/door.png")
    door = ImageTk.PhotoImage(door_image)
    mdoor = Button(window, image=door, command=marea)
    mdoor.place(x = 800, y = 100)
    sdoor = Button(window, image = door, command= sarea)
    sdoor.place(x = 200, y = 100)
    adoor = Button(window, image = door, command=aarea)
    adoor.place(x = 50, y = 400)
    cdoor = Button(window, image = door, command= carea)
    cdoor.place(x = 950, y = 400)
    THEdoor = Button(window, image = door)
    THEdoor.place(x = 500, y = 50)

def showstats():
    global window
    global statwin
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

def tgunlock():
    global textbox
    global tg
    if sum(lvls) == 4:
        textbox_image = Image.open("sprites/textbox.png")
        textbox = ImageTk.PhotoImage(textbox_image)
        thetextbox = Button(window, image=textbox, command = lobby)
        thetextbox.place(relx=0.5, y = 700 ,anchor=CENTER)
        text1 = Label(window, text = "training grounds is now unlocked")
        text1.place(relx=0.5, y = 700 ,anchor=CENTER)
        tg = TRUE
    else:
        lobby()

def tgicon():
    global window
    global tgimg
    tg_image = Image.open("sprites/tg.png")
    rtg_image = tg_image.resize((150, 150))
    tgimg = ImageTk.PhotoImage(rtg_image)
    tgicon = Button(window, image=tgimg, command = tgverify)
    tgicon.place(x= 1000, y = 30)

def tgverify():
    global textbox
    if tg == TRUE:
        traininggrounds()
    else:
        textbox_image = Image.open("sprites/textbox.png")
        textbox = ImageTk.PhotoImage(textbox_image)
        thetextbox = Button(window, image=textbox, command = lobby)
        thetextbox.place(relx=0.5, y = 700 ,anchor=CENTER)
        text1 = Label(window, text = "learn spells to access training grounds")
        text1.place(relx=0.5, y = 700 ,anchor=CENTER)

def traininggrounds():
    global lvls
    for widget in window.winfo_children():
            widget.destroy()
    if sum(lvls) == 4:
        vdialogue()
    else:
        home = Button(window, text='home', command=lobby)
        home.pack(pady= 30)
        tgsetup()

def tgsetup():
    global lvls
    statlist = Label(window, text=f"attack lvl = {lvls[0]}     defence lvl = {lvls[1]}     luck lvl = {lvls[2]}      health lvl = {lvls[3]}")
    statlist.pack(pady=20)
    loadicons()
    for x in range(0,4):
        frame = Frame(window)
        frame.pack(anchor=N, pady=10)
        icons = Button(frame, image=image_references[x], command=quizes[x])
        icons.pack(side=TOP,padx= 20)
        desc = Label(frame, text = f'{stats[x]} training\n {qsubjects[x]} questions', font=("DotGothic16", 15, "bold"))
        desc.pack()
    combatfrm = Frame(window)
    combatfrm.pack(anchor=CENTER)
    combatstart = Button(combatfrm, text="combat trial", command=combatsetup)
    combatstart.pack()
    combatdesc = Label(combatfrm, text= "use combination of all spells to face off minor enemies\n offers double xp")
    combatdesc.pack()

def combatsetup():
    global nero
    global window
    global textbox
    for widget in window.winfo_children():
        widget.destroy()

    

    thetextbox = Label(window, image=textbox)
    thetextbox.place(relx=0.5, y = 100 ,anchor=CENTER)

    combattext = Label(window, text = "player turn")
    combattext.place(relx=0.5, y=100, anchor=CENTER)

    nero_image = Image.open("sprites/nero.png")
    rnero_image = nero_image.resize((150, 150))
    nero = ImageTk.PhotoImage(rnero_image)
    combatpfp = Label(window, image=nero)
    combatpfp.place(x = 50, y = 700)


# class Enemy():
#     def __init__(self, name):
#         self.name = enemyname
    
def lobby():
    for widget in window.winfo_children():
        widget.destroy()
    doors()
    profile()
    tgicon()

beginning()

mainloop()