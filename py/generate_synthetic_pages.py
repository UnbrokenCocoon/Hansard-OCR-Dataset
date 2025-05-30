
import os
import pickle
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import random
from tqdm import tqdm

# === Configuration ===
pkl_path = r"C:\Users\t\PycharmProjects\bertopic\parsed_output\hansard_chunks.pkl"
font_path = "arial.ttf"  # Or e.g. "times.ttf" for book-style realism
image_size = (768, 1024)
final_size = (384, 512)
batch_size = 10000
output_root = "synthetic_pages"
os.makedirs(output_root, exist_ok=True)

# === Load data ===
with open(pkl_path, "rb") as f:
    data_chunks = pickle.load(f)

# === Generator ===
def generate_synthetic_page(text, width, height, font_path, font_size=20):
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    x, y = 80, 80
    line_height = font_size + 6
    max_chars = 90

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            y += line_height
            continue
        for i in range(0, len(line), max_chars):
            draw.text((x, y), line[i:i+max_chars], font=font, fill='black')
            y += line_height
            if y > height - 80:
                break

    img = np.array(image)

    # Augmentations
    angle = random.choice([0, -2, -1, 1, 2])
    M = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1.0)
    img = cv2.warpAffine(img, M, (width, height), borderValue=(255, 255, 255))

    blur_kernel = random.choice([None, (3, 3), (5, 5)])
    if blur_kernel:
        img = cv2.GaussianBlur(img, blur_kernel, 0.8)

    if random.choice([True, False]):
        noise = np.random.normal(0, 8, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)

    if random.choice([True, False]):
        tint = np.full_like(img, (240, 230, 210))
        img = cv2.addWeighted(img, 0.9, tint, 0.1, 0)

    return Image.fromarray(img)

# === Batch loop with existing file check ===
total = len(data_chunks)

for i in range(0, total, batch_size):
    batch = data_chunks[i:i+batch_size]
    batch_index = i // batch_size
    out_dir = os.path.join(output_root, f"batch_{batch_index:03d}")
    os.makedirs(out_dir, exist_ok=True)

    metadata_path = os.path.join(out_dir, "metadata.jsonl")
    existing_files = set(os.listdir(out_dir)) if os.path.exists(out_dir) else set()

    metadata = []

    for j, item in enumerate(tqdm(batch, desc=f"Batch {batch_index:03d}")):
        filename = f"{batch_index:03d}_{j:05d}.jpg"
        if filename in existing_files:
            continue  # Already exists

        try:
            img = generate_synthetic_page(item["content"], *image_size, font_path)
            img = img.resize(final_size, resample=Image.BICUBIC)
            img.save(os.path.join(out_dir, filename), quality=80, optimize=True)
            metadata.append({"filename": filename, "text": item["content"]})
        except Exception as e:
            print(f"❌ Failed for index {i + j}: {e}")

    if metadata:
        with open(metadata_path, "a", encoding="utf-8") as f:
            for entry in metadata:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Batch {batch_index:03d}: {len(metadata)} new images saved.")
