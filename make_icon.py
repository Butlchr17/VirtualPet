from PIL import Image

# Load your 64×64 egg sprite
img = Image.open("images/pet_egg.png")

# Save as multi-resolution .ico (Windows loves this)
img.save("pet_egg.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
print("pet_egg.ico created successfully!")