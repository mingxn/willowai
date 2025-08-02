# 🌿 Plant Analysis AI Project

Dự án phân tích cây trồng thông minh bằng hình ảnh sử dụng OpenAI API và Python. Hệ thống tích hợp ChatBot UI hiện đại với khả năng nhận dạng cây, chẩn đoán bệnh và tư vấn chăm sóc bằng tiếng Việt.

## ✨ Tính năng chính

- 🌱 **Nhận dạng cây trồng**: Xác định loại cây từ hình ảnh với độ tin cậy cao
- 🔍 **Chẩn đoán bệnh**: Phát hiện và phân tích bệnh trên cây với khuyến nghị điều trị
- 📊 **Phân tích sinh trưởng**: Đánh giá tình trạng phát triển và dinh dưỡng
- 💡 **Tư vấn chăm sóc**: Khuyến nghị chăm sóc cụ thể phù hợp với từng loại cây
- 🤖 **ChatBot thông minh**: Giao diện chat tương tác bằng tiếng Việt
- 📱 **Responsive UI**: Tương thích với mọi thiết bị (desktop, tablet, mobile)
- 🔄 **Real-time Analysis**: Phân tích hình ảnh và phản hồi tức thời

## 🚀 Demo và Giao diện

### 1. ChatBot Vue.js (Khuyến nghị) 🌟
- **URL**: http://localhost:3000
- **Tính năng**: 
  - Chat interface hiện đại
  - Upload hình ảnh drag & drop
  - Hiển thị kết quả được format đẹp
  - Real-time typing indicator
  - Responsive design

### 2. ChatBot HTML (Standalone)
- **File**: `ui/chatbot.html`
- **Tính năng**: 
  - Không cần cài đặt gì thêm
  - Mở trực tiếp trong trình duyệt
  - Giao diện tương tự Vue.js

### 3. API Documentation
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

## 🛠️ Cài đặt

### 1. Yêu cầu hệ thống
- **Python**: 3.8+ 
- **Node.js**: 18+ (cho Vue.js UI)
- **OpenAI API Key**: Cần có tài khoản OpenAI

### 2. Clone project và di chuyển vào thư mục
```bash
cd plant-analysis-ai
```

### 3. Cài đặt Python dependencies
```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
```

### 4. Cài đặt Node.js dependencies (cho Vue.js UI)
```bash
cd ui
npm install
cd ..
```

### 5. Cấu hình environment variables
Tạo file `.env` trong thư mục gốc:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1  # hoặc custom endpoint
```

### 6. Test cài đặt
```bash
# Test Python modules
python -c "import src.core.plant_analyzer; print('✅ Python modules OK')"

# Test API connection
python -c "from src.core.openai_client import OpenAIClient; client = OpenAIClient(); print('✅ API connection OK')"
```

## 📱 Sử dụng - Hướng dẫn chi tiết

### 🌟 Phương pháp 1: ChatBot Vue.js (Khuyến nghị)

1. **Khởi động API server**:
```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 5000
```

2. **Khởi động Vue.js development server**:
```bash
cd ui
npm run dev
```

3. **Truy cập ChatBot**:
- Mở trình duyệt: http://localhost:3000
- Upload hình ảnh cây hoặc chat với AI
- Xem kết quả được format đẹp mắt

### 💻 Phương pháp 2: ChatBot HTML (Đơn giản)

1. **Khởi động API server** (như trên)

2. **Mở file HTML**:
```bash
# Mở file trực tiếp trong trình duyệt
ui/chatbot.html
```

### 🌐 Phương pháp 3: Streamlit Web Interface

```bash
streamlit run src/web_app.py
```

### ⌨️ Phương pháp 4: Command Line Interface

```bash
# Phân tích toàn diện
python src/main.py --image path/to/image.jpg --analysis complete --verbose

# Chỉ nhận dạng cây
python src/main.py --image path/to/image.jpg --analysis identify

