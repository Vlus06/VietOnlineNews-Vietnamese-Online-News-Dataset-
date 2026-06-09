# VietOnlineNews: Vietnamese Online News Dataset

## Project Information

| Item | Information |
|---|---|
| Course | DS108 - Tiền xử lý và xây dựng bộ dữ liệu |
| Project name | VietOnlineNews |
| Task | Vietnamese Online News Dataset for Topic Classification |
| Students | Bùi Thị Thanh Tuyền, Nguyễn Thanh Tuyền |
| Supervisors | TS. Nguyễn Gia Tuấn Anh, CN. Trần Quốc Khánh |
| GitHub Repository | https://github.com/Vlus06/VietOnlineNews-Vietnamese-Online-News-Dataset- |
| Hugging Face Dataset | https://huggingface.co/datasets/VLUS06/VietOnlineNews |

---

## 1. Overview

**VietOnlineNews** là một hệ thống xây dựng, tiền xử lý, phân tích và trực quan hóa bộ dữ liệu tin tức trực tuyến tiếng Việt đa nguồn. Dự án được thực hiện trong khuôn khổ học phần **DS108 - Tiền xử lý và xây dựng bộ dữ liệu**, với mục tiêu chuyển đổi dữ liệu báo điện tử thô thành một bộ dữ liệu có cấu trúc, có khả năng tái lập và có thể sử dụng cho các bài toán xử lý ngôn ngữ tự nhiên tiếng Việt.

Dự án tập trung vào bài toán **phân loại chủ đề bài báo tiếng Việt**. Dữ liệu được thu thập từ nhiều nguồn báo điện tử, sau đó được chuẩn hóa, làm sạch, chia thành các tập `train`, `dev`, `test` và bổ sung metadata để hỗ trợ truy vết, phân tích và mở rộng cho các bài toán khác.

Dự án không chỉ dừng lại ở notebook phân tích dữ liệu, mà được nâng cấp thành một hệ thống có thể chạy lại, bao gồm:

- Bộ dữ liệu tin tức tiếng Việt đa nguồn.
- Notebook thu thập, làm sạch và phân tích dữ liệu.
- Pipeline xử lý dữ liệu và tạo cache thống kê.
- Dashboard tương tác bằng Streamlit.
- Docker để đóng gói môi trường chạy.
- Lưu trữ dữ liệu lớn trên Hugging Face Datasets.

---

## 2. Data Sources

Dữ liệu được thu thập từ ba nguồn báo điện tử tiếng Việt:

- **Tuổi Trẻ**
- **Thanh Niên**
- **VietnamNet**

Các nguồn này được lựa chọn vì có mức độ phổ biến cao, chuyên mục rõ ràng và cung cấp dữ liệu bài viết phù hợp trong phạm vi khảo sát.

---

## 3. Key Features

Dự án bao gồm các thành phần chính:

| Component | Description |
|---|---|
| Data Collection | Notebook thu thập dữ liệu riêng cho từng nguồn báo |
| Data Cleaning | Xử lý missing values, duplicate records, label conflicts và chuẩn hóa schema |
| EDA | Phân tích phân phối nhãn, nguồn báo, thời gian, độ dài văn bản và chất lượng dữ liệu |
| Streamlit Dashboard | Giao diện tương tác để khám phá dữ liệu và biểu đồ |
| Fast EDA Mode | Dùng cache thống kê được tính sẵn từ toàn bộ dataset để dashboard mở nhanh |
| Full Data Mode | Tải và merge toàn bộ dữ liệu để lọc/search đầy đủ khi cần |
| Docker Deployment | Đóng gói môi trường chạy để tăng khả năng tái lập |
| Hugging Face Hosting | Lưu trữ full dataset bên ngoài GitHub để repo gọn nhẹ |

---

## 4. Repository Structure

