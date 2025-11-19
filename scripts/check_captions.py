import os
import re

folder = r"C:\Users\User\Desktop\ComfyUI_lizz\lora_training_images"
txt_files = sorted([f for f in os.listdir(folder) if f.endswith('.txt')])

print(f"Checking {len(txt_files)} caption files...\n")

issues = []

for txt_file in txt_files:
    filepath = os.path.join(folder, txt_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        caption = f.read().strip()
    
    # Check if starts with lizzchar
    if not caption.startswith('lizzchar'):
        issues.append(f"{txt_file}: Doesn't start with 'lizzchar'")
    
    # Check for duplicate consecutive phrases
    parts = [p.strip() for p in caption.split(',')]
    for i in range(len(parts) - 1):
        if parts[i] and parts[i] == parts[i+1]:
            issues.append(f"{txt_file}: Duplicate consecutive phrase '{parts[i]}'")
    
    # Check for duplicate non-consecutive phrases
    seen = set()
    for part in parts:
        if part and part in seen:
            issues.append(f"{txt_file}: Duplicate phrase '{part}'")
        seen.add(part)
    
    # Check for typos
    if 'waiste' in caption:
        issues.append(f"{txt_file}: Typo 'waiste'")

if issues:
    print("=" * 80)
    print("ISSUES FOUND:")
    print("=" * 80)
    for issue in issues:
        print(f"  - {issue}")
    print(f"\nTotal issues: {len(issues)}")
else:
    print("=" * 80)
    print("NO ISSUES FOUND!")
    print("=" * 80)
    print(f"All {len(txt_files)} caption files are coherent and consistent!")
