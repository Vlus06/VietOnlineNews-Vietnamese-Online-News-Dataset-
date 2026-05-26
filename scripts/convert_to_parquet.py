from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

PROCESSED_DIR = Path("data/processed")

files = [
    "train.csv",
    "dev.csv",
    "test.csv",
    "news_metadata.csv",
]

ROW_GROUP_SIZE = 5_000

for file_name in files:
    csv_path = PROCESSED_DIR / file_name
    parquet_path = PROCESSED_DIR / file_name.replace(".csv", ".parquet")

    if not csv_path.exists():
        print(f"Skip: {csv_path} not found")
        continue

    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False)

    print(f"Writing {parquet_path} with row_group_size={ROW_GROUP_SIZE}...")
    table = pa.Table.from_pandas(df, preserve_index=False)

    pq.write_table(
        table,
        parquet_path,
        compression="zstd",
        row_group_size=ROW_GROUP_SIZE,
        use_dictionary=True,
        write_statistics=True,
    )

    print(f"Done: {parquet_path}")