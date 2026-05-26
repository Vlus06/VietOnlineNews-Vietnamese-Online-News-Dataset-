## Project Information

| Item | Information |
|---|---|
| Course | DS108 - Tiền xử lý và xây dựng bộ dữ liệu |
| Project name | VietOnlineNews |
| Task | Vietnamese Online News Dataset  |
| Students | Bùi Thị Thanh Tuyền, Nguyễn Thanh Tuyền |
| Supervisors | CN. Trần Quốc Khánh, TS. Nguyễn Gia Tuấn Anh |

---

# VietOnlineNews: Vietnamese Online News Dataset 

VietOnlineNews là một hệ thống xây dựng, tiền xử lý, phân tích và trực quan hóa bộ dữ liệu tin tức tiếng Việt đa nguồn. Dự án được phát triển cho học phần **DS108 - Tiền xử lý và xây dựng bộ dữ liệu**, với mục tiêu chuyển đổi dữ liệu báo điện tử thô thành một bộ dữ liệu có cấu trúc, có khả năng tái lập và có thể sử dụng cho các bài toán xử lý ngôn ngữ tự nhiên tiếng Việt.

Dự án không chỉ dừng lại ở notebook phân tích dữ liệu, mà còn được nâng cấp thành một hệ thống hoàn chỉnh gồm:

- Bộ dữ liệu tin tức tiếng Việt đa nguồn.
- Pipeline xử lý và tổ chức dữ liệu.
- Dashboard tương tác bằng Streamlit.
- Đóng gói môi trường chạy bằng Docker.
- Lưu trữ dữ liệu lớn trên Hugging Face Datasets.
---

## 1. Project Overview

Mục tiêu chính của dự án là xây dựng bộ dữ liệu tin tức tiếng Việt phục vụ bài toán **phân loại chủ đề bài báo**. Dữ liệu được thu thập từ nhiều nguồn báo điện tử tiếng Việt, sau đó được chuẩn hóa, làm sạch, tách thành các tập `train`, `dev`, `test` và bổ sung metadata để hỗ trợ truy vết, phân tích và mở rộng cho các bài toán khác.

Các nguồn dữ liệu chính bao gồm:

- Tuổi Trẻ
- Thanh Niên
- VietnamNet

Bộ dữ liệu sau xử lý được tổ chức thành hai nhóm chính:

1. **Text data**: gồm `id`, `title`, `description`, `content`, `category`.
2. **Metadata**: gồm `id`, `category`, `source`, `url`, `author`, `sub_topic`, `tag`, `public_date`.

---

## 2. Key Features

Dự án bao gồm các thành phần chính:

- **Data Cleaning Pipeline**: xử lý missing values, duplicate records, label conflicts và chuẩn hóa schema.
- **Exploratory Data Analysis**: phân tích phân phối nhãn, nguồn báo, thời gian, độ dài văn bản và chất lượng dữ liệu.
- **Interactive Dashboard**: giao diện Streamlit cho phép lọc dữ liệu theo nguồn báo, chủ đề, split, thời gian và từ khóa.
- **Hugging Face Dataset Hosting**: dữ liệu lớn được lưu trữ bên ngoài GitHub để đảm bảo repo gọn nhẹ.
- **Dockerized Deployment**: đóng gói hệ thống để người dùng khác có thể chạy lại dễ dàng.

---

## 3. Repository Structure

```text
VietOnlineNews/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
│
├── notebooks/
│   ├── 02_data_cleaning_and_imputation.ipynb
│   └── 03_exploratory_data_analysis.ipynb
│
├── scripts/
│   ├── download_data.py
│   └── convert_to_parquet.py
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
├── DATA_DICTIONARY.md
├── LICENSE
└── README.md
```

### Folder Description

