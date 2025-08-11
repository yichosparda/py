from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame.locals import *
from pygame import mixer
import time
import json

#loading sound effects
mixer.init()
correct = mixer.Sound("sounds/correct.mp3")
incorrect = mixer.Sound("sounds/incorrect.mp3")
select = mixer.Sound("sounds/select.mp3")
death = mixer.Sound("sounds/death.mp3")
boom = mixer.Sound("sounds/boom.mp3")

#stores backgrounds
backgrounds = ['startup','lobbybg', 'tutarea', 'tg', 'combat', 'tutstart']

#storing enemy and enemy types
enemies = ['slime', 'spider', 'cerberus']
enemyhp = [random.randint(50,60), random.randint(70,90), 500] #randomises enemy hp to some extent
enemyatk = [20, 30, 200]

#skill/quiz/spell levels for player
#saved using json
alvl = 0
slvl = 0
mlvl = 0
clvl = 0
lvls = [mlvl, alvl, slvl, clvl] #storing levels to refer to later 

xpmultiplier = 1 #multiplies xp gained after and enemy level/strength

subjectindex = 'none' #determines type of quiz

#completion level of each tutorial stage
#save using json
mlock = 3
alock = 3
slock = 3
clock = 3
locks = [mlock, alock, slock, clock] #storing completion levels

qsubjects = ["maths", "animal", "shape", "colour"] #types of quizes

dialoguenum = 0 #dialogue process/index
#dialogue dictionary
dialogue = ["hi vr", 
            "u want to escape?"
            "\n well ur gonna have to fight that big dog cerberus past that door at the end of the hallway "
            "\n but ur definitely too weak rn so ur gonna have to learn a few combat spells from the lecterns scattered around this place", 
            "u can check ur stats by clicking ur profile on the top left "
            "\n and train your spells at the training grounds when u learn some, "
            "\n good luck", 
            "", 
            'well this is a surprise, i guess ill have to break the locks for u '
            '\nbut ur gonna need to lend me some of ur energy since im a bit frail in this form',
            "this is the training grounds, i'd say u need to be at least level 20 in all ur stats to face cerberus",
            "u could also find some stray demons around to test ur abilities by pressing the combat trial button"]

spells = ['offensive', 'defensive', 'tactical', 'supportive'] #types of spells
stats = ['attack', 'defence', 'luck', 'health'] #player stats

#paths for loading stat icons later
image_paths = ["sprites/attack.png", "sprites/defence.png", "sprites/luck.png", "sprites/health.png"]
image_references = [] #storing images to prevent garbage collection

tg = TRUE #whether or not training grounds is unlocked
combat = FALSE #whether or not in combat

class Background():
    def __init__(self, index):
        self.index = index
    
    def load(self):
        global bgimage
        bgimage=ImageTk.PhotoImage(Image.open(f'backgrounds/{backgrounds[self.index]}.png'))
        currentbg = Label(window, image=bgimage)
        currentbg.place(anchor=CENTER, relx=0.5, rely=0.5)

def loadicons():
    global photo
    global image_references
    global stats
    image_references.clear()
    for x in range(0,4):
        img = Image.open(f'sprites/{stats[x]}icon.png')
        img = img.resize((70, 70))
        photo = ImageTk.PhotoImage(img)
        image_references.append(photo)

def windowsetup():
    global window
    global textbox
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
    
windowsetup()

def vdialogue():
    global textbox
    global v
    global window
    global vtext
    global vbg
    global currentbg
    global backgrounds

    v = ImageTk.PhotoImage(Image.open("sprites/v.png"))
    vbg = ImageTk.PhotoImage(Image.open(f"backgrounds/{backgrounds[currentbg.index]}.png")) 
    canvas = Canvas(window, width = 1200, height=900, highlightthickness=0)
    canvas.create_image(1200, 900, image=vbg, anchor = SE)
    canvas.create_image(1200, 900, image=v,anchor = SE)
    canvas.place(anchor=CENTER, relx=0.5, rely=0.5)

    thetextbox = Button(window, image=textbox, command = nexttext)
    thetextbox.place(relx=0.5, rely = 0.82 ,anchor=CENTER)
    vtext = Label(window, text = dialogue[dialoguenum])
    vtext.place(relx=0.5, rely=0.82 ,anchor=CENTER)
    profile()
    tgicon()

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
    elif dialoguenum == 7:
        dialoguenum +=1
        for widget in window.winfo_children():
            widget.destroy()
        tgsetup()
    else:
        vdialogue()

