# 📜 Hansard OCR Dataset Builder

This project provides a full pipeline for downloading and preparing historical UK parliamentary debates (Hansard) for use in OCR training — particularly for applications in **digital humanities**, **historical NLP**, and **document layout modelling**.

---

## 📂 What This Project Does

✅ Downloads the complete digitised Hansard archive from 1800–2004 using a precompiled list of ZIP archive URLs  
✅ Extracts and converts debate text into **synthetic, book-style page images** paired with ground truth text  
✅ Supports augmentation and "denigration" (noise injection) to simulate historical document imperfections  
✅ Designed for OCR model fine-tuning, including projects using TrOCR or LayoutLM  
⚠️ **Large-scale** : Over 2,000 ZIPs, potentially hundreds of thousands of pages  

---

## 📟 Dataset Source

We use the ZIP archive list compiled by [econandrew/uk-hansard-archive-urls](https://github.com/econandrew/uk-hansard-archive-urls ). We thank the author for this essential index of the digitised Hansard archive.

The raw ZIP archives contain HTML-structured parliamentary debates across both houses of Parliament. This data is in the public domain.

---

## 📅 Scripts Overview

### `hansard_fetcher.py`

* Downloads all ZIP archives into `hansard_zips/`
* Skips existing files (safe to resume)
* Fetches from the `urls.txt` file in the referenced GitHub repo

### `dataset_creator.py`

* Extracts HTML from ZIPs
* Parses into column-paragraph structure
* Chunks into ~300-token blocks
* Renders text into synthetic A5-style page images using historical-style fonts
* Applies light noise, skew, and blur to simulate OCR input quality degradation
* Saves `.png + .txt` pairs in an output folder

### `create_dataset.py`

* Builds a Hugging Face-compatible OCR dataset from image-text `.png/.txt` pairs
* Splits into train/test sets
* Saves processed dataset to disk for reuse
* Accepts CLI args: `--root_dir`, `--save_path`, `--test_size`

### `train_trocr.py`

* Fine-tunes a TrOCR model on the synthetic image-text pairs
* Supports the HuggingFace `Seq2SeqTrainer` setup
* Includes options for mixed precision training, logging, evaluation, and model saving
* Accepts CLI args: `--dataset_path` , `--output_dir` , `--batch_size` , `--num_train_epochs` , `--fp16` , etc.
* Generates a fine-tuned OCR model ready for inference on historical scans

---

## 🧠 Intended Use

This dataset is ideal for:

* 🕵️‍♂️ OCR model training (e.g. TrOCR, Tesseract, LayoutLM)
* 📚 Digital humanities and historical research
* 📜 Document layout and semantic structure modelling
* 💡 Synthetic dataset generation at scale for benchmark creation

---

## 📊 Benefits

* Public domain: fully open for research and commercial use
* Historically rich: authentic political, rhetorical, and linguistic diversity
* Reproducible: built with plain Python, no dependency on proprietary formats
* Scalable: millions of lines of ground-truth-aligned content

---

## 🔧 Next Steps

1. Run `hansard_fetcher.py` to download all source data  
2. Use `dataset_creator.py` to:
   - Extract and clean content
   - Generate synthetic A5-style page images
   - Apply stochastic degradation (augmentation)  
3. Run `create_dataset.py` to build a Hugging Face-ready OCR dataset:
```bash
python create_dataset.py --root_dir ./pages --save_path ./hf_dataset --test_size 0.1
4. Train a model with train_trocr.py:
```bash
python train_trocr.py --dataset_path ./hf_dataset --output_dir ./trocr_model --batch_size 16 --fp16
## 📅 License

The Hansard data is public domain (UK Crown Copyright).
Code in this repository is released under the MIT License.

---

## 🤝 Acknowledgements

* Archive URLs: [https://github.com/econandrew/uk-hansard-archive-urls](https://github.com/econandrew/uk-hansard-archive-urls)
* Hansard archives provided by: UK Parliament Digital Archive