# Chỉ chẩn đoán bệnh
python src/main.py --image path/to/image.jpg --analysis disease
```

### 🔧 Phương pháp 5: API Testing

```bash
# Swagger UI - Giao diện test API
http://localhost:5000/docs

# ReDoc - API Documentation
http://localhost:5000/redoc

# Health Check
curl http://localhost:5000/health
```

## 🏗️ Cấu trúc project chi tiết

```
plant-analysis-ai/
├── 🐍 Backend (Python)
│   ├── src/
│   │   ├── core/                     # 🧠 Core AI modules
│   │   │   ├── plant_analyzer.py     # Main AI analysis engine
│   │   │   ├── image_processor.py    # Image enhancement & processing
│   │   │   └── openai_client.py      # OpenAI API integration
│   │   ├── api/                      # 🌐 FastAPI REST API
│   │   │   ├── main.py              # FastAPI application & routes
│   │   │   └── __init__.py
│   │   ├── models/                   # 📋 Data models & structures
│   │   │   ├── data_models.py       # Pydantic models
│   │   │   └── __init__.py
│   │   ├── utils/                    # 🔧 Helper functions
│   │   │   ├── config.py            # Configuration management
│   │   │   ├── helpers.py           # Utility functions
│   │   │   └── __init__.py
│   │   ├── web_app.py               # 🎨 Streamlit web interface
│   │   └── main.py                  # ⌨️ CLI application
│   └── tests/                       # 🧪 Unit tests
│       ├── test_analyzer.py
│       ├── test_api.py
│       └── __init__.py
├── 🎨 Frontend (JavaScript/Vue.js)
│   └── ui/
│       ├── 📱 Vue.js App
│       │   ├── src/
│       │   │   ├── App.vue          # Main Vue application
│       │   │   ├── main.js          # Entry point
│       │   │   ├── style.css        # Global styles
│       │   │   └── components/
│       │   │       └── PlantChatbot.vue  # Main chatbot component
│       │   ├── package.json         # Node.js dependencies
│       │   ├── vite.config.js       # Vite build configuration
│       │   └── index.html           # HTML template
│       ├── 🌐 Standalone HTML
│       │   └── chatbot.html         # Self-contained chatbot
│       └── README.md                # UI documentation
├── 📁 Data & Storage
│   ├── data/
│   │   ├── sample_images/           # Sample images for testing
│   │   └── results/                 # Analysis results storage
│   └── docs/
│       └── API.md                   # API documentation
├── ⚙️ Configuration
│   ├── .env                         # Environment variables (create this)
│   ├── .env.example                 # Environment template
│   ├── requirements.txt             # Python dependencies
│   ├── .gitignore                   # Git ignore rules
│   └── README.md                    # This file
```

### 📊 Tech Stack

**Backend:**
- 🐍 **Python 3.8+**: Core language
- 🤖 **OpenAI GPT-4 Vision**: AI analysis engine
- ⚡ **FastAPI**: Modern REST API framework
- 🖼️ **PIL/OpenCV**: Image processing
- 📊 **NumPy**: Numerical operations
- 🎨 **Streamlit**: Web interface alternative

**Frontend:**
- 🟢 **Vue.js 3**: Progressive JavaScript framework
- ⚡ **Vite**: Modern build tool
- 🌐 **HTML5/CSS3**: Standalone version
- 📱 **Responsive Design**: Mobile-friendly UI
- 🎨 **Font Awesome**: Icons

**API & Integration:**
- 🔗 **Axios**: HTTP client
- 📋 **Swagger/OpenAPI**: API documentation
- 🔧 **CORS**: Cross-origin support
- 📁 **Multipart Upload**: File handling

## 📊 API Endpoints - Tài liệu API

### 🌿 Phân tích cây trồng
| Endpoint | Method | Mô tả | Tham số |
|----------|--------|-------|---------|
| `/analyze/identify` | POST | Nhận dạng loại cây từ hình ảnh | `file`, `enhance_image` |
| `/analyze/disease` | POST | Phát hiện và chẩn đoán bệnh trên cây | `file`, `enhance_image` |
| `/analyze/growth` | POST | Phân tích tình trạng sinh trưởng | `file`, `enhance_image` |
| `/analyze/complete` | POST | Phân tích toàn diện (tất cả) | `file`, `enhance_image` |

### 🖼️ Xử lý ảnh
| Endpoint | Method | Mô tả | Tham số |
|----------|--------|-------|---------|
| `/enhance-image` | POST | Cải thiện chất lượng hình ảnh | `file` |
| `/analyze/batch` | POST | Phân tích nhiều hình ảnh cùng lúc | `files[]` |

### ⚙️ Hệ thống
| Endpoint | Method | Mô tả | Response |
|----------|--------|-------|----------|
| `/health` | GET | Kiểm tra trạng thái server | JSON status |
| `/` | GET | Trang chủ API | HTML welcome |

## 🎯 Cách sử dụng API

### 💬 1. Sử dụng ChatBot (Khuyến nghị cho người dùng cuối)

**Vue.js ChatBot**: http://localhost:3000
- Giao diện thân thiện, dễ sử dụng
- Upload ảnh bằng drag & drop
- Kết quả hiển thị đẹp mắt với emoji và format
- Chat tương tác bằng tiếng Việt

**HTML ChatBot**: `ui/chatbot.html`
- Không cần cài đặt Node.js
- Mở trực tiếp trong trình duyệt
- Tương tự giao diện Vue.js

### 🧪 2. Test API với Swagger UI

```bash
# Mở Swagger UI
http://localhost:5000/docs