```text
VietOnlineNews/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── dashboard_cache/
│   │   ├── overview.json
│   │   ├── category_distribution.parquet
│   │   ├── source_distribution.parquet
│   │   ├── split_distribution.parquet
│   │   ├── category_source_matrix.parquet
│   │   ├── monthly_distribution.parquet
│   │   ├── monthly_category_distribution.parquet
│   │   ├── missing_summary.parquet
│   │   ├── length_summary.parquet
│   │   ├── length_histogram.parquet
│   │   └── preview_sample.parquet
│   │
│   ├── processed/
│   │   └── .gitkeep
│   │
│   └── rawdata/
│       └── .gitkeep
│
├── notebook/
│   ├── 01_data_collection/
│   │   ├── thanhnien.ipynb
│   │   ├── tuoitre.ipynb
│   │   └── vietnamnet.ipynb
│   │
│   ├── 02_data_cleaning_and_imputation.ipynb
│   └── 03_exploratory_data_analysis.ipynb
│
├── scripts/
│   ├── build_dashboard_cache.py
│   ├── convert_to_parquet.py
│   └── download_data.py
│
├── src/
│   ├── __init__.py
│   ├── paths.py
│   ├── data_loader.py
│   └── eda_utils.py
│
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Folder Description

| Folder/File | Description |
|---|---|
| `app/` | Chứa mã nguồn Streamlit Dashboard |
| `src/` | Chứa các module lõi dùng cho dashboard và xử lý dữ liệu |
| `scripts/` | Chứa các script vận hành như tải dữ liệu, chuyển Parquet, tạo dashboard cache |
| `data/rawdata/` | Thư mục dữ liệu thô ở local, không commit dữ liệu thật lên GitHub |
| `data/processed/` | Thư mục dữ liệu đã xử lý ở local, không commit full data lên GitHub |
| `data/dashboard_cache/` | Chứa thống kê EDA đã tính sẵn từ full dataset để dashboard mở nhanh |
| `notebook/` | Chứa notebook thu thập, làm sạch và phân tích dữ liệu |
| `Dockerfile` | Cấu hình Docker image |
| `docker-compose.yml` | Cấu hình chạy dashboard bằng Docker Compose |
| `requirements.txt` | Danh sách thư viện Python cần thiết |

---

## 5. Dataset

Do kích thước dữ liệu lớn, full dataset không được lưu trực tiếp trong GitHub repository. Dữ liệu được lưu trữ trên Hugging Face Datasets:

```text
https://huggingface.co/datasets/VLUS06/VietOnlineNews
```

Cấu trúc dữ liệu trên Hugging Face được tổ chức như sau:

```text
VietOnlineNews/
├── processed/
│   ├── train.csv
│   ├── dev.csv
│   ├── test.csv
│   └── news_metadata.csv
│
└── raw/
    ├── merged_data_thanhnien.csv
    ├── merged_data_tuoitre.csv
    └── merged_data_vietnamnet.csv
