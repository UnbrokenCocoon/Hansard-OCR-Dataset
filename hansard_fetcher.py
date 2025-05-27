import os
import requests
from tqdm import tqdm

# Step 1: Set up destination folder
output_dir = "hansard_zips"
os.makedirs(output_dir, exist_ok=True)

# Step 2: Download the list of ZIP URLs
url_list_url = "https://raw.githubusercontent.com/econandrew/uk-hansard-archive-urls/master/urls.txt"
response = requests.get(url_list_url)
urls = response.text.strip().splitlines()

# Step 3: Basic check for ZIP file URLs
valid_urls = [url for url in urls if url.lower().endswith(".zip")]

# Step 4: Download each file if not already present
for url in tqdm(valid_urls, desc="Downloading Hansard ZIPs"):
    filename = os.path.basename(url)
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        continue  # Skip already downloaded files

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"❌ Failed to download {url} — {e}")
