import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import streamlit as st
import plotly.express as px

from src.data_loader import load_news_data
from src.eda_utils import (
    filter_dataframe,
    get_category_distribution,
    get_source_distribution,
    get_split_distribution,
    get_category_source_matrix,
    get_monthly_distribution,
    get_monthly_category_distribution,
    get_missing_summary,
    get_text_length_summary,
)


st.set_page_config(
    page_title="VietOnlineNews Dashboard",
    page_icon="📰",
    layout="wide",
)


@st.cache_data(show_spinner="Đang tải dữ liệu...")
def load_data():
    return load_news_data()


st.title("📰 VietOnlineNews Dashboard")
st.markdown(
    """
Dashboard tương tác cho bộ dữ liệu **VietOnlineNews**.  
Người dùng có thể lọc dữ liệu theo nguồn báo, chủ đề, split, thời gian, từ khóa
và quan sát các biểu đồ EDA chính.
"""
)


try:
    df = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.info("Hãy chạy lệnh: `python scripts/download_data.py` trước khi mở dashboard.")
    st.stop()


# =========================
# Sidebar
# =========================

st.sidebar.header("Bộ lọc dữ liệu")

source_options = sorted(df["source"].dropna().unique()) if "source" in df.columns else []
category_options = sorted(df["category"].dropna().unique()) if "category" in df.columns else []
split_options = sorted(df["split"].dropna().unique()) if "split" in df.columns else []

selected_sources = st.sidebar.multiselect(
    "Nguồn báo",
    options=source_options,
    default=source_options,
)

selected_categories = st.sidebar.multiselect(
    "Chủ đề",
    options=category_options,
    default=category_options,
)

selected_splits = None
if split_options:
    selected_splits = st.sidebar.multiselect(
        "Tập dữ liệu",
        options=split_options,
        default=split_options,
    )

keyword = st.sidebar.text_input("Tìm kiếm từ khóa")

length_range = None
if "full_text_wc" in df.columns:
    min_len = int(df["full_text_wc"].min())
    max_len = int(df["full_text_wc"].max())

    length_range = st.sidebar.slider(
        "Khoảng độ dài văn bản",
        min_value=min_len,
        max_value=max_len,
        value=(min_len, max_len),
    )

date_range = None
if "public_date" in df.columns and df["public_date"].notna().any():
    min_date = df["public_date"].min().date()
    max_date = df["public_date"].max().date()

    date_range = st.sidebar.date_input(
        "Khoảng thời gian",
        value=(min_date, max_date),
    )


filtered_df = filter_dataframe(
    df=df,
    selected_sources=selected_sources,
    selected_categories=selected_categories,
    selected_splits=selected_splits,
    date_range=date_range,
    keyword=keyword,
    length_range=length_range,
)


# =========================
# KPI
# =========================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Số bài", f"{len(filtered_df):,}")
col2.metric("Số chủ đề", filtered_df["category"].nunique() if "category" in filtered_df.columns else 0)
col3.metric("Số nguồn", filtered_df["source"].nunique() if "source" in filtered_df.columns else 0)
col4.metric("Số split", filtered_df["split"].nunique() if "split" in filtered_df.columns else 0)

if "full_text_wc" in filtered_df.columns and len(filtered_df) > 0:
    col5.metric("Độ dài TB", f"{filtered_df['full_text_wc'].mean():.0f} từ")
else:
    col5.metric("Độ dài TB", "N/A")


# =========================
# Tabs
# =========================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Tổng quan",
        "Chất lượng dữ liệu",
        "Phân phối",
        "Thời gian",
        "Độ dài văn bản",
        "Khám phá dữ liệu",
    ]
)


with tab1:
    st.subheader("Tổng quan dữ liệu")

    overview = pd.DataFrame(
        {
            "Chỉ số": [
                "Số dòng sau lọc",
                "Số cột",
                "Số chủ đề",
                "Số nguồn báo",
                "Ngày sớm nhất",
                "Ngày muộn nhất",
            ],
            "Giá trị": [
                f"{len(filtered_df):,}",
                filtered_df.shape[1],
                filtered_df["category"].nunique() if "category" in filtered_df.columns else "N/A",
                filtered_df["source"].nunique() if "source" in filtered_df.columns else "N/A",
                filtered_df["public_date"].min() if "public_date" in filtered_df.columns else "N/A",
                filtered_df["public_date"].max() if "public_date" in filtered_df.columns else "N/A",
            ],
        }
    )

    st.dataframe(overview, use_container_width=True)

    st.subheader("Preview dữ liệu")
    st.dataframe(filtered_df.head(30), use_container_width=True)