# Các bước test:
1. Chọn endpoint (ví dụ: /analyze/complete)
2. Click "Try it out"
3. Upload file ảnh
4. Chọn enhance_image = true
5. Click "Execute"
6. Xem kết quả JSON
```

### 💻 3. Sử dụng với curl

```bash
# Phân tích toàn diện
curl -X POST "http://localhost:5000/analyze/complete" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/image.jpg" \
     -F "enhance_image=true"

# Chỉ nhận dạng cây
curl -X POST "http://localhost:5000/analyze/identify" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/image.jpg"
```

### 🐍 4. Sử dụng với Python

```python
import requests

# Upload và phân tích ảnh
def analyze_plant_image(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'enhance_image': 'true'}
        response = requests.post(
            'http://localhost:5000/analyze/complete',
            files=files,
            data=data
        )
        return response.json()

# Sử dụng
result = analyze_plant_image('path/to/plant.jpg')
print(f"Loại cây: {result['plant_type']}")
print(f"Tình trạng: {result['health_status']}")
print("Khuyến nghị:", result['recommendations'])
```

### 🌐 5. Sử dụng với JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function analyzePlant(imagePath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(imagePath));
    form.append('enhance_image', 'true');

    try {
        const response = await axios.post(
            'http://localhost:5000/analyze/complete',
            form,
            { headers: form.getHeaders() }
        );
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Sử dụng
analyzePlant('path/to/plant.jpg').then(result => {
    console.log('Kết quả phân tích:', result.analysis_text);
});
```

## 📋 Cấu trúc JSON Response

```json
{
  "success": true,
  "analysis_type": "complete",
  "model_used": "GPT-4o",
  "analysis_text": "Kết quả phân tích chi tiết bằng tiếng Việt...",
  "structured_data": {
    "plant_info": {
      "scientific_name": "Tên khoa học",
      "common_name": "Tên thông thường", 
      "confidence": 85
    },
    "health_status": {
      "overall_status": "Khỏe mạnh/Bệnh/Suy yếu",
      "severity_level": "Nhẹ/Trung bình/Nặng"
    },
    "growth_analysis": {
      "stage": "Giai đoạn phát triển",
      "nutrition_status": "Tình trạng dinh dưỡng"
    },
    "recommendations": {
      "treatment_steps": ["Bước điều trị 1", "Bước 2"],
      "care_instructions": ["Hướng dẫn chăm sóc 1", "Hướng dẫn 2"]
    }
  },
  "plant_type": "Loại cây",
  "health_status": "Tình trạng sức khỏe",
  "recommendations": ["Khuyến nghị 1", "Khuyến nghị 2"],
  "saved_at": "2025-07-26T21:14:22.557242"
}
```

