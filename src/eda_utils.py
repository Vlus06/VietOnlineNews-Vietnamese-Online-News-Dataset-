import pandas as pd


def filter_dataframe(
    df,
    selected_sources=None,
    selected_categories=None,
    selected_splits=None,
    date_range=None,
    keyword=None,
    length_range=None,
):
    filtered_df = df.copy()

    if selected_sources and "source" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["source"].isin(selected_sources)]

    if selected_categories and "category" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

    if selected_splits and "split" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["split"].isin(selected_splits)]

    if date_range is not None and len(date_range) == 2 and "public_date" in filtered_df.columns:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

        public_date = pd.to_datetime(filtered_df["public_date"], errors="coerce")

        filtered_df = filtered_df[
            (public_date >= start_date)
            & (public_date <= end_date)
        ]

    if keyword:
        keyword = keyword.lower().strip()

        candidate_cols = [
            "full_text_clean",
            "full_text",
            "title",
            "description",
            "content",
        ]

        search_cols = [col for col in candidate_cols if col in filtered_df.columns]

        if search_cols:
            mask = False

            for col in search_cols:
                mask = mask | (
                    filtered_df[col]
                    .fillna("")
                    .astype(str)
                    .str.lower()
                    .str.contains(keyword, regex=False)
                )

            filtered_df = filtered_df[mask]

    if length_range is not None and "full_text_wc" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["full_text_wc"].between(length_range[0], length_range[1])
        ]

    return filtered_df


def get_category_distribution(df):
    if "category" not in df.columns or df.empty:
        return pd.DataFrame(columns=["category", "count", "percent"])

    result = df["category"].value_counts().reset_index()
    result.columns = ["category", "count"]
    result["percent"] = (result["count"] / result["count"].sum() * 100).round(2)
    return result


def get_source_distribution(df):
    if "source" not in df.columns or df.empty:
        return pd.DataFrame(columns=["source", "count", "percent"])

    result = df["source"].value_counts().reset_index()
    result.columns = ["source", "count"]
    result["percent"] = (result["count"] / result["count"].sum() * 100).round(2)
    return result


def get_split_distribution(df):
    if "split" not in df.columns or df.empty:
        return pd.DataFrame(columns=["split", "count", "percent"])

    result = df["split"].value_counts().reset_index()
    result.columns = ["split", "count"]
    result["percent"] = (result["count"] / result["count"].sum() * 100).round(2)
    return result


def get_category_source_matrix(df):
    if "category" not in df.columns or "source" not in df.columns or df.empty:
        return pd.DataFrame()

    return pd.crosstab(df["category"], df["source"])


def get_monthly_distribution(df):
    if "public_date" not in df.columns or df.empty:
        return pd.DataFrame(columns=["month_period", "count"])

    temp_df = df.dropna(subset=["public_date"]).copy()

    if temp_df.empty:
        return pd.DataFrame(columns=["month_period", "count"])

    temp_df["month_period"] = temp_df["public_date"].dt.to_period("M").astype(str)

    result = (
        temp_df
        .groupby("month_period")
        .size()
        .reset_index(name="count")
    )

    return result


def get_monthly_category_distribution(df):
    if "public_date" not in df.columns or "category" not in df.columns or df.empty:
        return pd.DataFrame(columns=["month_period", "category", "count"])

    temp_df = df.dropna(subset=["public_date"]).copy()

    if temp_df.empty:
        return pd.DataFrame(columns=["month_period", "category", "count"])

    temp_df["month_period"] = temp_df["public_date"].dt.to_period("M").astype(str)

    result = (
        temp_df
        .groupby(["month_period", "category"])
        .size()
        .reset_index(name="count")
    )

    return result


def get_missing_summary(df):
    if df.empty:
        return pd.DataFrame(columns=["column", "missing_count", "missing_rate_percent"])

    result = df.isna().sum().reset_index()
    result.columns = ["column", "missing_count"]
    result["missing_rate_percent"] = (
        result["missing_count"] / len(df) * 100
    ).round(2)

    return result.sort_values("missing_count", ascending=False)


def get_text_length_summary(df):
    length_cols = [
        col for col in ["title_wc", "description_wc", "content_wc", "full_text_wc"]
        if col in df.columns
    ]

    if not length_cols:
        return pd.DataFrame()

    return df[length_cols].describe().T.reset_index().rename(columns={"index": "field"})