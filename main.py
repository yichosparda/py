from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame
from pygame import mixer

window = Tk()
window.title("")
window.geometry("300x270")
window.option_add("*Background", "#000000")
window.config(bg="#000000")

def mathquiz():
    global mcount
    mwindow = Toplevel(window)
    mwindow.title("maths question")
    mwindow.geometry("400x150")
    mwindow.option_add("*Background", "#000000")
    mwindow.config(bg="#000000")
    mcount = 15
    #general class for math questions and addition
    class Maths():
        # global mathsprogress
        def __init__(self, number1, number2): #numbers for the math question
            self.number1 = number1
            self.number2 = number2
            
        def question(self):
            #displays questions
            return f"what is {self.number1} + {self.number2}"
        
        def answer(self):
            try:
                answer = int(manswer.get()) #get the number from the input
                if answer == (self.number1)+ (self.number2):
                    return "correct!"
                else:
                    return f"sorry...\nthe answer was {self.number1 + self.number2}"
            except: #for non-integer inputs
                return f"sorry...\nthe answer was {self.number1 + self.number2}"

    #category for subtraction questions
    class Subtraction(Maths):
        def question(self):
                #displays questions
                return f"what is {self.number1} - {self.number2}"
            
        def answer(self):
            try:
                answer = int(manswer.get()) #get the number from the input
                if answer == self.number1 - self.number2:
                    return "correct!"
                else:
                    return f"sorry...the answer was {self.number1 - self.number2}"
            except: #for non-integer inputs
                return f"sorry...the answer was {self.number1 - self.number2}"
            
    #category for multiplication questions (only allows for numbers from 1 to 5)
    class Multiplication(Maths):
        def question(self):
            #displays question
            return f"what is {self.number1} x {self.number2}"
            
        def answer(self):
            try:
                answer = int(manswer.get()) #gets number from input
                if answer == self.number1 * self.number2:
                    return "correct!"
                else:
                    return f"sorry...\nthe answer was {self.number1 * self.number2}"
            except: #for non-integer inputs
                return f"sorry...\nthe answer was {self.number1 * self.number2}"

    #category for division questions   
    class Division(Maths):
        def question(self):
            #displays question
            return f"what is {self.number1} / {self.number2}"
        def answer(self):
            try:
                answer = int(manswer.get()) # gets number from input
                if answer == self.number1/self.number2:
                    return "correct!"
                else:
                    return f"sorry...\nthe answer was {self.number1 / self.number2}"
            except: #for non-integer inputs
                return f"sorry...\nthe answer was {self.number1 / self.number2}"
            
    subjects = [Maths, Subtraction, Multiplication, Division] #lists of subjects to refer to 
            
    def askquestion():
        text1 = Label(mwindow, text=question.question(), font=("DotGothic16", 20, "bold"))
        text1.grid(row=1, column=0, padx = 15, sticky="w")

    def checkanswer():
        global mcount
        text2 = Label(mwindow, text=question.answer(), font=("DotGothic16", 15, "bold"), justify=LEFT)
        text2.grid(row=2, column=0, sticky="w", padx=20)
        check.config(text = "continue", command = leave)
        mcount = "done"

    def leave():
        mwindow.destroy()

    def countdown():
        global mcount
        try :
            int(mcount)
            if mcount >= 0:
                timer.config(text=f"you have {mcount} seconds left!")
                mcount -= 1
                mwindow.after(1000, countdown)
            else:
                checkanswer()
        except:
            timer.grid_forget

    def enterbutton(event):
        if mcount == "done":
            mwindow.destroy()
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

    timer = Label(mwindow, text=f"you have {mcount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askquestion()
    countdown()
    manswer = Entry(mwindow, bd=3, relief="ridge", width=10)
    manswer.grid(row=1, column=1, sticky="w")
    manswer.bind("<Return>", enterbutton)
    manswer.bind("<Key>", checkint)
    check = Button(mwindow, text="check", command=checkanswer)
    check.grid(row=3, column=0, sticky="w", padx=20)

def shapesquiz():
    global scount
    swindow = Toplevel(window)
    swindow.title("shape question")
    swindow.geometry("300x270")
    swindow.option_add("*Background", "#000000")
    swindow.config(bg="#000000")

    shapes = ['Rectangle','Square','Circle','Pentagon','Hexagon','Octagon']
    scount = 15

    def leave():
        swindow.destroy()

    def countdown():
        global scount
        try :
            int(scount)
            if scount >= 0:
                timer.config(text=f"you have {scount} seconds left!")
                scount -= 1
                swindow.after(1000, countdown)
            else:
                shapeanswer()
        except:
            timer.grid_forget

    shape = random.randint(0,5)

    def enterbutton(event):
        if scount == "done":
            swindow.destroy()
        else:
            shapeanswer()

    def shapeanswer():
        global scount
        global answer
        text2 = 0
        answer = (sanswer.get()).upper()
        if answer == "RECTANGLE" and shapes[shape].upper() == "SQUARE":
            text2=Label(swindow, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            scount = "done"
            
        elif answer == shapes[shape].upper():
                text2=Label(swindow, text="correct!", font=("DotGothic16", 15, "bold"))
                text2.grid(row=4, column=0, sticky="w", padx=20)
                check.config(text = "continue", command = leave)
                check.grid(row = 5, column=0)
                scount = "done"
        else:
            text2=Label(swindow, text=f"sorry... it's {shapes[shape].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            scount = "done"

    def askshape():
        global photo
        question = Label(swindow, text="what shape is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        image = Image.open(f"shapes/{shapes[shape]}.png")
        if shape == 0:
            resized_image = image.resize((200, 100))
            photo = ImageTk.PhotoImage(resized_image)
            theshape = Label(swindow, image=photo)
            theshape.grid(row=2, column=0)
        else: 
            resized_image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(resized_image)
            theshape = Label(swindow, image=photo)
            theshape.grid(row=2, column=0)

    timer = Label(swindow, text=f"you have {scount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askshape()
    countdown()
    sanswer = Entry(swindow, bd=3, relief="ridge", width=10)
    sanswer.grid(row=3, column=0, sticky="w", padx=20)
    sanswer.bind("<Return>", enterbutton)
    check = Button(swindow, text="check", command=shapeanswer)
    check.grid(row=4, column=0, sticky="w", padx=20)

def coloursquiz():
    global ccount
    cwindow = Toplevel(window)
    cwindow.title("colour question")
    cwindow.geometry("300x160")
    cwindow.option_add("*Background", "#000000")
    cwindow.config(bg="#000000")
    colours = ['Red','Blue','Green','Pink','Black','Yellow','Orange','White','Purple','Brown']
    ccount = 15

    def leave():
        cwindow.destroy()

    def countdown():
        global ccount
        try :
            int(ccount)
            if ccount >= 0:
                timer.config(text=f"you have {ccount} seconds left!")
                ccount -= 1
                cwindow.after(1000, countdown)
            else:
                colouranswer()
        except:
            timer.grid_forget

    colour = random.randint(0,9)

    def enterbutton(event):
        global ccount
        if ccount == "done":
            cwindow.destroy()
        else:
            colouranswer()

    def askcolour():
        question = Label(cwindow, text="what colour is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        thecolour = Label(cwindow, text="---", fg=colours[colour], bg=colours[colour], font=("DotGothic16", 12, "bold"), relief="raised")
        thecolour.grid(row=1, column=1)

    def colouranswer():
        global ccount
        global answer
        text2 = 0
        answer = (canswer.get()).upper()
        if answer == colours[colour].upper():
                text2=Label(cwindow, text="correct!", font=("DotGothic16", 15, "bold"))
                text2.grid(row=3, column=0, sticky="w", padx=20)
                check.config(text = "continue", command = leave)
                check.grid(row = 4, column=0)
                ccount = "done"
        else:
            text2=Label(cwindow, text=f"sorry... it's {colours[colour].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=3, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 4, column=0)
            ccount = "done"

    timer = Label(cwindow, text=f"you have {ccount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)
    askcolour()
    countdown()
    canswer = Entry(cwindow, bd=3, relief="ridge", width=10)
    canswer.grid(row=2, column=0, sticky="w", padx=20)
    canswer.bind("<Return>", enterbutton)
    check = Button(cwindow, text="check", command=colouranswer)
    check.grid(row=3, column=0, sticky="w", padx=20)

def animalsquiz():
    global acount
    awindow = Toplevel(window)
    awindow.title("animal question")
    awindow.geometry("300x270")
    awindow.option_add("*Background", "#000000")
    awindow.config(bg="#000000")

    #placement for user answers
    animals = ['Bear','Bird','Cat','Dog','Fox','Horse', 'Penguin', 'Raccoon']
    acount = 15

    def leave():
        awindow.destroy()

    def countdown():
        global acount
        try :
            int(acount)
            if acount >= 0:
                timer.config(text=f"you have {acount} seconds left!")
                acount -= 1
                awindow.after(1000, countdown)
            else:
                animalanswer()
        except:
            timer.grid_forget

    animal = random.randint(0,7)

    def enterbutton(event):
        if acount == "done":
            leave()
        else:
            animalanswer()

    def animalanswer():
        global acount
        text2 = 0
        answer = (qanswer.get()).upper()
        if answer == "RECTANGLE" and animals[animal].upper() == "SQUARE":
            text2=Label(awindow, text="correct!", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            acount = "done"
            
        elif answer == animals[animal].upper():
                text2=Label(awindow, text="correct!", font=("DotGothic16", 15, "bold"))
                text2.grid(row=4, column=0, sticky="w", padx=20)
                check.config(text = "continue", command = leave)
                check.grid(row = 5, column=0)
                acount = "done"
        else:
            text2=Label(awindow, text=f"sorry... it's {animals[animal].lower()}", font=("DotGothic16", 15, "bold"))
            text2.grid(row=4, column=0, sticky="w", padx=20)
            check.config(text = "continue", command = leave)
            check.grid(row = 5, column=0)
            acount = "done"

    timer = Label(awindow, text=f"you have {acount} seconds left!", font=("DotGothic16", 15, "bold"))
    timer.grid(row=0, column=0, sticky="w", padx=5)

    def askanimal():
        global photo
        question = Label(awindow, text="what animal is this?", font=("DotGothic16", 20, "bold"))
        question.grid(row=1, column=0, sticky="w", padx=15)
        image = Image.open(f"animals/{animals[animal]}.png")
        resized_image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(resized_image)
        theshape = Label(awindow, image=photo)
        theshape.grid(row=2, column=0)

    askanimal()
    countdown()
    qanswer = Entry(awindow, bd=3, relief="ridge", width=10)
    qanswer.grid(row=3, column=0, sticky="w", padx=20)
    qanswer.bind("<Return>", enterbutton)
    check = Button(awindow, text="check", command=animalanswer)
    check.grid(row=4, column=0, sticky="w", padx=20)

# def pickquiz():
#     quizes = [mathquiz, shapesquiz, coloursquiz, animalsquiz]
#     quiz = random.randint(0,3)
#     quizes[quiz]()

# thequiz = Button(text="question", command=pickquiz)
# thequiz.pack()

mainloop()