with tab2:
    st.subheader("Missing Values")

    missing_summary = get_missing_summary(filtered_df)

    missing_nonzero = missing_summary[missing_summary["missing_count"] > 0]

    if not missing_nonzero.empty:
        fig = px.bar(
            missing_nonzero,
            x="missing_count",
            y="column",
            orientation="h",
            text="missing_rate_percent",
            title="Số lượng missing theo cột",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("Không có missing values trong dữ liệu sau khi lọc.")

    st.dataframe(missing_summary, use_container_width=True)


with tab3:
    st.subheader("Phân phối chủ đề")

    category_dist = get_category_distribution(filtered_df)

    if not category_dist.empty:
        fig = px.bar(
            category_dist.sort_values("count"),
            x="count",
            y="category",
            orientation="h",
            text="count",
            title="Số bài theo chủ đề",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(category_dist, use_container_width=True)

        imbalance_ratio = category_dist["count"].max() / category_dist["count"].min()
        st.info(f"Imbalance ratio: {imbalance_ratio:.2f}x")
    else:
        st.warning("Không có dữ liệu category để hiển thị.")

    st.subheader("Phân phối nguồn báo")

    source_dist = get_source_distribution(filtered_df)

    if not source_dist.empty:
        fig = px.pie(
            source_dist,
            names="source",
            values="count",
            title="Tỉ lệ bài theo nguồn báo",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Phân phối train/dev/test")

    split_dist = get_split_distribution(filtered_df)

    if not split_dist.empty:
        fig = px.bar(
            split_dist,
            x="split",
            y="count",
            text="count",
            title="Số bài theo split",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Heatmap Category × Source")

    matrix = get_category_source_matrix(filtered_df)

    if not matrix.empty:
        fig = px.imshow(
            matrix,
            text_auto=True,
            aspect="auto",
            title="Số bài theo Category và Source",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Không đủ dữ liệu để vẽ heatmap.")


with tab4:
    st.subheader("Số bài theo tháng")

    monthly_dist = get_monthly_distribution(filtered_df)

    if not monthly_dist.empty:
        fig = px.line(
            monthly_dist,
            x="month_period",
            y="count",
            markers=True,
            title="Xu hướng số bài theo tháng",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Xu hướng theo chủ đề")

    monthly_category_dist = get_monthly_category_distribution(filtered_df)

    if not monthly_category_dist.empty:
        fig = px.line(
            monthly_category_dist,
            x="month_period",
            y="count",
            color="category",
            title="Xu hướng chủ đề theo tháng",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Không có dữ liệu thời gian hợp lệ.")


with tab5:
    st.subheader("Thống kê độ dài văn bản")

    length_summary = get_text_length_summary(filtered_df)

    if not length_summary.empty:
        st.dataframe(length_summary, use_container_width=True)

    if "full_text_wc" in filtered_df.columns:
        fig = px.histogram(
            filtered_df,
            x="full_text_wc",
            nbins=80,
            title="Phân phối độ dài full_text",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Không có cột full_text_wc.")


with tab6:
    st.subheader("Bảng dữ liệu sau khi lọc")

    display_cols = [
        "id",
        "clean_id",
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

    display_cols = [col for col in display_cols if col in filtered_df.columns]

    st.caption("Chỉ hiển thị tối đa 1000 dòng đầu để dashboard chạy mượt hơn.")

    st.dataframe(
        filtered_df[display_cols].head(1000),
        use_container_width=True,
        height=550,
    )

    csv_data = filtered_df[display_cols].to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="Tải dữ liệu sau khi lọc",
        data=csv_data,
        file_name="filtered_viet_online_news.csv",
        mime="text/csv",
    )