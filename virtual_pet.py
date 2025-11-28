import tkinter as tk
from PIL import Image, ImageTk
import json
import sys
import os
import platform
import random

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_upscaled_photo(relative_path, scale=2):
    path = resource_path(relative_path)
    try:
        img = Image.open(path)
        if scale > 1:
            new_size = (img.width * scale, img.height * scale)
            img = img.resize(new_size, Image.BICUBIC)   # Use NEAREST for crisp pixel art
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

class Pet:
    def __init__(self):
        self.hunger = 50
        self.happiness = 50
        self.cleanliness = 50
        self.health = 100
        self.name = "Zorn"
        self.state = 'idle'
        self.load_state()
        self.set_mood()

    def set_mood(self):
        if self.health <= 0:
            self.state = "dead"
            return
        if self.happiness < 20:
            self.state = 'depressed'
        elif self.happiness < 40:
            self.state = 'sad'
        elif self.happiness > 85:
            self.state = 'happy'
        else:
            self.state = "idle"

    def update(self):
        self.hunger = max(0, self.hunger - 10)
        self.happiness = max(0, self.happiness - 5)
        self.cleanliness = max(0, self.cleanliness - 5)
        
        decrement = 0
        if self.hunger < 20 or self.happiness < 20 or self.cleanliness < 20:
            if self.hunger < 20:      decrement += 5
            if self.happiness < 20:   decrement += 5
            if self.cleanliness < 20: decrement += 5
        else:
            if self.hunger < 40:         decrement += 1
            if self.happiness < 40:   decrement += 1
            if self.cleanliness < 40: decrement += 1

        self.health = max(0, self.health - decrement)
        if self.health <= 0:
            self.health = 0
            self.state = "dead"

        self.set_mood()
        self.save_state()

    def feed(self):
        self.hunger = min(100, self.hunger + 30)
        self.happiness = min(100, self.happiness + 5)
        self.health = min(100, self.health + 8)
    
    def play(self):
        self.happiness = min(100, self.happiness + 30)
        self.hunger = max(0, self.hunger - 8)
        self.cleanliness = max(0, self.cleanliness - 5)
        self.health = min(100, self.health + 8)
    
    def clean(self):
        self.cleanliness = min(100, self.cleanliness + 35)
        self.happiness = min(100, self.happiness + 5)
        self.health = min(100, self.health + 8)

    def save_state(self):
        data = {
            'hunger': self.hunger,
            'happiness': self.happiness,
            'cleanliness': self.cleanliness,
            'health': self.health,
            'name': self.name,
        }
        try:
            with open('pet_state.json', 'w') as f:
                json.dump(data, f)
        except:
            pass

    def load_state(self):
        if os.path.exists('pet_state.json'):
            try:
                with open('pet_state.json', 'r') as f:
                    data = json.load(f)
                    self.hunger = data.get('hunger', 50)
                    self.happiness = data.get('happiness', 50)
                    self.cleanliness = data.get('cleanliness', 50)
                    self.health = data.get('health', 100)
                    self.name = data.get('name', "Zorn")
            except:
                pass

# Main window
root = tk.Tk()
root.title("Virtual Pet")
root.overrideredirect(True)  # No title bar
root.attributes("-topmost", True)
root.attributes("-alpha", 0.94)

# Transparent background
if platform.system() == "Windows":
    root.attributes("-transparentcolor", "magenta")
root.configure(bg="magenta")

# Icon
icon_path = resource_path("images/pet_egg.png")
egg_icon_img = Image.open(icon_path)
egg_icon = ImageTk.PhotoImage(egg_icon_img)
root.iconphoto(True, egg_icon)

# Window size & position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width, window_height = 256, 480
root.geometry(f"{window_width}x{window_height}+{screen_width - window_width - 50}+{screen_height - window_height - 50}")

# Canvas for pet
canvas = tk.Canvas(root, width=256, height=340, bg="magenta", highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=10, pady=(0, 20))

pet_item = canvas.create_image(128, 260, anchor="center")
hunger_bubble_item = canvas.create_image(80, 100, anchor="center", state="hidden")
clean_bubble_item = canvas.create_image(176, 100, anchor="center", state="hidden")

# Buttons
button_frame = tk.Frame(root, bg="magenta")
button_frame.pack(side="bottom", fill="x", pady=(0,15))

# Action buttons
tk.Button(button_frame, text="Feed", command=lambda: perform_action(pet.feed), bg="#ff9999", relief="flat", font=("Arial", 10)).pack(side="left", padx=15)
tk.Button(button_frame, text="Play", command=lambda: perform_action(pet.play), bg="#99ff99", relief="flat", font=("Arial", 10)).pack(side="left", padx=15)
tk.Button(button_frame, text="Clean", command=lambda: perform_action(pet.clean), bg="#99ccff", relief="flat", font=("Arial", 10)).pack(side="left", padx=15)

