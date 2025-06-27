import argparse
import os
import glob
from PIL import Image

from datasets import Dataset, DatasetDict, Features, Value
from datasets.features import Image as HFImage

from sklearn.model_selection import train_test_split


def parse_args():
    parser = argparse.ArgumentParser(description="Create a Hugging Face OCR dataset from image-text pairs")
    parser.add_argument("--root_dir", type=str, required=True,
                        help="Directory containing .jpg/.txt image-text pairs")
    parser.add_argument("--save_path", type=str, required=True,
                        help="Path to save the processed dataset")
    parser.add_argument("--test_size", type=float, default=0.1,
                        help="Proportion of data for validation set")
    return parser.parse_args()


def collect_examples(folder):
    examples = []
    for dirpath, _, _ in os.walk(folder):
        for jpg_path in glob.glob(os.path.join(dirpath, "*.jpg")):
            txt_path = jpg_path[:-4] + ".txt"
            if os.path.exists(txt_path):
                with open(txt_path, encoding="utf-8") as f:
                    text = f.read().strip()
                if text:
                    examples.append({"image": jpg_path, "text": text})
    return examples


def main():
    args = parse_args()

    print("🔍 Collecting image–text pairs...")
    data = collect_examples(args.root_dir)
    print(f"✅ Collected {len(data)} image–text pairs")

    features = Features({"image": HFImage(), "text": Value("string")})
    raw_dataset = Dataset.from_list(data, features=features)

    print("SplitOptions splitting into train/test...")
    train_ds, test_ds = train_test_split(raw_dataset, test_size=args.test_size, random_state=42)
    dataset = DatasetDict(train=train_ds, test=test_ds)

    print("💾 Saving dataset to disk...")
    dataset.save_to_disk(args.save_path)
    print(f"Dataset saved at: {args.save_path}")


if __name__ == "__main__":
    main()