| Folder/File | Description |
|---|---|
| `app/` | Chứa mã nguồn giao diện Streamlit Dashboard |
| `src/` | Chứa các module lõi được dashboard sử dụng |
| `scripts/` | Chứa các script chạy độc lập như tải dữ liệu hoặc chuyển đổi định dạng |
| `data/raw/` | Thư mục dữ liệu thô, không commit dữ liệu thật lên GitHub |
| `data/processed/` | Thư mục dữ liệu đã xử lý, không commit dữ liệu thật lên GitHub |
| `notebooks/` | Chứa notebook cleaning và EDA |
| `Dockerfile` | Cấu hình Docker image |
| `docker-compose.yml` | Cấu hình chạy hệ thống bằng Docker Compose |
| `requirements.txt` | Danh sách thư viện Python cần thiết |
| `DATA_DICTIONARY.md` | Mô tả chi tiết các file dữ liệu và ý nghĩa từng cột |

---

## 4. Dataset

Do kích thước dữ liệu lớn, các file dữ liệu không được lưu trực tiếp trong GitHub repository. Toàn bộ dataset được lưu trữ trên Hugging Face Datasets:

```text
https://huggingface.co/datasets/VLUS06/VietOnlineNews
```

Các file dữ liệu chính gồm:

| File | Description |
|---|---|
| `train.parquet` | Tập huấn luyện, gồm nội dung bài báo và nhãn chủ đề |
| `dev.parquet` | Tập phát triển/validation |
| `test.parquet` | Tập kiểm thử |
| `news_metadata.parquet` | Metadata của bài báo, dùng để phân tích và truy vết |

---

## 5. Data Schema

### 5.1 Text Splits: `train.parquet`, `dev.parquet`, `test.parquet`

| Column | Type | Description |
|---|---|---|
| `id` | string/int | Mã định danh duy nhất của bài báo |
| `title` | string | Tiêu đề bài báo |
| `description` | string | Mô tả ngắn hoặc sapo của bài báo |
| `content` | string | Nội dung chính của bài báo |
| `category` | string | Nhãn chủ đề chính của bài báo |

### 5.2 Metadata File: `news_metadata.parquet`

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

Trong dashboard, các file `train/dev/test` sẽ được merge với `news_metadata` thông qua cột `id`.

---

## 6. Installation

### 6.1 Clone Repository

```bash
git clone https://github.com/<your-username>/VietOnlineNews.git
cd VietOnlineNews
```

