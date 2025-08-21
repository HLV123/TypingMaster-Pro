# TypingMaster Pro

Ứng dụng luyện tập tốc độ và độ chính xác đánh máy toàn diện được xây dựng bằng Python và Tkinter. Có tính năng thống kê thời gian thực, nhiều chế độ luyện tập và theo dõi tiến độ chi tiết.


![UI Screenshot](./bản%20GUI%20đẹp,%20tính%20năng%20phong%20phú/UI.png)

## Tính năng

### Chức năng cốt lõi
- **Test đánh máy thời gian thực**: Theo dõi WPM, độ chính xác và thời gian trực tiếp
- **Nhiều chế độ hiển thị**: 
  - Chế độ câu đầy đủ để hiển thị toàn bộ văn bản
  - Chế độ từng từ để luyện tập tập trung
- **Các mức độ khó**: Dễ (0-25 ký tự), Trung bình (26-60 ký tự), Khó (61+ ký tự)
- **Lọc nội dung**: Chỉ chữ cái hoặc có ký tự đặc biệt/số
- **Hiển thị tiến độ**: Thanh tiến độ thời gian thực và đếm ký tự

### Thống kê và phân tích
- Thống kê đánh máy toàn diện với lưu trữ JSON
- Lịch sử phiên và kỷ lục cá nhân
- Theo dõi hiệu suất hàng ngày
- Phân tích tiến độ theo thời gian
- Chức năng xuất/nhập để sao lưu dữ liệu

### Giao diện người dùng
- Giao diện hiện đại, sạch sẽ với bảng màu Nord
- Bố cục ba cột đáp ứng
- Khu vực nội dung có thể cuộn
- Làm nổi bật văn bản thời gian thực cho ký tự đúng/sai
- Phản hồi trực quan với chỉ báo tiến độ mã màu

## Cài đặt

### Yêu cầu
- Python 3.7+
- Tkinter (thường đi kèm với Python)
- Không cần thư viện bổ sung

### Thiết lập
```bash
python main.py
```

## Cách sử dụng

### Bắt đầu
1. **Nhập file văn bản**: Nhấp "Import File" để tải file .txt với các câu luyện tập
2. **Chọn chế độ**: Chọn độ khó, loại nội dung và chế độ hiển thị ưa thích
3. **Bắt đầu đánh máy**: Nhấp vào vùng nhập hoặc bắt đầu gõ để bắt đầu test
4. **Theo dõi tiến độ**: Giám sát thống kê thời gian thực ở panel bên trái

### Định dạng file
Tạo file văn bản với mỗi câu trên một dòng:
```
Đây là câu luyện tập đầu tiên.
Đây là một câu khác để gõ.
Đảm bảo mỗi dòng có ít nhất 10 ký tự.
```

### Chế độ luyện tập

#### Mức độ khó
- **Dễ**: Câu ngắn (0-25 ký tự) - lý tưởng cho người mới bắt đầu
- **Trung bình**: Câu trung bình (26-60 ký tự) - luyện tập cân bằng
- **Khó**: Câu dài (61+ ký tự) - thử thách nâng cao

#### Loại nội dung
- **Chỉ chữ cái**: Ký tự chữ cái cơ bản và dấu câu
- **Có ký tự đặc biệt**: Bao gồm số và ký hiệu đặc biệt (@, #, $, v.v.)

#### Chế độ hiển thị
- **Câu đầy đủ**: Hiển thị văn bản hoàn chỉnh để luyện tập toàn diện
- **Từng từ**: Hiển thị một từ tại một thời điểm để tập trung độ chính xác

## Cấu trúc file

```
typingmaster-pro/
├── main.py                    # Điểm vào ứng dụng
├── gui_manager.py             # Giao diện GUI chính và bố cục
├── calculator.py              # Engine tính toán metrics đánh máy
├── data_manager.py            # Xử lý và lọc dữ liệu văn bản
├── statistics_manager.py      # Theo dõi hiệu suất và phân tích
├── mode_selection_dialog.py   # Dialog cấu hình chế độ luyện tập
├── DATA.txt                   # Lưu trữ văn bản luyện tập mặc định
└── typing_stats.json          # Dữ liệu thống kê và tiến độ
```

## Các thành phần chính

### Module Calculator
- Tính toán WPM (Từ mỗi phút)
- Tính phần trăm độ chính xác
- Phân tích ký tự và phím bấm
- Phát hiện và phân loại lỗi
- Hệ thống đánh giá hiệu suất

### Data Manager
- Nhập văn bản từ file .txt
- Lọc nội dung theo độ khó và loại
- Chọn văn bản dựa trên preferences
- Hỗ trợ nhiều encoding (UTF-8, Latin-1, CP1252)

### Statistics Manager
- Lưu trữ dữ liệu dựa trên JSON
- Theo dõi phiên và lịch sử
- Kỷ lục cá nhân
- Phân tích tiến độ hàng ngày/tuần
- Khả năng xuất/nhập dữ liệu

### GUI Manager
- Bố cục ba cột đáp ứng hiện đại
- Hiển thị thống kê thời gian thực
- Làm nổi bật văn bản tương tác
- Hiển thị tiến độ trực quan
- Tích hợp chọn chế độ

## Cấu hình

### Cài đặt mặc định
- File thống kê: `typing_stats.json`
- File văn bản luyện tập: `DATA.txt`
- Tự động lưu được bật cho tất cả phiên
- Cập nhật tính toán thời gian thực

### Tùy chỉnh
- Thay đổi bảng màu trong `gui_manager.py` (dictionary `self.colors`)
- Điều chỉnh ngưỡng độ khó trong `data_manager.py`
- Cấu hình đánh giá hiệu suất trong `calculator.py`


## Lưu trữ dữ liệu

### Định dạng thống kê
```json
{
  "results": [
    {
      "wpm": 45.2,
      "accuracy": 96.8,
      "time": 120.5,
      "text_length": 180,
      "user_length": 175,
      "timestamp": 1640995200.0,
      "date": "2025-01-01T10:00:00"
    }
  ],
  "session_data": {},
  "preferences": {}
}
```

## Lời cảm ơn

- Lấy cảm hứng từ các trình dạy đánh máy truyền thống với cải tiến hiện đại
- Được thiết kế cho cả người mới bắt đầu và người đánh máy nâng cao

