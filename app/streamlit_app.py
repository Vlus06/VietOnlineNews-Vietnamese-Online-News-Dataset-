import sys
import json
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


# =========================================================
# Page config
# =========================================================

st.set_page_config(
    page_title="VietOnlineNews Dashboard",
    page_icon="📰",
    layout="wide",
)


CACHE_DIR = ROOT_DIR / "data" / "dashboard_cache"


# =========================================================
# UI Style
# =========================================================

def inject_custom_css():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        .hero-card {
            padding: 2.1rem 2.3rem;
            border-radius: 28px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 48%, #334155 100%);
            color: white;
            margin-bottom: 1.4rem;
            box-shadow: 0 20px 48px rgba(15, 23, 42, 0.28);
        }

        .hero-title {
            font-size: 2.7rem;
            font-weight: 850;
            margin-bottom: 0.45rem;
            letter-spacing: -0.03em;
        }

        .hero-subtitle {
            font-size: 1.05rem;
            opacity: 0.94;
            line-height: 1.7;
        }

        .mode-note {
            padding: 1rem 1.2rem;
            border-radius: 18px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: #e0f2fe;
            margin-bottom: 1rem;
        }

        .metric-card {
            padding: 1.2rem 1.3rem;
            border-radius: 22px;
            background: #0f172a;
            border: 1px solid rgba(148, 163, 184, 0.25);
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.16);
            min-height: 124px;
        }

        .metric-label {
            font-size: 0.88rem;
            color: #94a3b8;
            margin-bottom: 0.45rem;
            font-weight: 700;
        }

        .metric-value {
            font-size: 1.62rem;
            font-weight: 850;
            color: #f8fafc;
            line-height: 1.2;
        }

        .metric-note {
            font-size: 0.82rem;
            color: #cbd5e1;
            margin-top: 0.4rem;
            line-height: 1.4;
        }

        .insight-card {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: #0f172a;
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-left: 5px solid #38bdf8;
            color: #e2e8f0;
            margin-bottom: 0.8rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
            min-height: 120px;
        }

        .insight-title {
            font-weight: 850;
            color: #f8fafc;
            margin-bottom: 0.35rem;
            font-size: 1rem;
        }

        .insight-body {
            color: #cbd5e1;
            line-height: 1.6;
            font-size: 0.94rem;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 850;
            margin-top: 1.1rem;
            margin-bottom: 0.75rem;
            letter-spacing: -0.01em;
        }

        div[data-testid="stMetric"] {
            background: #0f172a;
            border: 1px solid rgba(148, 163, 184, 0.2);
            padding: 1rem;
            border-radius: 18px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
        }

        div[data-testid="stTabs"] button {
            font-weight: 750;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">📰 VietOnlineNews Dashboard</div>
            <div class="hero-subtitle">
                Dashboard tương tác cho bộ dữ liệu tin tức trực tuyến tiếng Việt.
                Hệ thống hỗ trợ khám phá phân phối chủ đề, nguồn báo, thời gian,
                chất lượng dữ liệu và đặc điểm văn bản.
                <br>
                <b>Fast EDA Mode</b> sử dụng cache thống kê được tính sẵn từ toàn bộ dataset,
                giúp mở nhanh nhưng vẫn phản ánh đúng dữ liệu đầy đủ.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value, note="", icon="📌"):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight(title, body):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_custom_css()
render_hero()


# =========================================================
# Data loaders
# =========================================================

