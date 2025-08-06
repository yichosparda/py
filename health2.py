import tkinter as tk
from PIL import Image, ImageTk 

root = tk.Tk()
root.title("Health Bar Example")

image_path = "sprites/phealthbar.png"
pil_image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(pil_image)
canvas = tk.Canvas(root, width=500, height=50)
canvas.pack()
canvas.create_image(253, 27, image=tk_image)
max_health = 100
current_health = 100
canvas.create_rectangle(15, 15, 490, 40, fill="brown", tags="health_bar")

def update_health_bar():
    canvas.delete("health_bar")  # Clear previous health bar
    health_ratio = current_health / max_health
    bar_width = 490 * health_ratio
    canvas.create_rectangle(15, 15, bar_width, 40, fill="brown", tags="health_bar")

def take_damage():
    global current_health
    current_health -= 10
    if current_health <= 0:
        current_health = 0
        canvas.pack_forget()
    else:
        update_health_bar()

def heal():
    global current_health
    current_health += 10
    if current_health > max_health:
        current_health = max_health
    update_health_bar()

damage_button = tk.Button(root, text="Take Damage", command=take_damage)
damage_button.pack()

heal_button = tk.Button(root, text="Heal", command=heal)
heal_button.pack()

root.mainloop()