from pathlib import Path
from huggingface_hub import hf_hub_download

REPO_ID = "VLUS06/VietOnlineNews"
REPO_TYPE = "dataset"

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = [
    "train.parquet",
    "dev.parquet",
    "test.parquet",
    "news_metadata.parquet",
]

for file_name in files:
    output_path = OUTPUT_DIR / file_name

    if output_path.exists():
        print(f"Already exists: {output_path}")
        continue

    print(f"Downloading {file_name}...")

    path = hf_hub_download(
        repo_id=REPO_ID,
        filename=file_name,
        repo_type=REPO_TYPE,
        local_dir=OUTPUT_DIR,
    )

    print(f"Saved to {path}")

print("Dataset is ready.")