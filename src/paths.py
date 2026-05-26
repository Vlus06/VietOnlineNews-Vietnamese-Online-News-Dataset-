from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "rawdata"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

TRAIN_PARQUET_PATH = PROCESSED_DATA_DIR / "train.parquet"
DEV_PARQUET_PATH = PROCESSED_DATA_DIR / "dev.parquet"
TEST_PARQUET_PATH = PROCESSED_DATA_DIR / "test.parquet"
NEWS_METADATA_PARQUET_PATH = PROCESSED_DATA_DIR / "news_metadata.parquet"

TRAIN_CSV_PATH = PROCESSED_DATA_DIR / "train.csv"
DEV_CSV_PATH = PROCESSED_DATA_DIR / "dev.csv"
TEST_CSV_PATH = PROCESSED_DATA_DIR / "test.csv"
NEWS_METADATA_CSV_PATH = PROCESSED_DATA_DIR / "news_metadata.csv"