### 6.2 Create Virtual Environment

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
.venv\Scripts\activate
```

Kích hoạt môi trường ảo trên macOS/Linux:

```bash
source .venv/bin/activate
```

### 6.3 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 7. Download Dataset

Dữ liệu được tải từ Hugging Face bằng script:

```bash
python scripts/download_data.py
```

Sau khi tải xong, dữ liệu sẽ nằm trong:

```text
data/processed/
```

Các file cần có sau khi tải:

```text
data/processed/train.parquet
data/processed/dev.parquet
data/processed/test.parquet
data/processed/news_metadata.parquet
```

---

## 8. Run Streamlit Dashboard

Sau khi cài thư viện và tải dữ liệu, chạy dashboard bằng lệnh:

```bash
python -m streamlit run app/streamlit_app.py
```

Sau đó mở trình duyệt tại:

```text
http://localhost:8501
```

Dashboard hỗ trợ:

- Lọc dữ liệu theo nguồn báo.
- Lọc dữ liệu theo chủ đề.
- Lọc theo split `train/dev/test`.
- Lọc theo khoảng thời gian.
- Tìm kiếm từ khóa trong tiêu đề, mô tả và nội dung.
- Quan sát phân phối nhãn.
- Quan sát phân phối nguồn báo.
- Phân tích xu hướng theo thời gian.
- Phân tích độ dài văn bản.
- Tải dữ liệu sau khi lọc.

---

## 9. Run with Docker

Dự án có thể chạy bằng Docker Compose để đảm bảo khả năng tái lập môi trường.

### 9.1 Build and Run

```bash
docker compose up --build
```

Sau khi container chạy thành công, mở:

```text
http://localhost:8501
```

### 9.2 Stop Container

```bash
docker compose down
```

Docker sẽ tự động:

1. Cài đặt môi trường Python.
2. Cài các thư viện trong `requirements.txt`.
3. Tải dữ liệu từ Hugging Face nếu chưa có trong `data/processed/`.
4. Khởi động Streamlit Dashboard.

---

## 10. Data Processing Workflow

Quy trình xử lý dữ liệu gồm các bước chính:

1. Thu thập dữ liệu từ nhiều nguồn báo điện tử tiếng Việt.
2. Chuẩn hóa schema giữa các nguồn.
3. Chuẩn hóa nhãn chủ đề.
4. Xử lý missing values trong các trường văn bản quan trọng.
5. Phát hiện và loại bỏ duplicate records.
6. Kiểm tra và xử lý label conflicts.
7. Tạo metadata phục vụ truy vết.
8. Chia dữ liệu thành `train`, `dev`, `test`.
9. Chuyển dữ liệu sang định dạng Parquet để giảm dung lượng và tăng tốc độ đọc.
10. Trực quan hóa dữ liệu bằng Streamlit Dashboard.

---

## 11. Reproducibility

Dự án được thiết kế để đảm bảo khả năng tái lập:

- Không chỉnh sửa dữ liệu thô bằng tay hoặc bằng Excel.
- Tất cả biến đổi dữ liệu được thực hiện thông qua code.
- Dữ liệu lớn được lưu trên Hugging Face thay vì commit trực tiếp lên GitHub.
- Môi trường chạy được khai báo trong `requirements.txt`.
- Dashboard có thể chạy local hoặc thông qua Docker.
- Các thư mục `data/rawdata/` và `data/processed/` được tách riêng rõ ràng.

---

## 12. Notes on Data Storage

GitHub repository này không chứa các file dữ liệu lớn như `.csv` hoặc `.parquet`.

Các file này được loại khỏi Git bằng `.gitignore`:

```text
data/raw/*
data/processed/*
*.csv
*.parquet
*.gz
*.zip
```

Người dùng cần tải dữ liệu bằng:

```bash
python scripts/download_data.py
```

---

## 13. Ethical and Legal Considerations

Bộ dữ liệu được xây dựng cho mục đích học tập và nghiên cứu. Nội dung bài báo gốc thuộc quyền sở hữu của các đơn vị xuất bản tương ứng. Người dùng cần tuân thủ điều khoản sử dụng, chính sách bản quyền và quy định trích dẫn của các nguồn báo gốc.

Dữ liệu không nên được sử dụng cho các mục đích:

- Phân phối thương mại lại nội dung báo chí gốc.
- Mạo danh hoặc xuyên tạc nguồn xuất bản.
- Tạo hoặc phát tán thông tin sai lệch.
- Sử dụng ngoài phạm vi học tập và nghiên cứu nếu chưa có quyền phù hợp.

---

## 14. Limitations

Bộ dữ liệu vẫn có một số giới hạn:

- Phân phối dữ liệu phụ thuộc vào các nguồn báo được chọn.
- `sub_topic` và `tag` có thể không thống nhất hoàn toàn giữa các nguồn.
- Một số metadata như `author`, `tag`, `sub_topic` có thể bị thiếu.
- Nhãn `category` có thể tồn tại các trường hợp biên khó phân loại tuyệt đối.
- Dữ liệu phản ánh giai đoạn thu thập cụ thể, không đại diện cho toàn bộ báo chí tiếng Việt.

---

## 15. Related Documents

- `DATA_DICTIONARY.md`: Mô tả chi tiết các cột dữ liệu.
- `notebooks/02_data_cleaning_and_imputation.ipynb`: Quy trình làm sạch và xử lý dữ liệu.
- `notebooks/03_exploratory_data_analysis.ipynb`: Phân tích khám phá dữ liệu.
- Hugging Face Dataset: `VLUS06/VietOnlineNews`.

---

## 16. Citation

If you use this dataset or codebase, please cite:

```bibtex
@misc{vietonlinenews2026,
  title        = {VietOnlineNews: A Vietnamese Online News Dataset for Topic Classification},
  author       = {VLUS06},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/VLUS06/VietOnlineNews}}
}
```

---

## 17. License

This project is released for educational and research purposes.

The dataset follows a custom `educational-research-use-only` license. Original news articles and related content belong to their respective publishers.

---

## 18. Contact

For questions, feedback, or discussions, please open an issue on this GitHub repository or use the discussion section on the Hugging Face dataset page.