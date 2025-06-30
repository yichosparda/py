import tkinter as tk 
from PIL import Image, ImageTk
def main():
# Create the main window
    root = tk.Tk()
    root.title("Cat Viewer")
    # Load the image (replace 'cat.png' with your image filename)
    pil_image = Image.open("palace.png")
    # Convert to a Photolmage
    tk_image = ImageTk.PhotoImage(pil_image)
    # Create a label to hold the image and pack it into the window
    label = tk.Label(root, image=tk_image)
    label.pack(padx=10, pady=10)
    # Start the GUI event loop
    root.mainloop()
if __name__ == "__main__":
    main()