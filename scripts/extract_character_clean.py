from rembg import remove
from PIL import Image
import numpy as np

input_path = r"C:\Users\User\Desktop\ComfyUI_lizz\output\arcane_panel_00007_.png"
output_path = r"C:\Users\User\Desktop\ComfyUI_lizz\output\character_extracted_clean.png"

print(f"Loading image from: {input_path}")
input_image = Image.open(input_path)

print("Removing background with better settings...")
# Use u2net model with alpha matting for cleaner edges
output_image = remove(
    input_image,
    alpha_matting=True,
    alpha_matting_foreground_threshold=240,
    alpha_matting_background_threshold=10,
    alpha_matting_erode_size=10
)

print(f"Saving to: {output_path}")
output_image.save(output_path)

print("Done! Cleaner extraction complete.")

# Also create a version with pure transparency (remove semi-transparent pixels)
print("Creating version with pure edges...")
img_array = np.array(output_image)
# Get alpha channel
alpha = img_array[:, :, 3]
# Set threshold - anything below 200 alpha becomes fully transparent
alpha[alpha < 200] = 0
img_array[:, :, 3] = alpha

clean_image = Image.fromarray(img_array)
clean_output_path = r"C:\Users\User\Desktop\ComfyUI_lizz\output\character_extracted_pure.png"
clean_image.save(clean_output_path)
print(f"Pure version saved to: {clean_output_path}")
