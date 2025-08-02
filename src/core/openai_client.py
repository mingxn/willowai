"""
OpenAI API client for plant analysis.
"""
import base64
import io
from typing import Optional, Dict, Any
from PIL import Image
import openai

try:
    from ..utils.config import config
except ImportError:
    from src.utils.config import config

class OpenAIClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize OpenAI client."""
        client_config = {
            "api_key": api_key or config.OPENAI_API_KEY
        }
        
        # Add base URL if provided
        if base_url or config.OPENAI_BASE_URL:
            client_config["base_url"] = base_url or config.OPENAI_BASE_URL
            
        self.client = openai.OpenAI(**client_config)
    
    def encode_image(self, image_path_or_pil: str | Image.Image) -> str:
        """Encode image to base64 string."""
        if isinstance(image_path_or_pil, str):
            with open(image_path_or_pil, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        else:
            # PIL Image
            buffer = io.BytesIO()
            image_path_or_pil.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def analyze_plant_image(self, image_path_or_pil: str | Image.Image, analysis_type: str = "complete") -> Dict[str, Any]:
        """Analyze plant image using OpenAI Vision API."""
        
        # Encode image
        base64_image = self.encode_image(image_path_or_pil)
        
        # Create prompt based on analysis type
        prompts = {
            "plant_identification": self._get_plant_identification_prompt(),
            "disease_detection": self._get_disease_detection_prompt(),
            "growth_analysis": self._get_growth_analysis_prompt(),
            "complete": self._get_complete_analysis_prompt()
        }
        
        prompt = prompts.get(analysis_type, prompts["complete"])
        
        try:
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE
            )
            
            return {
                "success": True,
                "analysis": response.choices[0].message.content,
                "analysis_type": analysis_type,
                "model_used": config.OPENAI_MODEL
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis_type": analysis_type
            }
    
    def _get_plant_identification_prompt(self) -> str:
        """Get prompt for plant identification."""
        return """
        Hãy phân tích hình ảnh này và xác định loại cây trồng. Vui lòng cung cấp thông tin sau:
        
        1. **Tên khoa học và tên thông thường** của cây
        2. **Họ thực vật** mà cây thuộc về
        3. **Đặc điểm nhận dạng** chính (lá, thân, hoa, quả)
        4. **Độ tin cậy** của việc nhận dạng (%)
        5. **Thông tin bổ sung** về cây (nguồn gốc, mùa sinh trưởng, điều kiện trồng)
        
        Trả lời bằng tiếng Việt với định dạng JSON có cấu trúc rõ ràng.
        """
    
    def _get_disease_detection_prompt(self) -> str:
        """Get prompt for disease detection."""
        return """
        Hãy phân tích hình ảnh này để phát hiện bệnh hoặc vấn đề trên cây trồng. Cung cấp:
        
        1. **Tình trạng sức khỏe** tổng thể của cây (khỏe mạnh/bệnh/suy yếu)
        2. **Các dấu hiệu bệnh** được phát hiện (nếu có)
        3. **Tên bệnh** có thể (nếu xác định được)
        4. **Nguyên nhân** có thể gây ra bệnh
        5. **Mức độ nghiêm trọng** (nhẹ/trung bình/nặng)
        6. **Khuyến nghị điều trị** cụ thể
        7. **Biện pháp phòng ngừa** cho tương lai
        
        Trả lời bằng tiếng Việt với định dạng JSON có cấu trúc rõ ràng.
        """
    
    def _get_growth_analysis_prompt(self) -> str:
        """Get prompt for growth analysis."""
        return """
        Hãy phân tích giai đoạn phát triển và tình trạng sinh trưởng của cây trong hình ảnh:
        
        1. **Giai đoạn phát triển** hiện tại (mầm, non, trưởng thành, già)
        2. **Tình trạng dinh dưỡng** (đủ/thiếu/thừa chất dinh dưỡng)
        3. **Điều kiện môi trường** (ánh sáng, độ ẩm, nhiệt độ - dựa trên dấu hiệu trên cây)
        4. **Tốc độ sinh trưởng** ước tính (chậm/bình thường/nhanh)
        5. **Khuyến nghị chăm sóc** để tối ưu hóa sinh trưởng
        6. **Thời điểm thu hoạch** dự kiến (nếu là cây ăn quả/rau)
        
        Trả lời bằng tiếng Việt với định dạng JSON có cấu trúc rõ ràng.
        """
    
    def _get_complete_analysis_prompt(self) -> str:
        """Get prompt for complete analysis."""
        return """
        Hãy thực hiện phân tích toàn diện cây trồng trong hình ảnh này:
        
        ## 1. NHẬN DẠNG CÂY
        - Tên khoa học và tên thông thường
        - Họ thực vật
        - Đặc điểm nhận dạng chính
        - Độ tin cậy nhận dạng (%)
        
        ## 2. TÌNH TRẠNG SỨC KHỎE
        - Tình trạng tổng thể (khỏe mạnh/bệnh/suy yếu)
        - Các dấu hiệu bệnh (nếu có)
        - Tên bệnh có thể
        - Mức độ nghiêm trọng
        
        ## 3. PHÂN TÍCH SINH TRƯỞNG
        - Giai đoạn phát triển
        - Tình trạng dinh dưỡng
        - Điều kiện môi trường
        - Tốc độ sinh trưởng
        
        ## 4. KHUYẾN NGHỊ
        - Biện pháp điều trị (nếu có bệnh)
        - Cách chăm sóc tối ưu
        - Lịch bón phân và tưới nước
        - Biện pháp phòng ngừa
        - Thời điểm thu hoạch (nếu áp dụng)
        
        ## 5. THÔNG TIN BỔ SUNG
        - Nguồn gốc cây
        - Mùa sinh trưởng tốt nhất
        - Điều kiện trồng lý tưởng
        
        Trả lời bằng tiếng Việt với định dạng JSON có cấu trúc rõ ràng và chi tiết.
        """
