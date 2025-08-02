# Plant Analysis AI - API Documentation

## Tổng quan

Plant Analysis AI API cung cấp các endpoints để phân tích cây trồng từ hình ảnh sử dụng OpenAI Vision API.

## Base URL

```
http://localhost:8000
```

## Authentication

API sử dụng OpenAI API key được cấu hình trong environment variables. Không cần authentication cho client.

## Endpoints

### 1. Root Information
```http
GET /
```

Trả về thông tin tổng quan về API.

**Response:**
```json
{
  "message": "🌿 Welcome to Plant Analysis AI API",
  "project": "Plant Analysis AI",
  "version": "1.0.0",
  "description": "AI-powered plant analysis using OpenAI vision capabilities",
  "docs": "/docs",
  "endpoints": {
    "analyze_complete": "/analyze/complete",
    "analyze_plant": "/analyze/plant",
    "analyze_disease": "/analyze/disease", 
    "analyze_growth": "/analyze/growth",
    "health": "/health",
    "info": "/info"
  }
}
```

### 2. Health Check
```http
GET /health
```

Kiểm tra tình trạng hoạt động của API và kết nối OpenAI.

**Response (Healthy):**
```json
{
  "status": "healthy",
  "message": "API is running and OpenAI connection is working",
  "openai_status": "connected"
}
```

### 3. Project Information
```http
GET /info
```

Lấy thông tin chi tiết về project.

### 4. Analysis Types
```http
GET /analysis/types
```

Lấy danh sách các loại phân tích được hỗ trợ.

**Response:**
```json
{
  "supported_types": [
    "plant_identification",
    "disease_detection", 
    "growth_analysis",
    "complete"
  ],
  "descriptions": {
    "plant_identification": "Nhận dạng loại cây trồng",
    "disease_detection": "Phát hiện bệnh trên cây",
    "growth_analysis": "Phân tích tình trạng sinh trưởng", 
    "complete": "Phân tích toàn diện (bao gồm tất cả)"
  }
}
```

### 5. Complete Analysis
```http
POST /analyze/complete
```

Thực hiện phân tích toàn diện cây trồng.

**Parameters:**
- `file` (file, required): Hình ảnh cây trồng
- `enhance_image` (boolean, optional): Tăng cường chất lượng ảnh (default: true)
- `remove_background` (boolean, optional): Loại bỏ background (default: false)
- `save_result` (boolean, optional): Lưu kết quả (default: false)

**Response:**
```json
{
  "success": true,
  "analysis_type": "complete",
  "model_used": "gpt-4-vision-preview",
  "analysis_text": "Detailed analysis text...",
  "structured_data": {...},
  "plant_type": "Solanum lycopersicum",
  "health_status": "Khỏe mạnh",
  "recommendations": ["Suggestion 1", "Suggestion 2"],
  "image_info": {
    "size": [800, 600],
    "mode": "RGB",
    "format": "JPEG"
  },
  "request_metadata": {
    "filename": "plant.jpg",
    "file_size": 102400,
    "analysis_type": "complete",
    "enhance_image": true,
    "remove_background": false
  }
}
```

### 6. Plant Identification
```http
POST /analyze/plant
```

Chỉ thực hiện nhận dạng loại cây.

**Parameters:** Giống như `/analyze/complete`

### 7. Disease Detection
```http
POST /analyze/disease
```

Chỉ phát hiện bệnh trên cây.

**Parameters:** Giống như `/analyze/complete`

### 8. Growth Analysis
```http
POST /analyze/growth
```

Chỉ phân tích tình trạng sinh trưởng.

**Parameters:** Giống như `/analyze/complete`

### 9. Batch Analysis
```http
POST /analyze/batch
```

Phân tích nhiều hình ảnh cùng lúc (tối đa 10 files).

**Parameters:**
- `files` (array of files, required): Danh sách hình ảnh
- `analysis_type` (string, optional): Loại phân tích (default: "complete")
- `enhance_image` (boolean, optional): Tăng cường ảnh (default: true)
- `remove_background` (boolean, optional): Loại bỏ background (default: false)
- `save_results` (boolean, optional): Lưu kết quả (default: false)

**Response:**
```json
{
  "batch_results": {
    "image1.jpg": {...},
    "image2.jpg": {...}
  },
  "total_files": 2,
  "successful_analyses": 2,
  "failed_analyses": 0
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message",
  "message": "Detailed error description"
}
```

### 503 Service Unavailable
```json
{
  "status": "unhealthy",
  "message": "Analyzer not initialized"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "message": "Error details"
}
```

## Usage Examples

### cURL Examples

**Complete Analysis:**
```bash
curl -X POST "http://localhost:8000/analyze/complete" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@plant_image.jpg" \
  -F "enhance_image=true" \
  -F "save_result=true"
```

**Health Check:**
```bash
curl -X GET "http://localhost:8000/health"
```

### Python Example

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Analyze image
with open("plant_image.jpg", "rb") as f:
    files = {"file": f}
    data = {"enhance_image": True, "save_result": True}
    response = requests.post(
        "http://localhost:8000/analyze/complete",
        files=files,
        data=data
    )
    result = response.json()
    print(result)
```

### JavaScript Example

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('enhance_image', 'true');
formData.append('save_result', 'true');

fetch('http://localhost:8000/analyze/complete', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Rate Limiting

Hiện tại chưa có rate limiting. Trong production nên implement rate limiting để bảo vệ API.

## File Size Limits

- Maximum file size: 10MB
- Supported formats: JPG, JPEG, PNG, WEBP
- Batch analysis: Maximum 10 files per request

## Performance Notes

- Phân tích có thể mất 5-30 giây tùy thuộc vào độ phức tạp của hình ảnh
- Enable `enhance_image` sẽ tăng thời gian xử lý nhưng cải thiện chất lượng phân tích
- Background removal là tính năng thử nghiệm và có thể không hoạt động tốt với mọi loại ảnh