@st.cache_data(show_spinner="Đang tải EDA cache...")
def load_dashboard_cache():
    required_files = {
        "overview": CACHE_DIR / "overview.json",
        "category_distribution": CACHE_DIR / "category_distribution.parquet",
        "source_distribution": CACHE_DIR / "source_distribution.parquet",
        "split_distribution": CACHE_DIR / "split_distribution.parquet",
        "category_source_matrix": CACHE_DIR / "category_source_matrix.parquet",
        "monthly_distribution": CACHE_DIR / "monthly_distribution.parquet",
        "monthly_category_distribution": CACHE_DIR / "monthly_category_distribution.parquet",
        "missing_summary": CACHE_DIR / "missing_summary.parquet",
        "length_summary": CACHE_DIR / "length_summary.parquet",
        "length_histogram": CACHE_DIR / "length_histogram.parquet",
        "preview_sample": CACHE_DIR / "preview_sample.parquet",
    }

    missing_files = [
        str(path)
        for path in required_files.values()
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Không tìm thấy đầy đủ dashboard cache. "
            "Hãy chạy: python scripts/build_dashboard_cache.py\n\n"
            + "\n".join(missing_files)
        )

    with open(required_files["overview"], "r", encoding="utf-8") as f:
        overview = json.load(f)

    return {
        "overview": overview,
        "category_distribution": pd.read_parquet(required_files["category_distribution"]),
        "source_distribution": pd.read_parquet(required_files["source_distribution"]),
        "split_distribution": pd.read_parquet(required_files["split_distribution"]),
        "category_source_matrix": pd.read_parquet(required_files["category_source_matrix"]),
        "monthly_distribution": pd.read_parquet(required_files["monthly_distribution"]),
        "monthly_category_distribution": pd.read_parquet(required_files["monthly_category_distribution"]),
        "missing_summary": pd.read_parquet(required_files["missing_summary"]),
        "length_summary": pd.read_parquet(required_files["length_summary"]),
        "length_histogram": pd.read_parquet(required_files["length_histogram"]),
        "preview_sample": pd.read_parquet(required_files["preview_sample"]),
    }


@st.cache_data(show_spinner="Đang tải toàn bộ dữ liệu...")
def load_full_data():
    return load_news_data()


# =========================================================
# Insight generation
# =========================================================

def generate_auto_insights(
    overview,
    category_dist,
    source_dist,
    split_dist,
    monthly_dist,
    missing_summary,
    length_summary,
):
    insights = []

    if not category_dist.empty:
        top_cat = category_dist.iloc[0]
        bottom_cat = category_dist.iloc[-1]
        imbalance_ratio = category_dist["count"].max() / category_dist["count"].min()

        insights.append(
            (
                "🏷️ Chủ đề xuất hiện nhiều nhất",
                f"Chủ đề <b>{top_cat['category']}</b> có <b>{int(top_cat['count']):,}</b> bài, "
                f"chiếm <b>{top_cat['percent']}%</b> toàn bộ dữ liệu."
            )
        )

        insights.append(
            (
                "⚖️ Mức độ mất cân bằng nhãn",
                f"Imbalance ratio giữa lớp lớn nhất và nhỏ nhất là <b>{imbalance_ratio:.2f}x</b>. "
                f"Lớp nhỏ nhất là <b>{bottom_cat['category']}</b> với <b>{int(bottom_cat['count']):,}</b> bài."
            )
        )

    if not source_dist.empty:
        top_source = source_dist.iloc[0]
        insights.append(
            (
                "🌐 Nguồn báo đóng góp nhiều nhất",
                f"Nguồn <b>{top_source['source']}</b> có <b>{int(top_source['count']):,}</b> bài, "
                f"chiếm <b>{top_source['percent']}%</b> dữ liệu."
            )
        )

    if not split_dist.empty:
        split_text = ", ".join(
            f"{row['split']}: {int(row['count']):,}"
            for _, row in split_dist.iterrows()
        )
        insights.append(
            (
                "🧪 Tỉ lệ chia dữ liệu",
                f"Các tập dữ liệu hiện có: <b>{split_text}</b>."
            )
        )

    if not monthly_dist.empty:
        peak_month = monthly_dist.sort_values("count", ascending=False).iloc[0]
        insights.append(
            (
                "🕒 Tháng có nhiều bài nhất",
                f"Tháng <b>{peak_month['month_period']}</b> có số lượng bài cao nhất với "
                f"<b>{int(peak_month['count']):,}</b> bài."
            )
        )

    if not missing_summary.empty:
        missing_nonzero = missing_summary[missing_summary["missing_count"] > 0]
        if not missing_nonzero.empty:
            top_missing = missing_nonzero.iloc[0]
            insights.append(
                (
                    "🧩 Cột thiếu dữ liệu nhiều nhất",
                    f"Cột <b>{top_missing['column']}</b> có <b>{int(top_missing['missing_count']):,}</b> giá trị thiếu, "
                    f"tương ứng <b>{top_missing['missing_rate_percent']}%</b>."
                )
            )
        else:
            insights.append(
                (
                    "✅ Chất lượng dữ liệu sau xử lý",
                    "Không phát hiện missing values trong các cột được thống kê sau quá trình làm sạch."
                )
            )

    if not length_summary.empty:
        row = length_summary[length_summary["field"] == "full_text_wc"]
        if not row.empty:
            avg_len = row.iloc[0]["mean"]
            insights.append(
                (
                    "📏 Độ dài văn bản trung bình",
                    f"Độ dài trung bình của <b>full_text</b> là khoảng <b>{avg_len:.0f}</b> từ, "
                    "phù hợp cho các thực nghiệm phân loại văn bản tiếng Việt."
                )
            )

    return insights