# Top UI bar and name display
top_bar = tk.Frame(root, bg="#333333", height=46)
top_bar.place(x=0, y=0, relwidth=1)
top_bar.pack_propagate(False) # prevent resizing

# Close button
close_btn = tk.Button(root, text="✕", command=root.quit, bg='#e81123', fg='white', relief="flat", font=("Arial", 16, "bold"))
close_btn.place(relx=0.98, rely=0.0075, anchor='ne')

# Name display
name_frame = tk.Frame(top_bar, bg="#ffd700", highlightbackground="#000000", highlightthickness=3, padx=22, pady=8, relief="raised")
name_frame.place(relx=0.5, rely=0.5, anchor="center")
name_label = tk.Label(name_frame, text="", font=("Arial", 18, "bold"), bg="#ffd700", fg="#000000", highlightthickness=0)
name_label.pack()

# Dragging
drag_x = drag_y = 0

def start_drag(event):
    global drag_x, drag_y
    drag_x = event.x
    drag_y = event.y

def drag(event):
    dx = event.x - drag_x
    dy = event.y - drag_y
    x = root.winfo_x() + dx
    y = root.winfo_y() + dy
    root.geometry(f"+{x}+{y}")

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", drag)
button_frame.bind("<Button-1>", start_drag)
button_frame.bind("<B1-Motion>", drag)

# Functions
def get_image_path(state):
    path = resource_path(f"images/pet_{state}.png")
    if os.path.exists(path):
        return path
    return resource_path("images/pet_idle.png")

def perform_action(action):
    if pet is None or pet.state == "dead":
        return
    action()
    update_pet_image()
    pet.save_state()
    check_death()

def update_bubble_positions():
    pet_coords = canvas.coords(pet_item)
    if len(pet_coords) < 2:
        return
    pet_x, pet_y = pet_coords
    if canvas.itemcget(hunger_bubble_item, "state") == "normal":
        canvas.coords(hunger_bubble_item, pet_x - 48, pet_y -72)
    if canvas.itemcget(clean_bubble_item, "state") == "normal":
        canvas.coords(clean_bubble_item, pet_x + 48, pet_y - 72)

def update_pet_image():
    if pet is None:
        return

    # Main pet
    image_path = get_image_path(pet.state)
    new_photo = load_upscaled_photo(image_path)
    if new_photo is None:
        new_photo = load_upscaled_photo(resource_path("images/pet_idle.png"))
    if new_photo:
        canvas.itemconfig(pet_item, image=new_photo)
        canvas.pet_photo = new_photo

    if pet.state == "dead":
        canvas.itemconfig(hunger_bubble_item, state="hidden")
        canvas.itemconfig(clean_bubble_item, state="hidden")
        return

    # Hunger bubble
    hunger_need = "starved" if pet.hunger < 20 else "hungry" if pet.hunger < 40 else None
    if hunger_need:
        path = resource_path(f"images/thought_{hunger_need}.png")
        if not os.path.exists(path):
            path = resource_path("images/thought_hungry.png")
        photo = load_upscaled_photo(path)
        if photo:
            canvas.itemconfig(hunger_bubble_item, image=photo, state="normal")
            canvas.hunger_photo = photo
    else:
        canvas.itemconfig(hunger_bubble_item, state="hidden")

    # Clean bubble
    clean_need = "disgusting" if pet.cleanliness < 20 else "dirty" if pet.cleanliness < 40 else None
    if clean_need:
        path = resource_path(f"images/thought_{clean_need}.png")
        if not os.path.exists(path):
            path = resource_path("images/thought_dirty.png")
        photo = load_upscaled_photo(path)
        if photo:
            canvas.itemconfig(clean_bubble_item, image=photo, state="normal")
            canvas.clean_photo = photo
    else:
        canvas.itemconfig(clean_bubble_item, state="hidden")

    update_bubble_positions()  # keep bubbles above the pet's head

def show_egg(button_text="Hatch your pet!"):
    canvas.itemconfig(hunger_bubble_item, state="hidden")
    canvas.itemconfig(clean_bubble_item, state="hidden")
    button_frame.pack_forget()

    egg_photo = load_upscaled_photo(resource_path("images/pet_egg.png")) or load_upscaled_photo(resource_path("images/pet_idle.png"))
    canvas.itemconfig(pet_item, image=egg_photo)
    canvas.pet_photo = egg_photo

    if hasattr(root, "hatch_btn"):
        root.hatch_btn.destroy()

    root.hatch_btn = tk.Button(root, text=button_text, font=("Arial", 14, "bold"), bg="#ffff99", command=start_hatching)
    root.hatch_btn.place(relx=0.5, rely=0.88, anchor="center")
    root.hatch_btn.bind("<Button-1>", start_drag)
    root.hatch_btn.bind("<B1-Motion>", drag)