def mathquiz():
    global qwindow
    global result
    global mcount
    global manswer
    for widget in window.winfo_children():
        if isinstance(widget, (Button, ttk.Button)):
            widget.config(state="disabled")
    qwindow = Toplevel(window)
    qwindow.title("maths question")
    qwindow_width = 450
    qwindow_height = 150
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (qwindow_width / 2))
    y_coordinate = int((screen_height / 2) - (qwindow_height / 2))
    qwindow.geometry(f"{qwindow_width}x{qwindow_height}+{x_coordinate}+{y_coordinate}")
    qwindow.option_add("*Background", "#000000")
    qwindow.config(bg="#000000")
    qwindow.resizable(False,False)
    mcount = 15
    result = 0 

    def askquestion():
        text1 = Label(qwindow, text=question.question(), font=("DotGothic16", 20, "bold"))
        text1.grid(row=1, column=0, padx = 15, sticky="w")

    def checkanswer():
        global mcount
        global result
        text2 = Label(qwindow, text=question.answer(), font=("DotGothic16", 15, "bold"), justify=LEFT)
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
                after_id = qwindow.after(1000, countdown)
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

    timer = Label(qwindow, text=f"you have {mcount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askquestion()
    countdown()
    manswer = Entry(qwindow, bd=3, relief="ridge", width=10)
    manswer.grid(row=1, column=1, sticky="w")
    manswer.bind("<Return>", enterbutton)
    manswer.bind("<Key>", checkint)
    check = Button(qwindow, text="check", command=checkanswer)
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
        global qwindow
        global questiontally
        global window
        global mlock
        global locks
        global lvls
        global hpbar1
        global hpbar2
        if combat == FALSE:
            if lvls[0] == 0:
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    mlock -= 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy()
                    marea()
                else: 
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    mathquiz()
            else: 
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    lvls[0] += 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy()
                    traininggrounds()
                else:
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    mathquiz()
        else:
            if result ==TRUE:
                questiontally =+ 1
                print(questiontally)
                for widget in window.winfo_children():
                    if isinstance(widget, (Button, ttk.Button)):
                        widget.config(state="active")
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                if healthbar_id==0:
                    hpbar1.takedamage()
                elif healthbar_id==1:
                    hpbar2.takedamage()
            else:
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                enemy.enemyturn()

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
    global qwindow
    global result
    global acount
    for widget in window.winfo_children():
        if isinstance(widget, (Button, ttk.Button)):
            widget.config(state="disabled")
    qwindow = Toplevel(window)
    qwindow.title("animal question")
    qwindow_width = 300
    qwindow_height = 270
    screen_width = qwindow.winfo_screenwidth()
    screen_height = qwindow.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (qwindow_width / 2))
    y_coordinate = int((screen_height / 2) - (qwindow_height / 2))
    qwindow.geometry(f"{qwindow_width}x{qwindow_height}+{x_coordinate}+{y_coordinate}")
    qwindow.option_add("*Background", "#000000")
    qwindow.config(bg="#000000")
    qwindow.resizable(False,False)

    animals = ['Bear','Bird','Cat','Dog','Fox','Horse', 'Penguin', 'Raccoon']
    animal = random.randint(0,7)

    acount = 15
    result = 0 

    def leave():
        global qwindow
        global questiontally
        global window
        global alock
        global locks
        global lvls
        global hpbar1
        global hpbar2
        if combat == FALSE:
            if lvls[1] == 0:
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    alock -= 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy()
                    aarea()
                else: 
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    animalsquiz()
            else: 
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    lvls[1] += 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy()
                    traininggrounds()
                else:
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    animalsquiz()
        else:
            if result ==TRUE:
                questiontally =+ 1
                print(questiontally)
                for widget in window.winfo_children():
                    if isinstance(widget, (Button, ttk.Button)):
                        widget.config(state="active")
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                if healthbar_id==0:
                    hpbar1.takedamage()
                elif healthbar_id==1:
                    hpbar2.takedamage()
            else:
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                enemy.enemyturn()

    def countdown():
        global acount
        global after_id
        try :
            int(acount)
            if acount >= 0:
                timer.config(text=f"you have {acount} seconds left!")
                acount -= 1
                after_id = qwindow.after(1000, countdown)
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
            text2=Label(qwindow, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(correct)
            acount = "done"
            result = TRUE

        else:
            text2=Label(qwindow, text=f"sorry... it's {animals[animal].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(incorrect)
            acount = "done"
            result = FALSE

    timer = Label(qwindow, text=f"you have {acount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)

    def askanimal():
        global aphoto
        question = Label(qwindow, text="what animal is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        image = Image.open(f"animals/{animals[animal]}.png")
        resized_image = image.resize((100, 100))
        aphoto = ImageTk.PhotoImage(resized_image)
        theshape = Label(qwindow, image=aphoto)
        theshape.image = aphoto
        theshape.grid(row=2, column=0)

    askanimal()
    countdown()
    qanswer = Entry(qwindow, bd=3, relief="ridge", width=10)
    qanswer.grid(row=3, column=0, sticky="w", padx=20)
    qanswer.bind("<Return>", enterbutton)
    check = Button(qwindow, text="check", command=animalanswer)
    check.grid(row=4, column=0, sticky="w", padx=20)

def shapesquiz():
    global scount
    global qwindow
    global result
    for widget in window.winfo_children():
        if isinstance(widget, (Button, ttk.Button)):
            widget.config(state="disabled")
    qwindow = Toplevel(window)
    qwindow.title("shape question")
    qwindow_width = 300
    qwindow_height = 270
    screen_width = qwindow.winfo_screenwidth()
    screen_height = qwindow.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (qwindow_width / 2))
    y_coordinate = int((screen_height / 2) - (qwindow_height / 2))
    qwindow.geometry(f"{qwindow_width}x{qwindow_height}+{x_coordinate}+{y_coordinate}")
    qwindow.option_add("*Background", "#000000")
    qwindow.config(bg="#000000")
    qwindow.resizable(False,False)
    result = 0
    shapes = ['Rectangle','Square','Circle','Pentagon','Hexagon','Octagon']
    scount = 15

    def leave():
        global qwindow
        global questiontally
        global window
        global slock
        global locks
        global lvls
        global hpbar1
        global hpbar2
        if combat == FALSE:
            if lvls[2] == 0:
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    slock -= 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy()
                    sarea()
                else: 
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    shapesquiz()
            else: 
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    lvls[2] += 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy
                    traininggrounds()
                else:
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    shapesquiz()
        else:
            if result ==TRUE:
                questiontally =+ 1
                print(questiontally)
                for widget in window.winfo_children():
                    if isinstance(widget, (Button, ttk.Button)):
                        widget.config(state="active")
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                if healthbar_id==0:
                    hpbar1.takedamage()
                elif healthbar_id==1:
                    hpbar2.takedamage()
            else:
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                enemy.enemyturn()

    def countdown():
        global scount
        global after_id
        try :
            int(scount)
            if scount >= 0:
                timer.config(text=f"you have {scount} seconds left!")
                scount -= 1
                after_id = qwindow.after(1000, countdown)
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
            text2=Label(qwindow, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(correct)
            scount = "done"
            result = TRUE
            
        elif answer == shapes[shape].upper():
            text2=Label(qwindow, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(correct)
            scount = "done"
            result = TRUE

        else:
            text2=Label(qwindow, text=f"sorry... it's {shapes[shape].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            mixer.Sound.play(incorrect)
            scount = "done"
            result = FALSE

    def askshape():
        global photo
        question = Label(qwindow, text="what shape is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        image = Image.open(f"shapes/{shapes[shape]}.png")
        if shape == 0:
            resized_image = image.resize((200, 100))
            photo = ImageTk.PhotoImage(resized_image)
            theshape = Label(qwindow, image=photo)
            theshape.grid(row=2, column=0)
        else: 
            resized_image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(resized_image)
            theshape = Label(qwindow, image=photo)
            theshape.grid(row=2, column=0)

    timer = Label(qwindow, text=f"you have {scount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askshape()
    countdown()
    sanswer = Entry(qwindow, bd=3, relief="ridge", width=10)
    sanswer.grid(row=3, column=0, sticky="w", padx=20)
    sanswer.bind("<Return>", enterbutton)
    check = Button(qwindow, text="check", command=shapeanswer)
    check.grid(row=4, column=0, sticky="w", padx=20)

def coloursquiz():
    global qwindow
    global result
    global ccount
    for widget in window.winfo_children():
        if isinstance(widget, (Button, ttk.Button)):
            widget.config(state="disabled")
    qwindow = Toplevel(window)
    qwindow.title("colour question")
    qwindow_width = 300
    qwindow_height = 160
    screen_width = qwindow.winfo_screenwidth()
    screen_height = qwindow.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (qwindow_width / 2))
    y_coordinate = int((screen_height / 2) - (qwindow_height / 2))
    qwindow.geometry(f"{qwindow_width}x{qwindow_height}+{x_coordinate}+{y_coordinate}")
    qwindow.option_add("*Background", "#000000")
    qwindow.config(bg="#000000")
    qwindow.resizable(False,False)
    result = 0
    colours = ['Red','Blue','Green','Pink','Black','Yellow','Orange','White','Purple','Brown']
    ccount = 15

    def leave():
        global qwindow
        global questiontally
        global window
        global clock
        global locks
        global lvls
        global hpbar1
        global hpbar2
        if combat == FALSE:
            if lvls[3] == 0:
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    clock -= 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy()
                    carea()
                else: 
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    coloursquiz()
            else: 
                if result == TRUE:
                    qwindow.after_cancel(after_id)
                    lvls[3] += 1
                    locks = [mlock, alock, slock, clock]
                    qwindow.destroy()
                    traininggrounds()
                else:
                    qwindow.after_cancel(after_id)
                    qwindow.destroy()
                    coloursquiz()
        else:
            if result ==TRUE:
                questiontally =+ 1
                print(questiontally)
                for widget in window.winfo_children():
                    if isinstance(widget, (Button, ttk.Button)):
                        widget.config(state="active")
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                if healthbar_id==0:
                    hpbar1.takedamage()
                elif healthbar_id==1:
                    hpbar2.takedamage()
            else:
                qwindow.after_cancel(after_id)
                qwindow.destroy()
                enemy.enemyturn()

    def countdown():
        global ccount
        global after_id
        try :
            int(ccount)
            if ccount >= 0:
                timer.config(text=f"you have {ccount} seconds left!")
                ccount -= 1
                after_id = qwindow.after(1000, countdown)
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
        question = Label(qwindow, text="what colour is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        thecolour = Label(qwindow, text="---", fg=colours[colour], bg=colours[colour], font=("DotGothic16", 12, "bold"), relief="raised")
        thecolour.grid(row=1, column=1)

    def colouranswer():
        global ccount
        global answer
        global result
        text2 = 0
        answer = (canswer.get()).upper()
        if answer == colours[colour].upper():
            text2=Label(qwindow, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=3, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 4, column=0)
            mixer.Sound.play(correct)
            result = TRUE
            ccount = "done"
        else:
            text2=Label(qwindow, text=f"sorry... it's {colours[colour].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=3, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 4, column=0)
            mixer.Sound.play(incorrect)
            result = FALSE
            ccount = "done"

    timer = Label(qwindow, text=f"you have {ccount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askcolour()
    countdown()
    canswer = Entry(qwindow, bd=3, relief="ridge", width=10)
    canswer.grid(row=2, column=0, sticky="w", padx=20)
    canswer.bind("<Return>", enterbutton)
    check = Button(qwindow, text="check", command=colouranswer)
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
    global currentbg
    global theorb
    global orb
    global lvls
    currentbg = Background(2)
    currentbg.load()
    profile()
    if locks[subjectindex] > 0:
        lock_image = Image.open("sprites/lock.png")
        lock = ImageTk.PhotoImage(lock_image)
        lock1 = Button(window, width =602, height = 686, image = lock, command = tutq)
        lock1.image = lock
        lock1.place(relx=0.5, rely = 0.385 ,anchor=CENTER)
        indicator = Label(window, text=locks[subjectindex], font=("DotGothic16", 15, "bold"), bg='#423354') 
        indicator.place(anchor=CENTER, relx=0.5, rely= 0.2)
    else: 
        lectern_image = Image.open("sprites/lectern.png")
        lectern = ImageTk.PhotoImage(lectern_image)
        thelectern = Button(window, width = 320, height = 347, image=lectern, command = fintut)
        thelectern.place(relx=0.5, rely = 0.558 ,anchor=CENTER)
        orb = ImageTk.PhotoImage(Image.open(f'sprites/{stats[subjectindex]}icon.png'))
        if lvls[subjectindex] == 0:
            theorb = Label(window, image =orb, bg='#423354')
            theorb.place(anchor = CENTER, relx=0.5, rely=0.3)

def profile():
    global nero
    global neropfp
    global window
    nero_image = Image.open("sprites/nero.png")
    nero = ImageTk.PhotoImage(nero_image)
    neropfp = Button(window, width =179, height=179, image=nero, command = showstats)
    neropfp.image = nero
    neropfp.place(x= 30, y = 30)

def marea():
    global subjectindex
    subjectindex = 0
    for widget in window.winfo_children():
        widget.destroy()
    global currentbg
    currentbg = Background(5)
    currentbg.load()

    profile()
    if mlock == 3 and slock ==3 and clock ==3 and alock ==3:
        vdialogue()
    else:
        areasetup()

def aarea():
    global subjectindex
    subjectindex = 1
    for widget in window.winfo_children():
        widget.destroy()
    global currentbg
    currentbg = Background(5)
    currentbg.load()
    profile()
    if mlock == 3 and slock ==3 and clock ==3 and alock ==3:
        vdialogue()
    else:
        areasetup()

def sarea():
    global window
    global subjectindex
    subjectindex = 2
    for widget in window.winfo_children():
        widget.destroy()
    global currentbg
    currentbg = Background(5)
    currentbg.load()
    profile()
    if mlock == 3 and slock ==3 and clock ==3 and alock ==3:
        vdialogue()
    else:
        areasetup()

def carea():
    global window
    global subjectindex
    subjectindex = 3
    for widget in window.winfo_children():
        widget.destroy()
    global currentbg
    currentbg = Background(5)
    currentbg.load()
    profile()
    if mlock == 3 and slock ==3 and clock ==3 and alock ==3:
        vdialogue()
    else:
        areasetup()

areas = [marea, aarea, sarea, carea]

def fintut():
    global lvls
    global subjectindex
    global textbox
    global mlvl
    global theorb
    textbox_image = Image.open("sprites/textbox.png")
    textbox = ImageTk.PhotoImage(textbox_image)
    thetextbox = Button(window, image=textbox, command = tgunlock)
    thetextbox.place(relx=0.5, y = 700 ,anchor=CENTER)
    if lvls[subjectindex] == 0:
        vtext = Label(window, text = f'congrats! you have learnt {spells[subjectindex]} spells u can now use them to increase your {stats[subjectindex]} stat')
        vtext.place(relx=0.5, y = 700 ,anchor=CENTER)
        lvls[subjectindex] = 1
        theorb.destroy()
    else: 
        vtext = Label(window, text = 'spell already learnt')
        vtext.place(relx=0.5, y = 700 ,anchor=CENTER)

def doors():
    global mdoor
    global sdoor
    global cdoor
    global adoor
    global window
    global bdoor
    global lvls
    global dialoguenum
    
    bdoor = ImageTk.PhotoImage(Image.open('sprites/bossdoor.png'))
    thebdoor = Button(window, image=bdoor, width=260, height=356, state=DISABLED)
    thebdoor.place(anchor=CENTER, relx=0.5, rely=0.3)
    if lvls[2]==0:
        sdoor = ImageTk.PhotoImage(Image.open('sprites/sdoor.png'))
    else:
        sdoor = ImageTk.PhotoImage(Image.open('sprites/offsdoor.png'))
    thesdoor = Button(window, image=sdoor, width=173, height=503, command=sarea)
    thesdoor.place(anchor=CENTER, relx=0.276, rely=0.458)
    if lvls[0]==0:
        mdoor = ImageTk.PhotoImage(Image.open('sprites/mdoor.png'))
    else:
        mdoor = ImageTk.PhotoImage(Image.open('sprites/offmdoor.png'))
    themdoor = Button(window, image=mdoor, width=173, height=503, command=marea)
    themdoor.place(anchor=CENTER, relx=0.724, rely=0.458)
    if lvls[1]==0:
        adoor = ImageTk.PhotoImage(Image.open('sprites/adoor.png'))
    else:
        adoor = ImageTk.PhotoImage(Image.open('sprites/offadoor.png'))
    theadoor = Button(window, image=adoor, width=164, height=646, command=aarea)
    theadoor.place(anchor=CENTER, relx=0.0725, rely=0.635)
    if lvls[3]==0:
        cdoor = ImageTk.PhotoImage(Image.open('sprites/cdoor.png'))
    else:
        cdoor = ImageTk.PhotoImage(Image.open('sprites/offcdoor.png'))
    thecdoor = Button(window, image=cdoor, width=164, height=646, command=carea)
    thecdoor.place(anchor=CENTER, relx=0.9275, rely=0.635)

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
    global currentbg
    currentbg=Background(0)
    currentbg.load()
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
    global dialoguenum 
    global tgimg
    tg_image = Image.open("sprites/tg.png")
    tgimg = ImageTk.PhotoImage(tg_image)
    tgicon = Button(window, image=tgimg, command = tgverify)
    tgicon.place(x= 985, y = 25)
    if dialoguenum < 3:
        tgicon.config(state=DISABLED)

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
    global currentbg
    for widget in window.winfo_children():
            widget.destroy()
    currentbg = Background(3)
    currentbg.load()
    if sum(lvls) == 4:
        vdialogue()
    else:
        tgsetup()

def tgsetup():
    global lvls
    global currentbg
    currentbg = Background(3)
    currentbg.load()
    tgcanvas = Canvas(window, width=1200, height=900)
    tgcanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    tgcanvas.create_image(0, 0, anchor =NW, image=bgimage)
    homebutton = Button(window, text='lobby', command=lobby, fg="#000000", font=("DotGothic16", 15, "bold")) #draw image for this later)
    homebutton.place(anchor=CENTER, relx=0.5, rely=0.025)
    tgcanvas.create_text(600, 100, anchor=N, text=f"attack lvl = {lvls[0]}     defence lvl = {lvls[1]}     luck lvl = {lvls[2]}      health lvl = {lvls[3]}", font=("DotGothic16", 25), justify='center', fill='white')
    loadicons()
    abutton = Button(window, image=image_references[0], command=quizes[0], bg='#16131c')
    abutton.place(x= 180, y = 300)
    tgcanvas.create_text(222, 400, anchor=N, width=150,text=f'offensive training math questions', font=("DotGothic16", 15), justify='center', fill='white')
    bbutton = Button(window, image=image_references[1], command=quizes[1], bg='#16131c')
    bbutton.place(x= 430, y = 300)
    tgcanvas.create_text(472, 400, anchor=N, width=150,text=f'defencive training animal questions', font=("DotGothic16", 15), justify='center', fill='white')
    cbutton = Button(window, image=image_references[2], command=quizes[2], bg='#16131c')
    cbutton.place(x= 680, y = 300)
    tgcanvas.create_text(722, 400, anchor=N, width=150,text=f'tactical training shape questions', font=("DotGothic16", 15), justify='center', fill='white')
    dbutton = Button(window, image=image_references[3], command=quizes[3], bg='#16131c')
    dbutton.place(x= 930, y = 300)
    tgcanvas.create_text(972, 400, anchor=N, width=150,text=f'supportive training colour questions', font=("DotGothic16", 15), justify='center', fill='white')
    
    location = Combatmenu('training grounds')
    combatstart = Button(window, text="combat trial", command=location.innitcombat)
    combatstart.place(relx=0.5, rely=0.7, anchor=CENTER)
    tgcanvas.create_text(600, 700, anchor=N, width=150,text=f'combat trial\nfight enemies for more xp', font=("DotGothic16", 15), justify='center', fill='white')

class Combatmenu():
    def __init__(self, area):
        self.area = area
    
    def innitcombat(self):
        global theplayer
        global enemy
        global totalenemies
        global combat
        global questiontally
        questiontally = 0 #number of questions answered in combat
        combat = TRUE
        # enemytype = random.randint(0,2)
        enemytype = 1
        # totalenemies = random.randint(1,2)
        totalenemies = 2
        if enemytype ==1:
            enemy = Spiders(enemies[enemytype],enemyhp[enemytype], totalenemies, enemyatk[enemytype])
        else:
            enemy = Enemy(enemies[enemytype],enemyhp[enemytype], totalenemies, enemyatk[enemytype])
        theplayer = Player(200+lvls[3], 30+lvls[0], lvls[2])
        for widget in window.winfo_children():
            widget.destroy()
        self.combatsetup()
        theplayer.playerturn()

    def combatsetup(self):
        global nero
        global combatmenu
        global tk_image
        global lvls
        global currentbg
        currentbg = Background(4)
        currentbg.load()

        image_path = "sprites/healthbar.png"
        pil_image = Image.open(image_path)
        tk_image = ImageTk.PhotoImage(pil_image)
        enemy.displayenemy()

        menu_image = Image.open("sprites/combatmenu.png")
        combatmenu = ImageTk.PhotoImage(menu_image)
        thecmenu = Label(window, image=combatmenu)
        thecmenu.place(relx=0.5, rely=0.82 ,anchor=CENTER)

        profile()
        neropfp.place(x=63,y=645)

        theplayer.displayhealthbar()

class Player():
    def __init__(self, health, attack, luck):
        self.health = health
        self.attack = attack
        self.luck = luck
    
    def displayhealthbar(self):
        global hpbar_image
        global pcurrent_health
        global phealthbar
        pcurrent_health = self.health
        image_path = "sprites/phealthbar.png"
        pil_image = Image.open(image_path)
        hpbar_image = ImageTk.PhotoImage(pil_image)
        phealthbar = Canvas(window, width=502, height=50, highlightthickness=0)
        phealthbar.place(anchor=CENTER, relx=0.43, rely=0.8)
        phealthbar.create_image(253, 27, image=hpbar_image)
        phealthbar.create_rectangle(15, 15, 490, 40, fill="brown", tags="health_bar")
        hpamount = Label(window, text=f'{pcurrent_health}/{self.health}')
        hpamount.place(anchor=CENTER, relx=0.67, rely=0.8)
    
    def updatehp(self):
        global pcurrent_health
        global phealthbar
        phealthbar.delete("health_bar")
        health_ratio = pcurrent_health / self.health
        bar_width = 490 * health_ratio
        phealthbar.create_rectangle(15, 15, bar_width, 40, fill="brown", tags="health_bar")

    def takedamage(self):
        global pcurrent_health
        global enemy
        pcurrent_health -= enemy.attack
        if pcurrent_health <= 0:
            for widget in window.winfo_children():
                widget.destroy()
        else:
            self.updatehp()
    
    def healhp(self):
        global pcurrent_health
        global enemy
        pcurrent_health += self.health/5
        if pcurrent_health >= self.health:
            pcurrent_health = self.health
        self.updatehp()
        window.after(500, enemy.enemyturn)

    def playerturn(self):
        global playermenu
        try: thecanvas.delete('narration')
        except: pass
        playermenu = Frame(window)
        playermenu.place(relx=0.5, rely=0.82, anchor=CENTER)
        atk = Button(playermenu, text='attack', command=self.playerattack)
        atk.pack()
        heal = Button(playermenu, text="heal", command=self.healhp)
        heal.pack()
        thecanvas.create_text(600, 100, text="player turn", font=("DotGothic16", 20, "bold"), fill="white", tags='narration')
    
    def playerattack(self):
        global enemy
        global enemymenu
        global totalenemies
        playermenu.place_forget()
        enemymenu = Frame(window)
        enemymenu.place(relx=0.5, rely=0.82, anchor=CENTER)
        if enemy.amount == 2:
            e1button = Button(enemymenu, text = f'left {enemy.name}',command=hpbar1.createquiz)
            e1button.pack()
            e2button = Button(enemymenu, text = f'right {enemy.name}', command=hpbar2.createquiz)
            e2button.pack()
        elif enemy.amount == 1 and totalenemies == 2:
            e1button = Button(enemymenu, text=f'{enemy.name}',command=hpbar2.createquiz)
            e1button.pack()
        else:
            e1button = Button(enemymenu, text=f'{enemy.name}',command=hpbar1.createquiz)
            e1button.pack()
        goback = Button(enemymenu, text='go back', command = self.playerreturn)
        goback.pack()

    def playerreturn(self):
        global enemymenu
        for widget in enemymenu.winfo_children():
            widget.destroy() 
        self.playerturn()

class Enemy():
    def __init__(self, name, health, amount, attack):
        self.name = name
        self.health = health
        self.amount = amount
        self.attack = attack
    
    def displayenemy(self):
        global enemy_image
        global healthbars
        global enemy_currenthp
        global hpbar1
        global hpbar2
        global allenemies
        global combatbox
        global thecanvas
        thecanvas = Canvas(window, width=1200, height=900,)
        thecanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        thecanvas.create_image(0, 0, image=bgimage, anchor=NW)
        healthbars = []
        enemy_image = ImageTk.PhotoImage(Image.open(f"sprites/{self.name}.png"))
        thecanvas.create_image(600, 500, image=enemy_image, tags='enemy1')
        allenemies = ['enemy1']
        hpbar1 = Healthbar(self.health, 0)
        hpbar1.createhealthbar()
        hpbar1.displayhealthbar()
        enemy_currenthp = [self.health]
        if self.amount == 2:
            thecanvas.create_image(840, 500, image=enemy_image, tags='enemy2')
            allenemies.append('enemy2')
            hpbar2 = Healthbar(self.health, 1)
            hpbar2.createhealthbar()
            hpbar2.displayhealthbar()
            enemy_currenthp.append(self.health)
            thecanvas.delete('enemy1')
            thecanvas.create_image(360, 500, image=enemy_image, tags='enemy1')
        combatbox = ImageTk.PhotoImage(Image.open("sprites/combattext.png"))
        thecanvas.create_image(600, 100, image=combatbox)

    def enemyturn(self):
        global enemymenu
        global playermenu
        global turnsleft
        thecanvas.delete('narration')
        thecanvas.create_text(600, 100, text="enemy turn", font=("DotGothic16", 20, "bold"), fill="white", tags='narration')
        try:
            enemymenu.destroy()
        except:
            pass
        try: 
            playermenu.destroy()
        except:
            pass
        turnsleft = self.amount
        self.enemyattacks()

    def enemyattacks(self):
        global turnsleft
        print(self.amount)
        if turnsleft == 0:
            theplayer.playerturn()
        else:
            self.enemyattack()

    def enemyattack(self):
        global turnsleft
        window.after(1000)
        turnsleft -= 1
        theplayer.takedamage()
        window.after(1000, self.enemyattacks)

class Spiders(Enemy):
    def displayenemy(self):
        global enemy_image
        global healthbars
        global enemy_currenthp
        global hpbar1
        global hpbar2
        global allenemies
        global combatbox
        global thecanvas
        thecanvas = Canvas(window, width=1200, height=900,)
        thecanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        thecanvas.create_image(0, 0, image=bgimage, anchor=NW)
        healthbars = []
        enemy_image = ImageTk.PhotoImage(Image.open(f"sprites/{self.name}.png"))
        thecanvas.create_image(600, 350, image=enemy_image, tags='enemy1')
        allenemies = ['enemy1']
        hpbar1 = Healthbar(self.health, 0)
        hpbar1.createhealthbar()
        hpbar1.displayhealthbar()
        enemy_currenthp = [self.health]
        if self.amount == 2:
            thecanvas.create_image(840, 350, image=enemy_image, tags='enemy2')
            allenemies.append('enemy2')
            hpbar2 = Healthbar(self.health, 1)
            hpbar2.createhealthbar()
            hpbar2.displayhealthbar()
            enemy_currenthp.append(self.health)
            thecanvas.delete('enemy1')
            thecanvas.create_image(360, 350, image=enemy_image, tags='enemy1')
        combatbox = ImageTk.PhotoImage(Image.open("sprites/combattext.png"))
        thecanvas.create_image(600, 100, image=combatbox)

class Healthbar():
    def __init__(self, maxhp, index):
        self.maxhp = maxhp
        self.index = index
    
    def createhealthbar(self):
        global tk_image
        global enemy
        global healthbars
        canvas = Canvas(window, width=302, height=50, highlightthickness=0)
        canvas.create_image(153, 27, image=tk_image)
        canvas.create_rectangle(15, 15, 290, 40, fill="brown", tags='health_bar')
        healthbars.append(canvas)
    
    def displayhealthbar(self):
        global healthbars
        global enemy
        healthbars[self.index].place(anchor=CENTER, relx=0.5, rely=0.25)
        if self.index == 1 and enemy.amount==2:
            healthbars[self.index].place(anchor=CENTER, relx=0.7, rely=0.25)
            healthbars[0].place(anchor=CENTER, relx=0.3, rely=0.25)
        elif self.index == 2:
            healthbars[self.index].place(anchor=CENTER, relx=0.2, rely=0.26)
            healthbars[1].place(anchor=CENTER, relx=0.8, rely=0.26)
            healthbars[0].place(anchor=CENTER, relx=0.5, rely=0.25)
    
    def updatehp(self):
        global healthbars
        global enemy_currenthp
        healthbars[self.index].delete("health_bar")
        health_ratio = enemy_currenthp[self.index] / self.maxhp
        bar_width = 290 * health_ratio
        healthbars[self.index].create_rectangle(15, 15, bar_width, 40, fill="brown", tags="health_bar")

    def combatquestion(self):
        global quizes
        quizes[random.randint(0,3)]()

    def createquiz(self):
        global healthbar_id
        quizes[random.randint(0,3)]()
        # animalsquiz()
        healthbar_id = self.index

    def takedamage(self):
        global allenemies
        global enemy_currenthp
        global healthbars
        global enemy
        global theplayer
        global thecanvas
        global quizes
        global hurtenemy
        global coords

        coords = thecanvas.coords(allenemies[self.index])
        hurtenemy = ImageTk.PhotoImage(Image.open(f"sprites/hurt{enemy.name}.png"))
        thecanvas.delete(allenemies[self.index])
        thecanvas.create_image(coords[0], coords[1], image=hurtenemy, tags=allenemies[self.index])

        enemy_currenthp[self.index] -= theplayer.attack
        if enemy_currenthp[self.index] <= 0:
            mixer.Sound.play(death)
            enemy_currenthp[self.index] = 0
            healthbars[self.index].place_forget()
            thecanvas.delete(allenemies[self.index])
            newamount = enemy.amount - 1
            if newamount > 0 :
                enemy.amount = newamount
                enemy.enemyturn()
            else:
                traininggrounds()
        else:
            mixer.Sound.play(boom)
            window.after(300, self.returnsprite)
            self.updatehp()
    
    def returnsprite(self):
        thecanvas.delete(allenemies[self.index])
        thecanvas.create_image(coords[0], coords[1], image=enemy_image, tags=allenemies[self.index])
        enemy.enemyturn()

# class Boss(Enemy):
#     def __init__(self):
#         pass

def combatexp():
    global lvls
    global xpmultiplier
    global totalenemies
    global enemy
    
def lobby():
    global currentbg
    global lobbybgimg
    for widget in window.winfo_children():
        widget.destroy()
    currentbg=Background(1)
    currentbg.load()
    
    doors()
    profile()
    tgicon()

beginning()

mainloop()