from pathlib import Path
import json

import numpy as np
import pandas as pd


PROCESSED_DIR = Path("data/processed")
CACHE_DIR = Path("data/dashboard_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = PROCESSED_DIR / "train.parquet"
DEV_PATH = PROCESSED_DIR / "dev.parquet"
TEST_PATH = PROCESSED_DIR / "test.parquet"
META_PATH = PROCESSED_DIR / "news_metadata.parquet"


def load_split(path: Path, split_name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {path}")

    df = pd.read_parquet(path)
    df["split"] = split_name
    return df


def normalize_public_date(df: pd.DataFrame) -> pd.DataFrame:
    if "public_date" not in df.columns:
        return df

    df["public_date"] = pd.to_datetime(
        df["public_date"],
        errors="coerce",
        utc=True,
    )

    df["public_date"] = (
        df["public_date"]
        .dt.tz_convert("Asia/Ho_Chi_Minh")
        .dt.tz_localize(None)
    )

    return df


def create_text_features(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["title", "description", "content"]:
        if col not in df.columns:
            df[col] = ""

    df["title"] = df["title"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)
    df["content"] = df["content"].fillna("").astype(str)

    df["title_wc"] = df["title"].str.split().str.len()
    df["description_wc"] = df["description"].str.split().str.len()
    df["content_wc"] = df["content"].str.split().str.len()

    df["full_text"] = (
        df["title"] + " " + df["description"] + " " + df["content"]
    ).str.strip()

    df["full_text_wc"] = df["full_text"].str.split().str.len()

    return df


def save_overview(df: pd.DataFrame) -> None:
    overview = {
        "n_rows": int(len(df)),
        "n_columns": int(df.shape[1]),
        "n_categories": int(df["category"].nunique()) if "category" in df.columns else None,
        "n_sources": int(df["source"].nunique()) if "source" in df.columns else None,
        "min_date": str(df["public_date"].min()) if "public_date" in df.columns else None,
        "max_date": str(df["public_date"].max()) if "public_date" in df.columns else None,
        "avg_full_text_wc": float(df["full_text_wc"].mean()) if "full_text_wc" in df.columns else None,
        "median_full_text_wc": float(df["full_text_wc"].median()) if "full_text_wc" in df.columns else None,
        "p99_full_text_wc": float(df["full_text_wc"].quantile(0.99)) if "full_text_wc" in df.columns else None,
        "max_full_text_wc": float(df["full_text_wc"].max()) if "full_text_wc" in df.columns else None,
    }

    with open(CACHE_DIR / "overview.json", "w", encoding="utf-8") as f:
        json.dump(overview, f, ensure_ascii=False, indent=2)


def save_category_distribution(df: pd.DataFrame) -> None:
    category_distribution = (
        df["category"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    category_distribution.columns = ["category", "count"]
    category_distribution["percent"] = (
        category_distribution["count"] / category_distribution["count"].sum() * 100
    ).round(2)

    category_distribution.to_parquet(
        CACHE_DIR / "category_distribution.parquet",
        index=False,
    )


def save_source_distribution(df: pd.DataFrame) -> None:
    source_distribution = (
        df["source"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    source_distribution.columns = ["source", "count"]
    source_distribution["percent"] = (
        source_distribution["count"] / source_distribution["count"].sum() * 100
    ).round(2)

    source_distribution.to_parquet(
        CACHE_DIR / "source_distribution.parquet",
        index=False,
    )


def save_split_distribution(df: pd.DataFrame) -> None:
    split_distribution = (
        df["split"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    split_distribution.columns = ["split", "count"]
    split_distribution["percent"] = (
        split_distribution["count"] / split_distribution["count"].sum() * 100
    ).round(2)

    split_distribution.to_parquet(
        CACHE_DIR / "split_distribution.parquet",
        index=False,
    )


def save_category_source_matrix(df: pd.DataFrame) -> None:
    category_source = (
        df.assign(
            category=df["category"].fillna("Unknown"),
            source=df["source"].fillna("Unknown"),
        )
        .groupby(["category", "source"])
        .size()
        .reset_index(name="count")
    )

    category_source.to_parquet(
        CACHE_DIR / "category_source_matrix.parquet",
        index=False,
    )


def save_time_distributions(df: pd.DataFrame) -> None:
    if "public_date" not in df.columns:
        pd.DataFrame(columns=["month_period", "count"]).to_parquet(
            CACHE_DIR / "monthly_distribution.parquet",
            index=False,
        )
        pd.DataFrame(columns=["month_period", "category", "count"]).to_parquet(
            CACHE_DIR / "monthly_category_distribution.parquet",
            index=False,
        )
        return

    temp_df = df.dropna(subset=["public_date"]).copy()

    if temp_df.empty:
        pd.DataFrame(columns=["month_period", "count"]).to_parquet(
            CACHE_DIR / "monthly_distribution.parquet",
            index=False,
        )
        pd.DataFrame(columns=["month_period", "category", "count"]).to_parquet(
            CACHE_DIR / "monthly_category_distribution.parquet",
            index=False,
        )
        return

    temp_df["month_period"] = temp_df["public_date"].dt.to_period("M").astype(str)

    monthly_distribution = (
        temp_df
        .groupby("month_period")
        .size()
        .reset_index(name="count")
    )

    monthly_distribution.to_parquet(
        CACHE_DIR / "monthly_distribution.parquet",
        index=False,
    )

    monthly_category_distribution = (
        temp_df.assign(category=temp_df["category"].fillna("Unknown"))
        .groupby(["month_period", "category"])
        .size()
        .reset_index(name="count")
    )

    monthly_category_distribution.to_parquet(
        CACHE_DIR / "monthly_category_distribution.parquet",
        index=False,
    )


def save_missing_summary(df: pd.DataFrame) -> None:
    missing_summary = df.isna().sum().reset_index()
    missing_summary.columns = ["column", "missing_count"]

    missing_summary["missing_rate_percent"] = (
        missing_summary["missing_count"] / len(df) * 100
    ).round(2)

    missing_summary = missing_summary.sort_values(
        "missing_count",
        ascending=False,
    )

    missing_summary.to_parquet(
        CACHE_DIR / "missing_summary.parquet",
        index=False,
    )


def save_length_summary_and_histogram(df: pd.DataFrame) -> None:
    length_cols = [
        col
        for col in ["title_wc", "description_wc", "content_wc", "full_text_wc"]
        if col in df.columns
    ]

    if not length_cols:
        pd.DataFrame().to_parquet(
            CACHE_DIR / "length_summary.parquet",
            index=False,
        )
        pd.DataFrame().to_parquet(
            CACHE_DIR / "length_histogram.parquet",
            index=False,
        )
        return

    length_summary = df[length_cols].describe().T.reset_index()
    length_summary = length_summary.rename(columns={"index": "field"})

    length_summary.to_parquet(
        CACHE_DIR / "length_summary.parquet",
        index=False,
    )

    full_text_wc = df["full_text_wc"].dropna().astype(float)

    if full_text_wc.empty:
        pd.DataFrame().to_parquet(
            CACHE_DIR / "length_histogram.parquet",
            index=False,
        )
        return

    upper_cap = full_text_wc.quantile(0.99)
    capped = full_text_wc[full_text_wc <= upper_cap]

    n_bins = 40
    counts, edges = np.histogram(capped, bins=n_bins)

    length_hist = pd.DataFrame(
        {
            "bin_left": edges[:-1],
            "bin_right": edges[1:],
            "bin_center": (edges[:-1] + edges[1:]) / 2,
            "count": counts,
            "is_outlier": False,
        }
    )

    outlier_count = int((full_text_wc > upper_cap).sum())

    if outlier_count > 0:
        outlier_row = pd.DataFrame(
            {
                "bin_left": [upper_cap],
                "bin_right": [full_text_wc.max()],
                "bin_center": [upper_cap],
                "count": [outlier_count],
                "is_outlier": [True],
            }
        )

        length_hist = pd.concat(
            [length_hist, outlier_row],
            ignore_index=True,
        )

    length_hist["bin_label"] = length_hist.apply(
        lambda row: (
            f"> {int(row['bin_left']):,}"
            if row["is_outlier"]
            else f"{int(row['bin_left']):,} - {int(row['bin_right']):,}"
        ),
        axis=1,
    )

    length_hist.to_parquet(
        CACHE_DIR / "length_histogram.parquet",
        index=False,
    )


def save_preview_sample(df: pd.DataFrame) -> None:
    preview_cols = [
        "id",
        "split",
        "source",
        "category",
        "sub_topic",
        "tag",
        "public_date",
        "title",
        "description",
        "url",
        "author",
        "full_text_wc",
    ]

    preview_cols = [col for col in preview_cols if col in df.columns]

    sample_parts = []

    if "category" in df.columns:
        for _, group in df.groupby("category", dropna=False):
            sample_parts.append(
                group.sample(
                    n=min(len(group), 100),
                    random_state=42,
                )
            )

        preview_sample = pd.concat(sample_parts, ignore_index=True)
    else:
        preview_sample = df.sample(
            n=min(len(df), 1000),
            random_state=42,
        ).reset_index(drop=True)

    preview_sample[preview_cols].to_parquet(
        CACHE_DIR / "preview_sample.parquet",
        index=False,
    )


def main() -> None:
    print("Loading splits...")

    train_df = load_split(TRAIN_PATH, "train")
    dev_df = load_split(DEV_PATH, "dev")
    test_df = load_split(TEST_PATH, "test")

    text_df = pd.concat(
        [train_df, dev_df, test_df],
        ignore_index=True,
    )

    print("Loading metadata...")

    if not META_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file metadata: {META_PATH}")

    meta_df = pd.read_parquet(META_PATH)

    if "id" not in text_df.columns:
        raise ValueError("Không tìm thấy cột id trong train/dev/test.")

    if "id" not in meta_df.columns:
        raise ValueError("Không tìm thấy cột id trong news_metadata.")

    meta_cols_to_drop = [
        col
        for col in meta_df.columns
        if col in text_df.columns and col != "id"
    ]

    meta_df = meta_df.drop(columns=meta_cols_to_drop, errors="ignore")

    print("Merging...")

    df = text_df.merge(
        meta_df,
        on="id",
        how="left",
    )

    print("Creating text features...")

    df = normalize_public_date(df)
    df = create_text_features(df)

    print("Saving dashboard cache...")

    save_overview(df)
    save_category_distribution(df)
    save_source_distribution(df)
    save_split_distribution(df)
    save_category_source_matrix(df)
    save_time_distributions(df)
    save_missing_summary(df)
    save_length_summary_and_histogram(df)
    save_preview_sample(df)

    print("Dashboard cache created successfully.")
    print(f"Cache saved to: {CACHE_DIR}")


if __name__ == "__main__":
    main()