from rembg import remove
from PIL import Image

input_path = r"C:\Users\User\Desktop\ComfyUI_lizz\output\arcane_panel_00007_.png"
output_path = r"C:\Users\User\Desktop\ComfyUI_lizz\output\character_extracted.png"

print(f"Loading image from: {input_path}")
input_image = Image.open(input_path)

print("Removing background...")
output_image = remove(input_image)

print(f"Saving to: {output_path}")
output_image.save(output_path)

print("Done! Character extracted successfully.")