def start_hatching():
    root.hatch_btn.config(text="Hatching...", state="disabled")
    root.after(4000, finish_hatching)

def finish_hatching():
    if os.path.exists("pet_state.json"):
        os.remove("pet_state.json")
    global pet
    pet = Pet()
    update_pet_image()
    ask_name()  # Blocks until name is chosen
    root.hatch_btn.destroy()    # destroy hatch button after name is set
    button_frame.pack()
    game_loop()
    animate_movement()
    update_name_display()

# Allow the user to name their new pet when it hatches
def ask_name():
    # Dim the UI slightly
    root.attributes("-alpha", 0.85)

    # Create a centered panel inside the main window
    panel = tk.Frame(root, bg="#ffd700", bd=4, relief="raised")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    tk.Label(panel, text="♡ Name your pet ♡", font=("Arial", 18, "bold"),
             bg="#ffd700", fg="#000").pack(pady=(20, 10))

    # Entry field
    entry = tk.Entry(panel, font=("Arial", 20, "bold"), justify="center",
                     width=16, relief="flat", bg="white", fg="#000",
                     highlightthickness=2, highlightbackground="#ff3399",
                     insertbackground="#000")
    entry.pack(pady=12)
    entry.insert(0, pet.name)
    entry.focus_set()

    # Confirm button function
    def save_name():
        new_name = entry.get().strip()
        pet.name = new_name if new_name else "Zorn"
        update_name_display()
        pet.save_state()
        panel.destroy()
        root.attributes("-alpha", 0.94)  # restore brightness

    # Confirm button
    tk.Button(panel, text="Confirm", font=("Arial", 14, "bold"),
              bg="#ff3399", fg="white", relief="flat",
              command=save_name, padx=40, pady=10).pack(pady=15)

    # Shortcut keys
    entry.bind("<Return>", lambda e: save_name())
    entry.bind("<Escape>", lambda e: save_name())

def update_name_display():
    if pet and pet.state != "dead":
        name_label.config(text=pet.name.upper())
        name_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Golden nameplate when alive
        name_frame.config(bg="#ffd700", highlightbackground="#000000")
        
        # # Optional Mood glow effect on text
        # if pet.happiness > 90:
        #     name_label.config(fg="#ff3399")   # hot pink when super happy
        # elif pet.happiness < 30:
        #     name_label.config(fg="#aaaaaa")   # sad dim gray
        # else:
        #     name_label.config(fg="#000000")   # strong black

    else:
        name_frame.place_forget()
        top_bar.config(bg="#222222")  # dark when dead/egg

# Death Check
def check_death():
    if pet is not None and pet.state == "dead":
        update_pet_image()  # Handles dead image + hides bubbles
        root.after(3000, lambda: show_egg("Hatch new pet?"))

# Start
pet = None
save_file = resource_path("pet_state.json")

if os.path.exists(save_file):
    try:
        with open(save_file) as f:
            json.load(f)
        pet = Pet()
        update_pet_image()
        update_name_display()
        button_frame.pack(side="bottom", fill="x", pady=(0, 20))
        game_loop()
        animate_movement()
        check_death()
    except:
        show_egg("Hatch your pet!")
else:
    show_egg("Hatch your pet!")

# Game Loops
def game_loop():
    if pet and pet.state != "dead":
        pet.update()
        update_pet_image()
        update_name_display()
        check_death()
        root.after(6000, game_loop)

def animate_movement():
    if pet is None or pet.state == "dead":
        return

    pet_coords = canvas.coords(pet_item)
    if pet_coords:
        cx, cy = pet_coords
        dx = random.randint(-35, 35)
        dy = random.randint(-20, 20)

        new_x = cx + dx
        new_y = cy + dy

        new_x = max(70, min(new_x, 256 - 70))
        new_y = max(160, min(new_y, 340 - 80))

        canvas.coords(pet_item, new_x, new_y)
        update_bubble_positions()

    root.after(3200, animate_movement)

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", drag)
button_frame.bind("<Button-1>", start_drag)
button_frame.bind("<B1-Motion>", drag)
top_bar.bind("<Button-1>", start_drag)
top_bar.bind("<B1-Motion>", drag)

root.mainloop()