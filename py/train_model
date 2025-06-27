import argparse
import os

from datasets import load_from_disk

from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    default_data_collator,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Train a TrOCR OCR model on a preprocessed dataset")
    parser.add_argument("--dataset_path", type=str, required=True,
                        help="Path to the preprocessed dataset")
    parser.add_argument("--output_dir", type=str, default="./trocr-ocr-model",
                        help="Directory to save trained model and logs")
    parser.add_argument("--batch_size", type=int, default=8,
                        help="Batch size per device during training")
    parser.add_argument("--num_train_epochs", type=int, default=5,
                        help="Number of training epochs")
    parser.add_argument("--fp16", action="store_true",
                        help="Use FP16 precision if available")
    parser.add_argument("--save_strategy", type=str, default="epoch",
                        choices=["no", "epoch", "steps"],
                        help="When to save model checkpoints")
    parser.add_argument("--model_name", type=str, default="microsoft/trocr-base-stage1",
                        help="Base model to fine-tune")
    return parser.parse_args()


def main():
    args = parse_args()

    print("📂 Loading preprocessed dataset...")
    dataset = load_from_disk(args.dataset_path)
    train_dataset = dataset["train"]
    eval_dataset = dataset["test"]

    print("🧮 Loading processor and model...")
    processor = TrOCRProcessor.from_pretrained(args.model_name, use_fast=True)
    model = VisionEncoderDecoderModel.from_pretrained(args.model_name)

    model.config.decoder_start_token_id = processor.tokenizer.cls_token_id
    model.config.pad_token_id = processor.tokenizer.pad_token_id
    model.config.vocab_size = model.decoder.config.vocab_size

    print("🏋️ Setting up training arguments...")
    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        eval_strategy="epoch",
        save_strategy=args.save_strategy,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.num_train_epochs,
        fp16=args.fp16,
        logging_dir=os.path.join(args.output_dir, "logs"),
        logging_steps=10,
        save_total_limit=2,
        predict_with_generate=True,
        remove_unused_columns=False,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=processor.image_processor,  # For image resizing, etc.
        data_collator=default_data_collator,
    )

    print("🚀 Starting training...")
    trainer.train()

    print("💾 Saving final model...")
    trainer.save_model(args.output_dir)
    print("✅ Training complete!")


if __name__ == "__main__":
    main()