## 💡 Ví dụ sử dụng thực tế

### 🌿 Sử dụng ChatBot (Khuyến nghị)

1. **Mở ChatBot**: http://localhost:3000
2. **Upload hình ảnh**: Kéo thả hoặc click icon 📷
3. **Đặt câu hỏi**: "Cây này bị bệnh gì?" hoặc "Làm sao chăm sóc?"
4. **Xem kết quả**: Định dạng đẹp với emoji và tiếng Việt

### 🐍 Sử dụng Python Code

```python
from src.core.plant_analyzer import PlantAnalyzer

# Khởi tạo analyzer
analyzer = PlantAnalyzer()

# Phân tích hình ảnh
result = analyzer.analyze_plant_image("path/to/plant.jpg")

# Xem kết quả
print(f"🌿 Loại cây: {result.plant_type}")
print(f"💚 Tình trạng: {result.health_status}")
print("💡 Khuyến nghị:")
for rec in result.recommendations:
    print(f"  • {rec}")
```

### ⌨️ Sử dụng Command Line

```bash
# Phân tích ảnh cây cam bị bệnh
python src/main.py --image "samples/orange_tree_disease.jpg" --analysis complete --verbose

# Kết quả mẫu:
# 🔍 NHẬN DẠNG CÂY: Citrus sp. (Cây cam/quýt) - 90% tin cậy
# ⚕️ TÌNH TRẠNG: Bệnh - Sâu vẽ bùa (Leaf miner)
# 💡 KHUYẾN NGHỊ: Sử dụng thuốc trừ sâu sinh học...
```

## 🎯 Use Cases - Các trường hợp sử dụng

### 🌱 Cho nông dân và người trồng cây
- **Chẩn đoán nhanh**: Upload ảnh để phát hiện bệnh sớm
- **Tư vấn điều trị**: Nhận khuyến nghị cụ thể cho từng loại bệnh
- **Theo dõi sinh trưởng**: Đánh giá tình trạng phát triển của cây

### 🎓 Cho giáo dục và nghiên cứu
- **Học tập**: Nhận dạng các loài cây khác nhau
- **Nghiên cứu**: Phân tích và lưu trữ dữ liệu phân tích
- **Thực hành**: Test kiến thức về bệnh cây và chăm sóc

### 🏢 Cho doanh nghiệp nông nghiệp
- **API Integration**: Tích hợp vào ứng dụng mobile/web
- **Batch Processing**: Phân tích hàng loạt hình ảnh
- **Custom Training**: Huấn luyện model cho cây trồng cụ thể

### 🏠 Cho người yêu cây cảnh
- **Nhận dạng cây**: Xác định loại cây mới mua
- **Chăm sóc**: Học cách chăm sóc đúng cách
- **Giải quyết vấn đề**: Tìm nguyên nhân khi cây héo, vàng lá

## 🔧 Troubleshooting - Khắc phục sự cố

### ❌ Lỗi thường gặp

**1. API không kết nối được**
```bash
# Kiểm tra API server
curl http://localhost:5000/health

# Nếu lỗi, khởi động lại:
python -m uvicorn src.api.main:app --reload --port 5000
```

**2. ChatBot hiển thị JSON thô**
- ✅ **Đã khắc phục**: Sử dụng chatbot mới với format đẹp
- 🌐 Truy cập: http://localhost:3000 hoặc `ui/chatbot.html`

**3. Upload ảnh thất bại**
```bash
# Kiểm tra định dạng file (JPG, PNG, WEBP)
# Kiểm tra kích thước < 10MB
# Thử với ảnh khác
```

