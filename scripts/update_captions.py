import os
from PIL import Image

# Directory containing images
training_dir = r"C:\Users\User\Desktop\ComfyUI_lizz\lora_training_images"

# Core character features to include in every caption
core_features = "lizzchar, lime green skin, spiky teal hair with purple streaks, olive green hoodie"

# Optimized captions based on image analysis
captions = {
    "character_fullbody.png": f"{core_features}, full body, standing pose, hands in pockets, confident stance, combat boots, teal leggings, white background",

    # Back/rear views
    "Gemini_Generated_Image_473zpr473zpr473z.png": f"{core_features}, back view, rear angle, standing, full body, white background",
    "Gemini_Generated_Image_waix7nwaix7nwaix.png": f"{core_features}, 3/4 back view, turning away, full body, white background",

    # Side profiles
    "Gemini_Generated_Image_5a16xt5a16xt5a16.png": f"{core_features}, side profile, left side view, full body, standing straight, white background",
    "Gemini_Generated_Image_oboivioboivioboi.png": f"{core_features}, right side profile, full body, standing, white background",

    # Front views
    "Gemini_Generated_Image_75o73u75o73u75o7.png": f"{core_features}, front view, full body, standing straight, neutral pose, white background",
    "Gemini_Generated_Image_nc3dtvnc3dtvnc3d.png": f"{core_features}, front facing, full body, relaxed stance, white background",

    # 3/4 views
    "Gemini_Generated_Image_ia1i3aia1i3aia1i.png": f"{core_features}, 3/4 front view, full body, standing, angled pose, white background",
    "Gemini_Generated_Image_l6ulo6l6ulo6l6ul.png": f"{core_features}, 3/4 angle, full body, dynamic stance, white background",

    # Portraits/close-ups
    "Gemini_Generated_Image_qkptjxqkptjxqkpt.png": f"{core_features}, portrait, excited expression, smiling, wide eyes, cheerful, close-up face, upper body",
    "Gemini_Generated_Image_lm8g6slm8g6slm8g.png": f"{core_features}, portrait, happy expression, grinning, energetic, face focus, upper body",
    "Gemini_Generated_Image_rxt18brxt18brxt1.png": f"{core_features}, close-up portrait, neutral expression, slight smile, face detail, upper body",
    "Gemini_Generated_Image_ow46zyow46zyow46.png": f"{core_features}, portrait view, calm expression, soft smile, frontal face, upper body",

    # Action/dynamic poses
    "Gemini_Generated_Image_q3v93aq3v93aq3v9.png": f"{core_features}, jumping pose, mid-air, energetic, dynamic action, full body",
    "Gemini_Generated_Image_vd1mssvd1mssvd1m.png": f"{core_features}, running pose, motion, active stance, full body, dynamic angle",

    # Nighttime/dramatic lighting
    "Gemini_Generated_Image_268nst268nst268n.png": f"{core_features}, full body, standing, dramatic rim lighting, cyan glow, dark background, moody atmosphere, silhouette effect",
    "Gemini_Generated_Image_388y3h388y3h388y.png": f"{core_features}, back view, full body, night lighting, backlit silhouette, cyan rim light, dark atmosphere",
    "Gemini_Generated_Image_3c6by63c6by63c6b (1).png": f"{core_features}, front view, full body, dramatic lighting, cyan backlight, hands on hips, confident pose, dark background",
    "Gemini_Generated_Image_4v4f864v4f864v4f.png": f"{core_features}, 3/4 front view, full body, night scene, cyan rim lighting, moody atmosphere, dark background",
    "Gemini_Generated_Image_6i8lnu6i8lnu6i8l.png": f"{core_features}, side view, full body, dramatic side lighting, cyan glow, silhouette, dark background",
    "Gemini_Generated_Image_9hkuzf9hkuzf9hku.png": f"{core_features}, side profile, full body, night lighting, rim light, mysterious atmosphere, dark background",
    "Gemini_Generated_Image_t131zvt131zvt131.png": f"{core_features}, front view, full body, strong backlight, cyan glow, dramatic silhouette, standing straight, dark background",

    # More action/dynamic poses
    "Gemini_Generated_Image_32dklo32dklo32dk.png": f"{core_features}, jumping high, mid-air leap, dynamic action, energetic pose, legs tucked, white background, full body",
    "Gemini_Generated_Image_v6a7mwv6a7mwv6a7.png": f"{core_features}, running forward, motion, dynamic pose, action shot, white background, full body",
    "Gemini_Generated_Image_wk84ihwk84ihwk84.png": f"{core_features}, excited pose, arms raised, celebrating, energetic stance, white background, full body",
    "Gemini_Generated_Image_778emx778emx778e.png": f"{core_features}, waving hand, friendly gesture, standing, white background, full body",
    "Gemini_Generated_Image_zduhdazduhdazduh.png": f"{core_features}, walking pose, casual stride, hands in pockets, relaxed, white background, full body",

    # Cyberpunk/neon city scenes
    "Gemini_Generated_Image_398ldk398ldk398l.png": f"{core_features}, running in cyberpunk city, neon lights, pink and cyan glow, urban environment, dynamic action, full body",
    "Gemini_Generated_Image_vk7c35vk7c35vk7c.png": f"{core_features}, running in neon city street, cyberpunk background, crowd silhouettes, pink and cyan lighting, urban scene, full body",
    "Gemini_Generated_Image_ywz63oywz63oywz6.png": f"{core_features}, back view, walking in cyberpunk city, neon signs, pink and cyan lights, urban night scene, wet street reflections, full body",
    "Gemini_Generated_Image_vwyl07vwyl07vwyl.png": f"{core_features}, back view, standing in neon city, cyberpunk street, pink and cyan neon signs, urban environment, crowd silhouettes, full body",
    "Gemini_Generated_Image_ywbja7ywbja7ywbj.png": f"{core_features}, cyberpunk city scene, neon environment, pink and cyan lights, urban setting, full body",

    # Sitting poses - indoor/cozy environments
    "Gemini_Generated_Image_cktir1cktir1ckti.png": f"{core_features}, sitting on couch, relaxed pose, indoor setting, warm lighting, living room, bookshelf background, lamp light, daytime through window",

    # Sitting poses - cyberpunk/bar environments
    "Gemini_Generated_Image_3p5v9x3p5v9x3p5v.png": f"{core_features}, sitting on bar stool, casual pose, cyberpunk bar interior, neon signs, pink and cyan lighting, people in background, nighttime",
    "Gemini_Generated_Image_yvci9myvci9myvci.png": f"{core_features}, sitting on bar stool, relaxed stance, cyberpunk diner, neon lighting, purple and pink glow, interior scene, nighttime atmosphere",

    # Sitting poses - rooftop/outdoor
    "Gemini_Generated_Image_5fh4u65fh4u65fh4.png": f"{core_features}, sitting on ledge, legs dangling, rooftop view, cyberpunk city skyline, skyscrapers, daytime, blue sky, urban environment, contemplative pose",
    "Gemini_Generated_Image_davogidavogidavo.png": f"{core_features}, sitting on ledge, legs dangling, rooftop, cyberpunk city at night, neon lights, pink and cyan glow, urban skyline, nighttime atmosphere",

    # Additional varied poses
    "Gemini_Generated_Image_7yo90h7yo90h7yo9.png": f"{core_features}, full body, standing pose, white background",
    "Gemini_Generated_Image_b1gnbrb1gnbrb1gn.png": f"{core_features}, full body, standing pose, white background",
    "Gemini_Generated_Image_c4ak7tc4ak7tc4ak.png": f"{core_features}, full body, standing pose, white background",
    "Gemini_Generated_Image_h8zca6h8zca6h8zc.png": f"{core_features}, full body, standing pose, white background",
    "Gemini_Generated_Image_m7yskmm7yskmm7ys.png": f"{core_features}, full body, standing pose, white background",
    "Gemini_Generated_Image_mw1uz3mw1uz3mw1u.png": f"{core_features}, full body, standing pose, white background",
    "Gemini_Generated_Image_oauwwvoauwwvoauw.png": f"{core_features}, full body, standing pose, white background",
    "Gemini_Generated_Image_p3vej8p3vej8p3ve.png": f"{core_features}, full body, standing pose, white background",
}

# Apply generic caption to any not specifically defined
print("Updating captions for LoRA training optimization...\n")

image_files = [f for f in os.listdir(training_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

for img_file in image_files:
    txt_file = os.path.splitext(img_file)[0] + '.txt'
    txt_path = os.path.join(training_dir, txt_file)

    # Get caption (use specific or generate generic one)
    if img_file in captions:
        caption = captions[img_file]
        print(f"[OK] {img_file}: Custom caption")
    else:
        # Generic caption for unspecified images
        caption = f"{core_features}, full body, standing, white background"
        print(f"[*] {img_file}: Generic caption")

    # Write caption file
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(caption)

print(f"\n[DONE] Updated {len(image_files)} caption files")
print("\nOptimizations applied:")
print("- Removed redundant style descriptors")
print("- Focused on unique aspects per image")
print("- Consistent core character features")
print("- Concise, tag-based format")
