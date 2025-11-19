from PIL import Image
import numpy as np

input_path = r"C:\Users\User\Desktop\ComfyUI_lizz\output\arcane_panel_00007_.png"
output_path = r"C:\Users\User\Desktop\ComfyUI_lizz\output\character_extracted_no_red.png"

print(f"Loading image from: {input_path}")
img = Image.open(input_path).convert('RGBA')
img_array = np.array(img)

# Extract RGB channels
r = img_array[:, :, 0].astype(float)
g = img_array[:, :, 1].astype(float)
b = img_array[:, :, 2].astype(float)
a = img_array[:, :, 3]

print("Detecting and removing red/orange areas...")

# Create mask for red/orange areas
# Red is dominant: R > G and R > B
# Also check for high saturation reds
red_mask = (r > g + 30) & (r > b + 30) & (r > 150)

# Also catch bright orange/red areas
bright_red_mask = (r > 200) & (g < 150) & (b < 150)

# Combine masks
remove_mask = red_mask | bright_red_mask

# Set alpha to 0 where we want to remove
a[remove_mask] = 0

# Apply back to image
img_array[:, :, 3] = a

print(f"Removed {np.sum(remove_mask)} red pixels")

# Save result
result_img = Image.fromarray(img_array)
result_img.save(output_path)
print(f"Saved to: {output_path}")

# Also create a version that removes the character and keeps only the clean areas
print("\nCreating version with character isolation...")
# Character is likely in the center-left area with cyan/blue/purple tones
# Red is mostly on the right side

# Create a more sophisticated mask
height, width = r.shape

# Define regions: left half is character, right half might have red background
left_boundary = width // 2

# For the right side, be more aggressive with red removal
for x in range(left_boundary, width):
    for y in range(height):
        pixel_r = img_array[y, x, 0]
        pixel_g = img_array[y, x, 1]
        pixel_b = img_array[y, x, 2]

        # Remove anything that's too red on the right side
        if pixel_r > pixel_g + 20 and pixel_r > pixel_b + 20:
            img_array[y, x, 3] = 0

output_path_clean = r"C:\Users\User\Desktop\ComfyUI_lizz\output\character_only.png"
result_img_clean = Image.fromarray(img_array)
result_img_clean.save(output_path_clean)
print(f"Character-only version saved to: {output_path_clean}")

print("\nDone! Check both files:")
print(f"1. {output_path}")
print(f"2. {output_path_clean}")
