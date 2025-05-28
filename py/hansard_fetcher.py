import os
import requests
import zipfile
from tqdm import tqdm

# === Step 1: Set up folders ===
output_dir = "hansard_zips"
extracted_dir = "hansard_extracted"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(extracted_dir, exist_ok=True)

# === Step 2: Download the list of ZIP URLs ===
url_list_url = "https://raw.githubusercontent.com/econandrew/uk-hansard-archive-urls/master/urls.txt"
response = requests.get(url_list_url)
urls = response.text.strip().splitlines()

# === Step 3: Filter valid ZIP URLs ===
valid_urls = [url for url in urls if url.lower().endswith(".zip")]

# === Step 4: Download ZIP files ===
error_list = []

for url in tqdm(valid_urls, desc="Downloading Hansard ZIPs"):
    filename = os.path.basename(url)
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        continue  # Skip already downloaded

    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        error_list.append((url, str(e)))

# === Step 5: Check for missing files ===
downloaded_files = set(os.listdir(output_dir))
expected_files = set(os.path.basename(url) for url in valid_urls)
missing_files = expected_files - downloaded_files

# === Step 6: Extract ZIP files ===
bad_zip_list = []

for filename in tqdm(os.listdir(output_dir), desc="Extracting ZIP files"):
    if not filename.lower().endswith(".zip"):
        continue

    zip_path = os.path.join(output_dir, filename)
    extract_path = os.path.join(extracted_dir, os.path.splitext(filename)[0])

    if os.path.exists(extract_path):
        continue  # Skip already extracted

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile as e:
        bad_zip_list.append((filename, str(e)))

# === Final Summary ===
if error_list:
    print(f"\n❌ {len(error_list)} downloads failed:")
    with open("download_errors.txt", "w") as f:
        for url, err in error_list:
            print(f" - {url} — {err}")
            f.write(f"{url}\t{err}\n")

if missing_files:
    print(f"\n⚠️ {len(missing_files)} files missing after download:")
    with open("missing_files.txt", "w") as f:
        for fname in sorted(missing_files):
            print(f" - {fname}")
            f.write(fname + "\n")

if bad_zip_list:
    print(f"\n❌ {len(bad_zip_list)} bad ZIP files:")
    with open("bad_zip_files.txt", "w") as f:
        for fname, err in bad_zip_list:
            print(f" - {fname} — {err}")
            f.write(f"{fname}\t{err}\n")

if not (error_list or missing_files or bad_zip_list):
    print("\n✅ All files downloaded and extracted successfully.")
