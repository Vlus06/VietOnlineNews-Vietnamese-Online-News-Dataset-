import pandas as pd

from src.paths import (
    TRAIN_PARQUET_PATH,
    DEV_PARQUET_PATH,
    TEST_PARQUET_PATH,
    NEWS_METADATA_PARQUET_PATH,
)


ID_CANDIDATES = ["id", "clean_id", "article_id"]


def _find_id_column(df):
    for col in ID_CANDIDATES:
        if col in df.columns:
            return col
    raise ValueError(
        f"Không tìm thấy cột id. Các cột hiện có: {df.columns.tolist()}"
    )


def _read_split_file(path, split_name):
    if not path.exists():
        return None

    df = pd.read_parquet(path)
    df["split"] = split_name

    return df


def _load_splits():
    split_files = [
        (TRAIN_PARQUET_PATH, "train"),
        (DEV_PARQUET_PATH, "dev"),
        (TEST_PARQUET_PATH, "test"),
    ]

    dfs = []

    for path, split_name in split_files:
        df = _read_split_file(path, split_name)
        if df is not None:
            dfs.append(df)

    if not dfs:
        raise FileNotFoundError(
            "Không tìm thấy train/dev/test parquet trong data/processed/. "
            "Hãy chạy: python scripts/download_data.py"
        )

    return pd.concat(dfs, ignore_index=True)


def _load_metadata():
    if not NEWS_METADATA_PARQUET_PATH.exists():
        return None

    return pd.read_parquet(NEWS_METADATA_PARQUET_PATH)


def _merge_with_metadata(df_text, df_meta):
    if df_meta is None:
        return df_text

    text_id_col = _find_id_column(df_text)
    meta_id_col = _find_id_column(df_meta)

    # Nếu tên id khác nhau thì đổi metadata về cùng tên với split
    if meta_id_col != text_id_col:
        df_meta = df_meta.rename(columns={meta_id_col: text_id_col})

    # Tránh trùng cột category vì train/dev/test đã có category
    duplicated_cols = [
        col for col in df_meta.columns
        if col in df_text.columns and col != text_id_col
    ]

    df_meta = df_meta.drop(columns=duplicated_cols, errors="ignore")

    df = df_text.merge(
        df_meta,
        on=text_id_col,
        how="left"
    )

    return df


def _normalize_datetime(df):
    if "public_date" not in df.columns:
        return df

    public_date = pd.to_datetime(
        df["public_date"],
        errors="coerce",
        utc=True
    )

    try:
        public_date = (
            public_date
            .dt.tz_convert("Asia/Ho_Chi_Minh")
            .dt.tz_localize(None)
        )
    except Exception:
        public_date = pd.to_datetime(df["public_date"], errors="coerce")

    df["public_date"] = public_date

    return df


def _ensure_text_features(df):
    text_cols = [
        col for col in ["title", "description", "content"]
        if col in df.columns
    ]

    if "full_text" not in df.columns:
        if text_cols:
            df["full_text"] = (
                df[text_cols]
                .fillna("")
                .astype(str)
                .agg(" ".join, axis=1)
                .str.strip()
            )
        else:
            df["full_text"] = ""

    if "title_wc" not in df.columns and "title" in df.columns:
        df["title_wc"] = df["title"].fillna("").astype(str).str.split().str.len()

    if "description_wc" not in df.columns and "description" in df.columns:
        df["description_wc"] = (
            df["description"]
            .fillna("")
            .astype(str)
            .str.split()
            .str.len()
        )

    if "content_wc" not in df.columns and "content" in df.columns:
        df["content_wc"] = (
            df["content"]
            .fillna("")
            .astype(str)
            .str.split()
            .str.len()
        )

    if "full_text_wc" not in df.columns:
        df["full_text_wc"] = (
            df["full_text"]
            .fillna("")
            .astype(str)
            .str.split()
            .str.len()
        )

    return df


def load_news_data():
    df_text = _load_splits()
    df_meta = _load_metadata()

    df = _merge_with_metadata(df_text, df_meta)
    df = _normalize_datetime(df)
    df = _ensure_text_features(df)

    return df