# Hệ thống Sinh tồn nơi Hoang dã (WSS)

## Giới thiệu
Hệ thống Sinh tồn nơi Hoang dã (WSS) là một trò chơi mô phỏng trong đó người chơi cố gắng di chuyển từ phía tây sang phía đông của bản đồ. Trên đường đi, người chơi sẽ gặp các loại địa hình khác nhau, cùng với nhiều nguy hiểm và tài nguyên như thức ăn, nước và vàng.

## Cách chơi
- Người chơi bắt đầu ở phía tây của bản đồ và cần di chuyển về phía đông
- Mỗi loại địa hình có chi phí di chuyển khác nhau (sức lực, thức ăn, nước)
- Người chơi cần thu thập tài nguyên và quản lý chúng một cách hiệu quả
- Người chơi có thể giao dịch với thương nhân để đổi tài nguyên

## Các thành phần chính

### Bản đồ (Map)
- Lưới ô vuông với các loại địa hình khác nhau
- Mỗi ô có thể chứa vật phẩm hoặc thương nhân
- Kích thước bản đồ có thể tùy chỉnh

### Người chơi (Player)
- Có các chỉ số: sức lực, nước, thức ăn, vàng
- Có hai thành phần đặc biệt: Vision (Tầm nhìn) và Brain (Trí tuệ)

### Vision - Tầm nhìn
Có 4 loại tầm nhìn khác nhau:
1. **Focused (Tập trung)**: Chỉ nhìn thấy các ô ở phía đông
2. **Cautious (Thận trọng)**: Nhìn thấy các ô ở phía bắc, nam và đông
3. **Keen-Eyed (Mắt tinh)**: Nhìn thấy nhiều ô hơn, bao gồm cả ô đông thứ hai
4. **Far-Sight (Nhìn xa)**: Nhìn thấy hai ô theo mọi hướng

Mỗi loại tầm nhìn có các phương thức để tìm đường đi:
- `closest_food`: Tìm thức ăn gần nhất
- `closest_water`: Tìm nước gần nhất
- `closest_gold`: Tìm vàng gần nhất
- `closest_trader`: Tìm thương nhân gần nhất
- `second_closest_food`, `second_closest_water`, v.v.: Tìm nguồn tài nguyên gần thứ hai
- `easiest_path`: Tìm đường đi tiêu hao sức lực ít nhất

### Brain - Trí tuệ
Có 2 loại trí tuệ:
1. **SurvivalBrain**: Ưu tiên sinh tồn, tìm nước và thức ăn khi cần thiết
2. **ResourceBrain**: Tập trung thu thập tài nguyên trước khi di chuyển về phía đông

### Địa hình (Terrain)
Các loại địa hình khác nhau với chi phí di chuyển khác nhau:
- Đồng bằng (Plains): Chi phí thấp
- Rừng (Forest): Chi phí trung bình
- Đầm lầy (Swamp): Chi phí cao
- Núi (Mountain): Chi phí di chuyển cao, chi phí nước thấp

### Vật phẩm (Items)
- Thức ăn (Food): Tăng lượng thức ăn
- Nước (Water): Tăng lượng nước
- Vàng (Gold): Tăng lượng vàng
- Thương nhân (Trader): Cho phép giao dịch tài nguyên

## Cách chạy trò chơi
1. Chạy file `main.py` để khởi động trò chơi trong terminal
2. Chạy file `wss/ui.py` để khởi động trò chơi với giao diện đồ họa

## Điều khiển
- Sử dụng các phím mũi tên để di chuyển
- Nhấn `R` để nghỉ ngơi
- Nhấn `I` để xem thông tin đường đi

## Tùy chỉnh
Bạn có thể tùy chỉnh trò chơi bằng cách thay đổi các tham số trong file `wss/ui.py`:
- Thay đổi loại tầm nhìn: `vision_type = "cautious"` (có thể là "focused", "keen", "farsight")
- Thay đổi loại trí tuệ: `brain_type = "resource"` (có thể là "survival")
- Thay đổi kích thước bản đồ và độ khó
