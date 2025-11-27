# VirtualPet
A cute, always-on-top desktop pet inspired by classic virtual pets (Tamagotchi / Desktop Goose style).  
Your little friend lives on your desktop, gets hungry/dirty/sad, shows thought bubbles when it needs something, and can die if neglected — but you can always hatch a new one!

Fully written in Python with Tkinter + Pillow. Works perfectly on Windows, Linux, and macOS.

## Features

- Egg → Hatch animation (4 seconds)
- 4 stats: Hunger, Happiness, Cleanliness, Health
- Mood states: happy, idle, sad, depressed, dead
- Thought bubbles for hunger & cleanliness needs (normal + critical versions supported)
- Feed / Play / Clean buttons
- Pet slowly drifts around the screen every few seconds
- Fully draggable (click & drag anywhere — pet, buttons, egg)
- Saves progress automatically (pet_state.json)
- Transparent window on Windows (true shaped window)
- Close button (X)
- Works as script or standalone executable

## Requirements (to run from source)

- Python 3.8+
- Pillow → pip install pillow

On Linux:
sudo apt install python3-tk python3-pil.imagetk   # Ubuntu/Debian
# or
sudo dnf install python3-tkinter python3-pillow-tk  # Fedora

## How to Run

git clone https://github.com/yourusername/virtual-pet.git
cd virtual-pet
python virtual_pet.py

Your pet will appear in the bottom-right corner. Drag it anywhere you like!

## Building a Standalone Executable

### Windows → .exe

pip install pyinstaller
pyinstaller --onefile --windowed --noconsole ^
    --add-data "images;images" ^
    --icon=images/pet_egg.ico ^
    --name "DesktopPet" ^
    virtual_pet.py

### Linux → single binary

pip install pyinstaller
pyinstaller --onefile --windowed \
    --add-data "images:images" \
    --name "DesktopPet" \
    virtual_pet.py

Executable will be in dist/

Linux transparency note: The app uses magenta as transparent color (perfect on Windows).  
On Linux the magenta frame is usually visible — still super cute.  
For perfect shaped transparency, change all bg="magenta" to bg="black" and make your PNGs actually transparent.

## File Structure

virtual-pet/
├── virtual_pet.py
├── make_icon.py            # <- in case you wanted to create a desktop shortcut
├── pet_egg.ico
├── images/                 # <- put your 64×64 pixel art here
│   ├── pet_idle.png
│   ├── pet_happy.png
│   ├── pet_sad.png
│   ├── pet_depressed.png
│   ├── pet_dead.png (optional)
│   ├── pet_egg.png
│   ├── thought_hungry.png
│   ├── thought_starved.png (optional)
│   ├── thought_dirty.png
│   └── thought_disgusting.png (optional)
└── pet_state.json          # auto-created save file

All images are automatically upscaled ×2 (128×128) with bicubic interpolation, but you can optionally use nearest-neighbor for crisp pixel art.

## Customization

Just replace the PNGs in the images/ folder with your own 64×64 pixel art (keep the same filenames) and you instantly have a completely different pet/creature/character.

## License

MIT License — do whatever you want with it.

---
Enjoy your eternal desktop companion!