# =========================================================
# Sidebar mode
# =========================================================

st.sidebar.header("Cấu hình dữ liệu")

mode = st.sidebar.radio(
    "Chế độ chạy",
    options=["Fast EDA Mode", "Full Data Mode"],
    index=0,
    help=(
        "Fast EDA Mode dùng cache thống kê đã tính sẵn từ toàn bộ dataset nên mở nhanh. "
        "Full Data Mode tải toàn bộ dữ liệu để lọc/search đầy đủ."
    ),
)


# =========================================================
# FAST EDA MODE
# =========================================================

if mode == "Fast EDA Mode":
    try:
        cache = load_dashboard_cache()
    except FileNotFoundError as e:
        st.error(str(e))
        st.info(
            "Trên máy người phát triển, hãy chạy `python scripts/build_dashboard_cache.py` "
            "rồi commit thư mục `data/dashboard_cache/` lên GitHub."
        )
        st.stop()

    st.markdown(
        """
        <div class="mode-note">
            <b>Fast EDA Mode</b>: dashboard đang sử dụng cache thống kê đã tính sẵn từ toàn bộ dataset.
            Vì vậy, các biểu đồ tổng quan vẫn phản ánh full dataset nhưng không cần tải toàn bộ dữ liệu khi mở app.
        </div>
        """,
        unsafe_allow_html=True,
    )

    overview = cache["overview"]
    category_dist = cache["category_distribution"]
    source_dist = cache["source_distribution"]
    split_dist = cache["split_distribution"]
    category_source_long = cache["category_source_matrix"]
    monthly_dist = cache["monthly_distribution"]
    monthly_category_dist = cache["monthly_category_distribution"]
    missing_summary = cache["missing_summary"]
    length_summary = cache["length_summary"]
    length_hist = cache["length_histogram"]
    preview_df = cache["preview_sample"]

    st.markdown('<div class="section-title">Tổng quan nhanh</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        render_metric_card(
            "Số bài",
            f"{overview.get('n_rows', 0):,}",
            "Tổng số bài sau xử lý",
            "🧾",
        )

    with col2:
        render_metric_card(
            "Số chủ đề",
            f"{overview.get('n_categories', 0):,}",
            "Nhãn category chính",
            "🏷️",
        )

    with col3:
        render_metric_card(
            "Số nguồn báo",
            f"{overview.get('n_sources', 0):,}",
            "Nguồn dữ liệu khác nhau",
            "🌐",
        )

    with col4:
        avg_wc = overview.get("avg_full_text_wc", None)
        render_metric_card(
            "Độ dài TB",
            f"{avg_wc:.0f} từ" if avg_wc is not None else "N/A",
            "Tính trên full_text",
            "📏",
        )

    with col5:
        min_date = str(overview.get("min_date", "N/A"))[:10]
        max_date = str(overview.get("max_date", "N/A"))[:10]
        render_metric_card(
            "Thời gian",
            f"{min_date} → {max_date}",
            "Khoảng thời gian xuất bản",
            "🕒",
        )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Tổng quan & Insight",
            "Chất lượng dữ liệu",
            "Phân phối",
            "Thời gian",
            "Độ dài văn bản",
            "Preview dữ liệu",
        ]
    )

    with tab1:
        st.subheader("Tổng quan dữ liệu")

        overview_df = pd.DataFrame(
            {
                "Chỉ số": [
                    "Số dòng",
                    "Số cột",
                    "Số chủ đề",
                    "Số nguồn báo",
                    "Ngày sớm nhất",
                    "Ngày muộn nhất",
                    "Độ dài full_text trung bình",
                    "Trung vị độ dài full_text",
                    "P99 độ dài full_text",
                    "Độ dài full_text lớn nhất",
                ],
                "Giá trị": [
                    f"{overview.get('n_rows', 0):,}",
                    f"{overview.get('n_columns', 0):,}",
                    overview.get("n_categories", "N/A"),
                    overview.get("n_sources", "N/A"),
                    overview.get("min_date", "N/A"),
                    overview.get("max_date", "N/A"),
                    round(overview.get("avg_full_text_wc", 0), 2),
                    round(overview.get("median_full_text_wc", 0), 2),
                    round(overview.get("p99_full_text_wc", 0), 2),
                    round(overview.get("max_full_text_wc", 0), 2),
                ],
            }
        )

        st.dataframe(overview_df, use_container_width=True)

        st.subheader("Insight tự động")

        insights = generate_auto_insights(
            overview=overview,
            category_dist=category_dist,
            source_dist=source_dist,
            split_dist=split_dist,
            monthly_dist=monthly_dist,
            missing_summary=missing_summary,
            length_summary=length_summary,
        )

        c1, c2 = st.columns(2)

        for idx, (title, body) in enumerate(insights):
            with c1 if idx % 2 == 0 else c2:
                render_insight(title, body)

    with tab2:
        st.subheader("Data Quality Panel")

        total_missing = missing_summary["missing_count"].sum() if not missing_summary.empty else 0
        total_cells = overview.get("n_rows", 0) * overview.get("n_columns", 1)

        if total_cells > 0:
            missing_rate = total_missing / total_cells
            quality_score = max(0, 100 - missing_rate * 100)
        else:
            quality_score = 0

        c1, c2, c3 = st.columns(3)

        c1.metric("Data Quality Score", f"{quality_score:.2f}/100")
        c2.metric("Tổng missing", f"{int(total_missing):,}")
        c3.metric("Số cột thống kê", f"{len(missing_summary):,}")

        st.subheader("Missing Values")

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
            st.success("Không có missing values trong các cột được thống kê.")

        st.dataframe(missing_summary, use_container_width=True)

    with tab3:
        st.subheader("Phân phối chủ đề")

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

        st.subheader("Phân phối nguồn báo")

        if not source_dist.empty:
            c1, c2 = st.columns([1.2, 1])

            with c1:
                fig = px.pie(
                    source_dist,
                    names="source",
                    values="count",
                    title="Tỉ lệ bài theo nguồn báo",
                )
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.dataframe(source_dist, use_container_width=True)

        st.subheader("Phân phối train/dev/test")

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

        if not category_source_long.empty:
            matrix = category_source_long.pivot_table(
                index="category",
                columns="source",
                values="count",
                fill_value=0,
            )

            fig = px.imshow(
                matrix,
                text_auto=True,
                aspect="auto",
                title="Số bài theo Category và Source",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Không có dữ liệu category-source để vẽ heatmap.")

        st.subheader("Category Focus Explorer")

        if not category_dist.empty:
            category_options = ["Tất cả"] + category_dist["category"].dropna().tolist()

            focus_category = st.selectbox(
                "Chọn một chủ đề để phân tích sâu",
                options=category_options,
            )

            if focus_category != "Tất cả":
                st.markdown(f"### Đang phân tích chủ đề: `{focus_category}`")

                focus_source = category_source_long[
                    category_source_long["category"] == focus_category
                ].sort_values("count", ascending=False)

                c1, c2 = st.columns(2)

                with c1:
                    fig = px.bar(
                        focus_source,
                        x="source",
                        y="count",
                        text="count",
                        title=f"Phân phối nguồn báo trong chủ đề {focus_category}",
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with c2:
                    focus_monthly = monthly_category_dist[
                        monthly_category_dist["category"] == focus_category
                    ]

                    if not focus_monthly.empty:
                        fig = px.line(
                            focus_monthly,
                            x="month_period",
                            y="count",
                            markers=True,
                            title=f"Xu hướng theo tháng của chủ đề {focus_category}",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Không có dữ liệu thời gian cho chủ đề này.")

        st.subheader("Source Comparison")

        source_list = source_dist["source"].dropna().tolist() if not source_dist.empty else []

        if len(source_list) >= 2:
            c1, c2 = st.columns(2)

            with c1:
                source_a = st.selectbox("Nguồn báo A", source_list, index=0)

            with c2:
                source_b = st.selectbox("Nguồn báo B", source_list, index=1)

            compare_df = category_source_long[
                category_source_long["source"].isin([source_a, source_b])
            ]

            if not compare_df.empty:
                fig = px.bar(
                    compare_df,
                    x="category",
                    y="count",
                    color="source",
                    barmode="group",
                    title=f"So sánh phân phối chủ đề: {source_a} vs {source_b}",
                )
                fig.update_layout(xaxis_tickangle=-35)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Cần ít nhất hai nguồn báo để so sánh.")

    with tab4:
        st.subheader("Số bài theo tháng")

        if not monthly_dist.empty:
            fig = px.line(
                monthly_dist,
                x="month_period",
                y="count",
                markers=True,
                title="Xu hướng số bài theo tháng",
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(monthly_dist, use_container_width=True)
        else:
            st.warning("Không có dữ liệu thời gian hợp lệ.")

        st.subheader("Xu hướng chủ đề theo tháng")

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
            st.warning("Không có dữ liệu thời gian theo category.")

    with tab5:
        st.subheader("Thống kê độ dài văn bản")

        st.dataframe(length_summary, use_container_width=True)

        if not length_hist.empty:
            st.caption(
                "Histogram dưới đây hiển thị phân phối độ dài `full_text` đến percentile 99%. "
                "Các bài rất dài được gom vào bucket outlier cuối cùng để biểu đồ dễ đọc hơn."
            )

            c1, c2, c3 = st.columns(3)

            row = length_summary[length_summary["field"] == "full_text_wc"]

            if not row.empty:
                mean_len = row.iloc[0]["mean"]
                median_len = row.iloc[0]["50%"]
                max_len = row.iloc[0]["max"]

                c1.metric("Độ dài trung bình", f"{mean_len:.0f} từ")
                c2.metric("Trung vị", f"{median_len:.0f} từ")
                c3.metric("Dài nhất", f"{max_len:.0f} từ")

            show_log_y = st.checkbox(
                "Hiển thị trục Y dạng log",
                value=False,
                key="fast_length_hist_log",
            )

            hist_plot = length_hist.copy()

            fig = px.bar(
                hist_plot,
                x="bin_center",
                y="count",
                title="Phân phối độ dài full_text",
                labels={
                    "bin_center": "Độ dài văn bản (số từ)",
                    "count": "Số bài",
                },
            )

            fig.update_traces(
                marker_line_width=0,
                customdata=hist_plot[["bin_left", "bin_right", "bin_label"]],
                hovertemplate=(
                    "Khoảng độ dài: %{customdata[2]} từ"
                    "<br>Số bài: %{y:,}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Độ dài văn bản (số từ)",
                yaxis_title="Số bài",
                xaxis=dict(
                    tickformat=",.0f",
                    showgrid=False,
                ),
                yaxis=dict(
                    type="log" if show_log_y else "linear"
                ),
            )

            st.plotly_chart(fig, use_container_width=True)

            outlier_df = hist_plot[hist_plot.get("is_outlier", False) == True]

            if not outlier_df.empty:
                outlier_count = int(outlier_df["count"].sum())
                outlier_label = outlier_df.iloc[0]["bin_label"]
                st.info(
                    f"Có {outlier_count:,} bài nằm trong nhóm outlier độ dài `{outlier_label}` từ."
                )

            with st.expander("Xem bảng histogram"):
                st.dataframe(
                    hist_plot[["bin_label", "count"]].rename(
                        columns={
                            "bin_label": "Khoảng độ dài",
                            "count": "Số bài",
                        }
                    ),
                    use_container_width=True,
                )
        else:
            st.warning("Không có dữ liệu histogram độ dài.")

    with tab6:
        st.subheader("Preview dữ liệu")

        st.caption(
            "Bảng này chỉ là preview đại diện. "
            "Các biểu đồ ở các tab trước vẫn được tính từ toàn bộ dataset."
        )

        keyword_preview = st.text_input("Tìm kiếm nhanh trong preview")

        display_df = preview_df.copy()

        if keyword_preview:
            keyword_lower = keyword_preview.lower().strip()

            search_cols = [
                col for col in ["title", "description", "content", "url", "author"]
                if col in display_df.columns
            ]

            if search_cols:
                mask = pd.Series(False, index=display_df.index)

                for col in search_cols:
                    mask = mask | (
                        display_df[col]
                        .fillna("")
                        .astype(str)
                        .str.lower()
                        .str.contains(keyword_lower, regex=False)
                    )

                display_df = display_df[mask]

        display_cols = [
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

        display_cols = [col for col in display_cols if col in display_df.columns]

        st.dataframe(
            display_df[display_cols].head(1000),
            use_container_width=True,
            height=550,
        )

    st.stop()


# =========================================================
# FULL DATA MODE
# =========================================================

st.warning(
    "Đang chạy Full Data Mode: dashboard sẽ tải và merge toàn bộ dữ liệu. "
    "Chế độ này có thể mất thời gian nhưng hỗ trợ lọc/search đầy đủ."
)

try:
    df = load_full_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.info(
        "Hãy chạy `python scripts/download_data.py` để tải full dataset từ Hugging Face, "
        "hoặc chuyển sang Fast EDA Mode nếu chỉ muốn xem thống kê nhanh."
    )
    st.stop()


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

keyword = st.sidebar.text_input("Tìm kiếm từ khóa trong full data")

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


st.markdown('<div class="section-title">Tổng quan dữ liệu sau lọc</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Số bài", f"{len(filtered_df):,}")
col2.metric("Số chủ đề", filtered_df["category"].nunique() if "category" in filtered_df.columns else 0)
col3.metric("Số nguồn", filtered_df["source"].nunique() if "source" in filtered_df.columns else 0)
col4.metric("Số split", filtered_df["split"].nunique() if "split" in filtered_df.columns else 0)

if "full_text_wc" in filtered_df.columns and len(filtered_df) > 0:
    col5.metric("Độ dài TB", f"{filtered_df['full_text_wc'].mean():.0f} từ")
else:
    col5.metric("Độ dài TB", "N/A")


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
    st.subheader("Tổng quan dữ liệu sau lọc")

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
        st.caption(
            "Biểu đồ dưới đây mặc định chỉ hiển thị tới percentile 99% để tránh outlier kéo giãn trục."
        )

        show_log_y_full = st.checkbox(
            "Hiển thị trục Y dạng log",
            value=False,
            key="full_length_hist_log",
        )

        length_data = filtered_df["full_text_wc"].dropna().astype(float)

        if not length_data.empty:
            upper_cap = length_data.quantile(0.99)
            plot_data = filtered_df[filtered_df["full_text_wc"] <= upper_cap].copy()

            fig = px.histogram(
                plot_data,
                x="full_text_wc",
                nbins=40,
                title="Phân phối độ dài full_text đến p99",
                labels={"full_text_wc": "Độ dài văn bản (số từ)"},
            )

            fig.update_layout(
                xaxis_title="Độ dài văn bản (số từ)",
                yaxis_title="Số bài",
                yaxis=dict(type="log" if show_log_y_full else "linear"),
            )

            st.plotly_chart(fig, use_container_width=True)

            outlier_count = int((length_data > upper_cap).sum())

            st.info(
                f"Ngưỡng hiển thị p99 ≈ {upper_cap:.0f} từ. "
                f"Số bài dài hơn ngưỡng này: {outlier_count:,}."
            )
        else:
            st.warning("Không có dữ liệu độ dài hợp lệ.")
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