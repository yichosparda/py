import tkinter as tk

root = tk.Tk()
root.title("Health Bar Example")

canvas_width = 300
canvas_height = 30
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="grey")
canvas.pack()

max_health = 100
current_health = 100  # Start with some health

def update_health_bar():
    canvas.delete("health_bar")  # Clear previous health bar
    
    # Calculate health bar width based on current health
    health_ratio = current_health / max_health
    bar_width = canvas_width * health_ratio
    
    # Draw the health bar rectangle
    canvas.create_rectangle(0, 0, bar_width, canvas_height, fill="green", tags="health_bar")
    
    # Optionally, add a border or text
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, outline="black", width=2)


# Example: Simulate health change
def take_damage():
    global current_health
    current_health -= 10
    if current_health < 0:
        current_health = 0
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