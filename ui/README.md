# 🌿 Plant Analysis AI - Chatbot UI

Giao diện chatbot Vue.js cho hệ thống phân tích cây trồng bằng AI.

## ✨ Tính năng

- 💬 **Chatbot thông minh**: Giao tiếp bằng tiếng Việt tự nhiên
- 📸 **Upload và phân tích hình ảnh**: Kéo thả hoặc chọn file
- 🔍 **Nhận dạng cây trồng**: Xác định loại cây từ hình ảnh
- 🩺 **Chẩn đoán bệnh**: Phát hiện và phân tích bệnh trên cây
- 📈 **Đánh giá sinh trưởng**: Phân tích tình trạng phát triển
- 💡 **Khuyến nghị chăm sóc**: Tư vấn cách chăm sóc tối ưu
- 📱 **Responsive design**: Tương thích mobile và desktop
- ⚡ **Real-time**: Hiển thị trạng thái phân tích theo thời gian thực

## 🚀 Cách sử dụng

### Phương pháp 1: File HTML đơn giản (Khuyến nghị)
1. Mở file `chatbot.html` trong trình duyệt
2. Đảm bảo FastAPI server đang chạy trên port 8000
3. Bắt đầu chat với AI

### Phương pháp 2: Vue.js Development Server
1. Cài đặt dependencies:
```bash
cd ui
npm install
```

2. Chạy development server:
```bash
npm run dev
```

3. Mở trình duyệt tại `http://localhost:3000`

### Phương pháp 3: Build cho production
1. Build project:
```bash
npm run build
```

2. Serve static files:
```bash
npm run serve
```

## 🔧 Cấu hình

### API Endpoint
Mặc định chatbot kết nối đến `http://127.0.0.1:8000`. Để thay đổi:

1. Trong `chatbot.html`:
```javascript
apiBaseUrl: 'http://your-api-domain.com'
```

2. Trong `PlantChatbot.vue`:
```javascript
apiBaseUrl: 'http://your-api-domain.com'
```

### Kích thước file
- Tối đa: 10MB
- Định dạng hỗ trợ: JPG, JPEG, PNG, WEBP

## 📖 Cách sử dụng Chatbot

### 1. Phân tích hình ảnh
- Nhấn icon 📷 để chọn hình ảnh
- Hoặc gõ tin nhắn mô tả vấn đề
- Nhấn gửi để phân tích

### 2. Đặt câu hỏi
Các loại câu hỏi được hỗ trợ:
- "Cây này bị bệnh gì?"
- "Làm sao để chăm sóc cây này?"
- "Tại sao lá cây bị vàng?"
- "Khi nào nên tưới nước?"

### 3. Kết quả phân tích
Chatbot sẽ trả về:
- **Nhận dạng cây**: Tên khoa học và thông thường
- **Tình trạng sức khỏe**: Đánh giá tổng thể
- **Phân tích sinh trưởng**: Giai đoạn phát triển
- **Khuyến nghị**: Cách chăm sóc cụ thể

## 🎨 Giao diện

### Desktop
- Sidebar: Thông tin tính năng và trạng thái
- Main chat: Khu vực trò chuyện chính
- Input area: Upload ảnh và nhập tin nhắn

### Mobile
- Responsive design tự động điều chỉnh
- Sidebar thu gọn
- Touch-friendly buttons

## 🔗 Tích hợp API

Chatbot tự động tích hợp với các endpoint:

- `GET /health` - Kiểm tra trạng thái API
- `POST /analyze/complete` - Phân tích toàn diện
- `POST /analyze/identify` - Nhận dạng cây
- `POST /analyze/disease` - Chẩn đoán bệnh
- `POST /analyze/growth` - Đánh giá sinh trưởng

## 📱 Screenshots

### Chat Interface
```
┌─────────────────────────────────────────┐
│ 🌿 Plant AI                             │
│ Chatbot phân tích cây trồng             │
├─────────────────────────────────────────┤
│ 👋 Chào mừng bạn đến với Plant AI!     │
│                                         │
│ Tôi có thể giúp bạn:                   │
│ • 📸 Phân tích hình ảnh cây trồng       │
│ • 🔍 Nhận dạng loại cây                 │
│ • 🩺 Chẩn đoán bệnh trên cây           │
├─────────────────────────────────────────┤
│ 📷 [Upload] [Type message...] [Send] 📤 │
└─────────────────────────────────────────┘
```

## 🛠️ Troubleshooting

### API không kết nối được
- Kiểm tra FastAPI server đang chạy
- Xác nhận port 8000 không bị chặn
- Kiểm tra firewall settings

### Upload ảnh thất bại
- Kiểm tra kích thước file < 10MB
- Đảm bảo định dạng được hỗ trợ
- Thử với ảnh khác

### Phân tích chậm
- Ảnh có thể quá lớn, resize trước khi upload
- Kiểm tra kết nối internet
- Server có thể đang xử lý nhiều request

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Hãy tạo issue hoặc pull request.

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần Troubleshooting
2. Tạo issue trên GitHub
3. Liên hệ team phát triển