```

### Dataset Files

| File | Description |
|---|---|
| `processed/train.csv` | Tập huấn luyện, gồm nội dung bài báo và nhãn chủ đề |
| `processed/dev.csv` | Tập phát triển/validation |
| `processed/test.csv` | Tập kiểm thử |
| `processed/news_metadata.csv` | Metadata của bài báo, dùng để phân tích và truy vết |
| `raw/merged_data_thanhnien.csv` | Dữ liệu thô đã gộp từ Thanh Niên |
| `raw/merged_data_tuoitre.csv` | Dữ liệu thô đã gộp từ Tuổi Trẻ |
| `raw/merged_data_vietnamnet.csv` | Dữ liệu thô đã gộp từ VietnamNet |

---

## 6. Data Schema

### 6.1 Text Splits: `train.csv`, `dev.csv`, `test.csv`

| Column | Type | Description |
|---|---|---|
| `id` | string/int | Mã định danh duy nhất của bài báo |
| `title` | string | Tiêu đề bài báo |
| `description` | string | Mô tả ngắn hoặc sapo của bài báo |
| `content` | string | Nội dung chính của bài báo |
| `category` | string | Nhãn chủ đề chính của bài báo |

### 6.2 Metadata File: `news_metadata.csv`

| Column | Type | Description |
|---|---|---|
| `id` | string/int | Mã định danh duy nhất của bài báo |
| `category` | string | Nhãn chủ đề chính |
| `source` | string | Nguồn báo |
| `url` | string | Đường dẫn gốc của bài báo |
| `author` | string | Tác giả bài báo nếu có |
| `sub_topic` | string | Chủ đề con theo từng nguồn báo |
| `tag` | string | Tag hoặc từ khóa liên quan |
| `public_date` | datetime | Ngày xuất bản bài báo |

Trong dashboard, các file `train/dev/test` có thể được merge với `news_metadata` thông qua cột `id`.

---

## 7. Dashboard Modes

Streamlit Dashboard hỗ trợ hai chế độ chạy.

### 7.1 Fast EDA Mode

Đây là chế độ mặc định.

Fast EDA Mode sử dụng các file trong:

```text
data/dashboard_cache/
```

Các file này là thống kê EDA được tính sẵn từ toàn bộ dataset. Nhờ đó dashboard mở nhanh, không cần tải hoặc merge full dataset khi khởi động.
### 7.2 Full Data Mode

Full Data Mode tải và merge toàn bộ dữ liệu từ `data/processed/`. Chế độ này hỗ trợ lọc/search đầy đủ trên full dataset nhưng có thể mất thời gian hơn khi mở.

Để dùng Full Data Mode, cần tải full dataset từ Hugging Face bằng:

```bash
python scripts/download_data.py
```

Nếu dữ liệu tải về ở dạng CSV, có thể chuyển sang Parquet để tăng tốc độ đọc:

```bash
python scripts/convert_to_parquet.py
```

---

## 8. Quick Start

### 8.1 Clone repository

```bash
git clone https://github.com/Vlus06/VietOnlineNews-Vietnamese-Online-News-Dataset-.git
cd VietOnlineNews-Vietnamese-Online-News-Dataset-
```

### 8.2 Create virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 8.3 Install dependencies

```bash
pip install -r requirements.txt
```

### 8.4 Run dashboard

```bash
python -m streamlit run app/streamlit_app.py
```

Open the dashboard at:

```text
http://localhost:8501
```

By default, the dashboard runs in **Fast EDA Mode**, so it can start quickly without downloading the full dataset.

---

## 9. Run with Docker

Dự án có thể chạy bằng Docker Compose để đảm bảo khả năng tái lập môi trường.

### 9.1 Build and run

```bash
docker compose up --build
```

Sau khi container chạy thành công, mở:

```text
http://localhost:8501
```

Lưu ý: Streamlit trong container có thể in log dạng:

```text
http://0.0.0.0:8501
```

Tuy nhiên, trên máy host, hãy mở bằng:

```text
http://localhost:8501
```

### 9.2 Stop container

```bash
docker compose down
```

Docker mặc định chạy Fast EDA Mode bằng dashboard cache, nên không cần tải full dataset khi khởi động.

---

## 10. Download Full Dataset

Dữ liệu đầy đủ được tải từ Hugging Face bằng script:

```bash
python scripts/download_data.py
```

Sau khi tải xong, dữ liệu sẽ nằm trong:

```text
data/processed/
```

Các file cần có:

```text
data/processed/train.csv
data/processed/dev.csv
data/processed/test.csv
data/processed/news_metadata.csv
```

Nếu muốn dùng Parquet cho tốc độ đọc tốt hơn:

```bash
python scripts/convert_to_parquet.py
```

---

## 11. Rebuild Dashboard Cache

Nếu full dataset thay đổi, cần tạo lại dashboard cache bằng lệnh:

```bash
python scripts/build_dashboard_cache.py
```

Script này đọc dữ liệu trong `data/processed/`, tính toán các thống kê EDA chính và lưu vào:

```text
data/dashboard_cache/
```

Các file cache này có thể được commit lên GitHub vì dung lượng nhỏ và giúp dashboard mở nhanh.

---

## 12. Data Processing Workflow

Quy trình xử lý dữ liệu gồm các bước chính:

1. Thu thập dữ liệu từ nhiều nguồn báo điện tử tiếng Việt.
2. Chuẩn hóa schema giữa các nguồn.
3. Chuẩn hóa nhãn chủ đề.
4. Xử lý missing values trong các trường văn bản quan trọng.
5. Phát hiện và loại bỏ duplicate records.
6. Kiểm tra và xử lý label conflicts.
7. Tạo metadata phục vụ truy vết.
8. Chia dữ liệu thành `train`, `dev`, `test`.
9. Chuyển dữ liệu sang định dạng Parquet để tăng tốc độ đọc khi chạy local.
10. Tạo dashboard cache từ full dataset.
11. Trực quan hóa dữ liệu bằng Streamlit Dashboard.

---

## 13. Reproducibility

Dự án được thiết kế để đảm bảo khả năng tái lập:

- Không chỉnh sửa dữ liệu thô bằng tay hoặc bằng Excel.
- Tất cả biến đổi dữ liệu được thực hiện thông qua code.
- Full dataset được lưu trên Hugging Face thay vì commit trực tiếp lên GitHub.
- Dashboard cache được tính từ full dataset để hỗ trợ demo nhanh.
- Môi trường chạy được khai báo trong `requirements.txt`.
- Dashboard có thể chạy local hoặc thông qua Docker.
- Các thư mục `data/rawdata/`, `data/processed/` và `data/dashboard_cache/` được tách riêng rõ ràng.

---

## 14. Notes on Data Storage

GitHub repository này không chứa full data như `.csv` hoặc full `.parquet` trong `data/processed/`.

Các file dữ liệu lớn được loại khỏi Git bằng `.gitignore`, ví dụ:

```text
data/rawdata/*
data/processed/*
*.csv
*.parquet
*.gz
*.zip
```

Ngoại lệ là thư mục:

```text
data/dashboard_cache/
```

Thư mục này được commit lên GitHub vì chỉ chứa các thống kê tổng hợp nhỏ, giúp dashboard mở nhanh mà không cần tải toàn bộ dữ liệu.

---

## 15. Ethical and Legal Considerations

Bộ dữ liệu được xây dựng cho mục đích học tập và nghiên cứu. Nội dung bài báo gốc thuộc quyền sở hữu của các đơn vị xuất bản tương ứng. Người dùng cần tuân thủ điều khoản sử dụng, chính sách bản quyền và quy định trích dẫn của các nguồn báo gốc.

Dữ liệu không nên được sử dụng cho các mục đích:

- Phân phối thương mại lại nội dung báo chí gốc.
- Mạo danh hoặc xuyên tạc nguồn xuất bản.
- Tạo hoặc phát tán thông tin sai lệch.
- Sử dụng ngoài phạm vi học tập và nghiên cứu nếu chưa có quyền phù hợp.

---

## 16. Limitations

Bộ dữ liệu vẫn có một số giới hạn:

- Phân phối dữ liệu phụ thuộc vào các nguồn báo được chọn.
- `sub_topic` và `tag` có thể không thống nhất hoàn toàn giữa các nguồn.
- Một số metadata như `author`, `tag`, `sub_topic` có thể bị thiếu.
- Nhãn `category` có thể tồn tại các trường hợp biên khó phân loại tuyệt đối.
- Dữ liệu phản ánh giai đoạn thu thập cụ thể, không đại diện cho toàn bộ báo chí tiếng Việt.
- Fast EDA Mode dùng thống kê tổng hợp, nên không thay thế hoàn toàn Full Data Mode cho các thao tác search sâu trên toàn bộ văn bản.

---

## 17. Citation

If you use this dataset or codebase, please cite:

```bibtex
@misc{vietonlinenews2026,
  title        = {VietOnlineNews: A Vietnamese Online News Dataset for Topic Classification},
  author       = {Bùi Thị Thanh Tuyền and Nguyễn Thanh Tuyền},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/VLUS06/VietOnlineNews}}
}
```

---

## 18. License

This project is released for educational and research purposes.

The dataset follows a custom `educational-research-use-only` usage policy. Original news articles and related content belong to their respective publishers.

---

## 19. Contact

For questions, feedback, or discussions, please open an issue on the GitHub repository or use the discussion section on the Hugging Face dataset page.