**4. OpenAI API lỗi**
```bash
# Kiểm tra API key trong .env
cat .env | grep OPENAI_API_KEY

# Test API connection
python -c "from src.core.openai_client import OpenAIClient; OpenAIClient().test_connection()"
```

**5. Vue.js dev server không chạy**
```bash
cd ui
npm install  # Cài lại dependencies
npm run dev  # Khởi động lại
```

### 🔍 Debug và Logs

```bash
# Xem logs API server
python -m uvicorn src.api.main:app --reload --log-level debug

# Test từng module
python -c "import src.core.plant_analyzer; print('✅ Core modules OK')"
python -c "import src.api.main; print('✅ API modules OK')"

# Kiểm tra Python environment
pip list | grep -E "(fastapi|openai|pillow)"
```

## 🤝 Đóng góp và Phát triển

### 🚀 Roadmap phát triển

**Version 2.0 (Planned)**
- [ ] 🔄 Real-time chat với WebSocket
- [ ] 📱 Mobile app (React Native)
- [ ] 🧠 Custom AI model training
- [ ] 🌍 Multi-language support
- [ ] 📊 Analytics dashboard
- [ ] 🔐 User authentication
- [ ] ☁️ Cloud deployment

**Version 1.2 (Current)**
- [x] ✅ Vue.js ChatBot UI
- [x] ✅ Improved JSON response formatting
- [x] ✅ Image enhancement
- [x] ✅ Batch processing
- [x] ✅ Comprehensive API documentation

### 🛠️ Cách đóng góp

1. **Fork repository**
```bash
git clone https://github.com/your-username/plant-analysis-ai.git
cd plant-analysis-ai
```

2. **Tạo feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Phát triển và test**
```bash
# Thêm code mới
# Chạy tests
python -m pytest tests/
```

4. **Commit và push**
```bash
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

5. **Tạo Pull Request**

### 🧪 Testing

```bash
# Chạy tất cả tests
python -m pytest tests/ -v

# Test specific module
python -m pytest tests/test_analyzer.py -v

# Test API endpoints
python -m pytest tests/test_api.py -v

# Test coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### 📝 Code Standards

- **Python**: Follow PEP 8
- **JavaScript**: ESLint + Prettier
- **Documentation**: Comprehensive docstrings
- **Comments**: Vietnamese for user-facing, English for code
- **Type Hints**: Required for all Python functions

## 📄 License và Credits

### 📜 License
```
MIT License

Copyright (c) 2025 Plant Analysis AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

### 🙏 Credits và Acknowledgments

- **OpenAI**: GPT-4 Vision API for plant analysis
- **FastAPI**: Modern Python web framework
- **Vue.js**: Progressive JavaScript framework
- **Streamlit**: Rapid web app development
- **OpenCV**: Computer vision library
- **Font Awesome**: Beautiful icons

### 🌟 Contributors

- **Main Developer**: [Your Name]
- **UI/UX Design**: Community contributions welcome
- **Documentation**: Community maintained
- **Testing**: Automated + community testing

## 📞 Hỗ trợ và Liên hệ

### 🆘 Nhận hỗ trợ

1. **Đọc documentation**: Kiểm tra README và API docs
2. **Tìm kiếm issues**: GitHub Issues tab
3. **Tạo issue mới**: Mô tả chi tiết vấn đề
4. **Community Discord**: [Link to Discord] (if available)

### 📧 Liên hệ

- **GitHub Issues**: Cho bug reports và feature requests
- **Email**: your-email@domain.com
- **LinkedIn**: [Your LinkedIn Profile]

### 🌟 Star the project

Nếu project này hữu ích cho bạn, đừng quên ⭐ star repository để ủng hộ!

---

**🌿 Plant Analysis AI - Công nghệ AI phục vụ nông nghiệp Việt Nam**

*"Bringing AI to agriculture, one plant at a time"* 🌱✨
