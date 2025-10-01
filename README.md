# Google Search Playwright CLI

Ứng dụng dòng lệnh Python này sử dụng [Playwright](https://playwright.dev/python/) để tự động tìm kiếm Google, hỗ trợ chuyển trang tùy thuộc vào số lượng kết quả bạn muốn xem và hiển thị tiêu đề cùng mô tả cho mỗi kết quả.

## Yêu cầu

- Python 3.10 trở lên
- Playwright và các trình duyệt của nó (`playwright install`)

## Cài đặt

```bash
pip install .
playwright install
```

## Sử dụng

Chạy ứng dụng thông qua script đã cài đặt:

```bash
google-search-cli
```

Hoặc chạy trực tiếp module chính:

```bash
python -m main
```

Ứng dụng sẽ yêu cầu nhập từ khóa và số lượng kết quả muốn xem, sau đó tự động điều hướng qua các trang kết quả để thu thập dữ liệu.

## Ghi chú

- Việc tự động hóa Google có thể bị chặn nếu gửi quá nhiều yêu cầu trong thời gian ngắn.
- Bạn có thể chỉnh sửa logic trích xuất trong `src/google_search/searcher.py` để phù hợp với thay đổi giao diện của Google.

## Tiện ích bổ sung

Kho chứa vẫn bao gồm script `check_os.sh` giúp nhận diện hệ điều hành hiện tại.
