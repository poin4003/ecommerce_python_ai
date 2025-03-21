# Ứng Dụng Web Ecommerce Đơn Giản

## Mô tả
Đây là một ứng dụng web ecommerce đơn giản, cho phép người dùng:
- Thêm sản phẩm mới (tên, mô tả, hình ảnh).
- Đánh giá sản phẩm (tích cực hoặc tiêu cực).
- Xem gợi ý sản phẩm dựa trên đánh giá tích cực và danh mục (category) tương tự.

Ứng dụng sử dụng:
- **Flask** (Python) để xây dựng backend.
- **SQLite** để lưu trữ dữ liệu.
- **TensorFlow** để phân loại hình ảnh sản phẩm.
- **Hugging Face API** để phân tích cảm xúc của đánh giá.
- **Docker** để đóng gói và chạy ứng dụng.

## Thành phần chính
- `app.py`: File chính chạy ứng dụng Flask.
- `models.py`: Định nghĩa mô hình cơ sở dữ liệu (sản phẩm).
- `templates/`: Chứa các file HTML (`all_products.html`, `recommendations.html`) để hiển thị giao diện.
- `static/uploads/`: Thư mục lưu hình ảnh sản phẩm.
- `requirements.txt`: Danh sách các thư viện Python cần thiết.
- `Dockerfile`: File để build container Docker.
- `.env`: File chứa các biến môi trường (token Hugging Face, cấu hình Flask).

## Hướng dẫn clone và chạy

### 1. Clone dự án
Clone mã nguồn về máy:
```bash
git clone <đường-dẫn-repository>
cd ecommerce_project