"""
OpenAI API client for plant analysis.
"""

import base64
import io
from typing import Optional, Dict, Any, List
from PIL import Image
import openai
import logging
from datetime import datetime
from pathlib import Path

try:
    from ..utils.config import config
    from .vector_db import get_vector_db
except ImportError:
    from src.utils.config import config
    from src.core.vector_db import get_vector_db

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for interacting with OpenAI API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize OpenAI client."""
        client_config = {"api_key": api_key or config.OPENAI_API_KEY}

        # Add base URL if provided
        if base_url or config.OPENAI_BASE_URL:
            client_config["base_url"] = base_url or config.OPENAI_BASE_URL

        self.client = openai.OpenAI(**client_config)

    def encode_image(self, image_path_or_pil: str | Image.Image) -> str:
        """Encode image to base64 string."""
        if isinstance(image_path_or_pil, str):
            with open(image_path_or_pil, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        else:
            # PIL Image
            buffer = io.BytesIO()
            image_path_or_pil.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def analyze_plant_image(
        self, image_path_or_pil: str | Image.Image, analysis_type: str = "complete"
    ) -> Dict[str, Any]:
        """Analyze plant image using OpenAI Vision API with ChromaDB context."""

        # Encode image
        base64_image = self.encode_image(image_path_or_pil)

        # Query ChromaDB for relevant context
        context_info = self._get_chromadb_context(analysis_type)

        # Create prompt based on analysis type with context
        prompts = {
            "plant_identification": self._get_plant_identification_prompt(context_info),
            "disease_detection": self._get_disease_detection_prompt(context_info),
            "growth_analysis": self._get_growth_analysis_prompt(context_info),
            "complete": self._get_complete_analysis_prompt(context_info),
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
                                },
                            },
                        ],
                    }
                ],
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
            )

            return {
                "success": True,
                "analysis": response.choices[0].message.content,
                "analysis_type": analysis_type,
                "model_used": config.OPENAI_MODEL,
                "context_used": len(context_info) > 0,
                "context_records": len(context_info),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "analysis_type": analysis_type}

    def _get_chromadb_context(
        self, analysis_type: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Query ChromaDB for relevant context based on analysis type."""
        try:
            vector_db = get_vector_db()
            if not vector_db or not vector_db.is_available():
                logger.warning("ChromaDB not available for context retrieval")
                return []

            # Create search queries based on analysis type
            search_queries = {
                "plant_identification": [
                    "plant identification scientific name common name",
                    "plant species botanical family classification",
                    "plant recognition morphology leaves flowers",
                ],
                "disease_detection": [
                    "plant disease symptoms pathogen infection",
                    "plant health problems fungal bacterial viral",
                    "disease diagnosis treatment prevention",
                ],
                "growth_analysis": [
                    "plant growth development stage maturity",
                    "plant nutrition fertilizer nutrient deficiency",
                    "plant care cultivation growing conditions",
                ],
                "complete": [
                    "plant analysis identification health disease",
                    "plant care treatment recommendations",
                    "plant cultivation growing conditions",
                ],
            }

            queries = search_queries.get(analysis_type, search_queries["complete"])
            all_records = []

            # Search with each query and collect unique results
            seen_ids = set()
            for query in queries:
                records = vector_db.search_records(
                    query=query,
                    limit=limit,
                    filter_metadata={"analysis_type": analysis_type}
                    if analysis_type != "complete"
                    else None,
                )

                for record in records:
                    if record["id"] not in seen_ids:
                        all_records.append(record)
                        seen_ids.add(record["id"])

                        if len(all_records) >= limit:
                            break

                if len(all_records) >= limit:
                    break

            logger.info(
                f"Retrieved {len(all_records)} context records from ChromaDB for {analysis_type}"
            )
            return all_records[:limit]

        except Exception as e:
            logger.error(f"Failed to retrieve ChromaDB context: {e}")
            return []

    def _format_context_for_prompt(self, context_records: List[Dict[str, Any]]) -> str:
        """Format ChromaDB context records for inclusion in prompts."""
        if not context_records:
            return ""

        context_text = "\n## KIẾN THỨC THAM KHẢO TỪ CƠ SỞ DỮ LIỆU:\n"

        for i, record in enumerate(context_records, 1):
            metadata = record.get("metadata", {})

            context_text += f"\n### Trường hợp {i}:\n"
            context_text += (
                f"- **Loại phân tích**: {metadata.get('analysis_type', 'không rõ')}\n"
            )
            context_text += (
                f"- **Loại cây**: {metadata.get('plant_type', 'không rõ')}\n"
            )
            context_text += f"- **Tình trạng sức khỏe**: {metadata.get('health_status', 'không rõ')}\n"

            # Add relevant analysis excerpts
            document = record.get("document", "")
            if document:
                # Extract key information from document
                lines = document.strip().split("\n")
                relevant_lines = [line.strip() for line in lines if line.strip()][
                    :5
                ]  # First 5 lines
                context_text += f"- **Kết quả phân tích**: {' '.join(relevant_lines)}\n"

            # Add distance/similarity score if available
            if "distance" in record and record["distance"] is not None:
                similarity = max(
                    0, 1 - record["distance"]
                )  # Convert distance to similarity
                context_text += f"- **Độ tương đồng**: {similarity:.2f}\n"

        context_text += "\n**Lưu ý**: Sử dụng thông tin tham khảo này để đưa ra phân tích chính xác hơn, nhưng vẫn tập trung vào hình ảnh hiện tại.\n"

        return context_text

    def _get_plant_identification_prompt(
        self, context_records: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Get prompt for plant identification with ChromaDB context."""
        base_prompt = """
        Hãy phân tích hình ảnh này và xác định loại cây trồng. Vui lòng cung cấp thông tin sau:
        
        1. **Tên khoa học và tên thông thường** của cây
        2. **Họ thực vật** mà cây thuộc về
        3. **Đặc điểm nhận dạng** chính (lá, thân, hoa, quả)
        4. **Độ tin cậy** của việc nhận dạng (%)
        5. **Thông tin bổ sung** về cây (nguồn gốc, mùa sinh trưởng, điều kiện trồng)
        
        Trả lời bằng tiếng Việt với định dạng JSON có cấu trúc rõ ràng.
        """

        if context_records:
            context_text = self._format_context_for_prompt(context_records)
            return context_text + "\n" + base_prompt

        return base_prompt

    def _get_disease_detection_prompt(
        self, context_records: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Get prompt for disease detection with ChromaDB context."""
        base_prompt = """
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

        if context_records:
            context_text = self._format_context_for_prompt(context_records)
            return context_text + "\n" + base_prompt

        return base_prompt

    def _get_growth_analysis_prompt(
        self, context_records: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Get prompt for growth analysis with ChromaDB context."""
        base_prompt = """
        Hãy phân tích giai đoạn phát triển và tình trạng sinh trưởng của cây trong hình ảnh:
        
        1. **Giai đoạn phát triển** hiện tại (mầm, non, trưởng thành, già)
        2. **Tình trạng dinh dưỡng** (đủ/thiếu/thừa chất dinh dưỡng)
        3. **Điều kiện môi trường** (ánh sáng, độ ẩm, nhiệt độ - dựa trên dấu hiệu trên cây)
        4. **Tốc độ sinh trưởng** ước tính (chậm/bình thường/nhanh)
        5. **Khuyến nghị chăm sóc** để tối ưu hóa sinh trưởng
        6. **Thời điểm thu hoạch** dự kiến (nếu là cây ăn quả/rau)
        
        Trả lời bằng tiếng Việt với định dạng JSON có cấu trúc rõ ràng.
        """

        if context_records:
            context_text = self._format_context_for_prompt(context_records)
            return context_text + "\n" + base_prompt

        return base_prompt

    def _get_complete_analysis_prompt(
        self, context_records: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Get prompt for complete analysis with ChromaDB context."""
        base_prompt = """
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

        if context_records:
            context_text = self._format_context_for_prompt(context_records)
            return context_text + "\n" + base_prompt

        return base_prompt
