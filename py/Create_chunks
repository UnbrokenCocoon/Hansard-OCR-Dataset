import os
import pickle
from pathlib import Path
from bs4 import BeautifulSoup
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_speeches_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")
    contributions = soup.find_all("membercontribution")
    speeches = [clean_text(contrib.get_text()) for contrib in contributions]
    return speeches

def chunk_speeches(speeches, chunk_size=800):
    chunks, current_chunk = [], []
    current_word_count = 0

    for speech in speeches:
        words = speech.split()
        if current_word_count + len(words) > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0
        current_chunk.append(speech)
        current_word_count += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def process_directory(input_dir, output_dir, max_files=20, chunk_size=800):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.rglob("*.xml"))
    processed = 0
    batch_count = 0

    for file in files:
        if processed >= max_files:
            break
        speeches = extract_speeches_from_file(file)
        chunks = chunk_speeches(speeches, chunk_size=chunk_size)

        if chunks:
            output_path = output_dir / f"hansard_800chunk_{batch_count:05}.pkl"
            with open(output_path, "wb") as f:
                pickle.dump(chunks, f)
            print(f"✅ Saved: {output_path.name} ({len(chunks)} chunks)")
            batch_count += 1
        else:
            print(f"⚠️ No valid speeches found in: {file.name}")
        processed += 1

# Example usage
process_directory(
    input_dir=r"", #specify clone location first
    output_dir=r"",
    max_files=200,
    chunk_size=800
)
