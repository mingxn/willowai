"""
Helper functions and utilities.
"""
import os
import json
import time
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

def save_analysis_result(result: Dict[str, Any], output_dir: str = "data/results") -> str:
    """Save analysis result to JSON file."""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plant_analysis_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Add timestamp to result
    result["saved_at"] = datetime.now().isoformat()
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return filepath

def load_analysis_result(filepath: str) -> Dict[str, Any]:
    """Load analysis result from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_analysis_for_display(result: Dict[str, Any]) -> str:
    """Format analysis result for human-readable display."""
    if not result.get("success", False):
        return f"❌ Phân tích thất bại: {result.get('error', 'Unknown error')}"
    
    output = []
    output.append("🌿 KẾT QUẢ PHÂN TÍCH CÂY TRỒNG")
    output.append("=" * 60)
    
    # Try to parse and display the raw analysis text first
    analysis_text = result.get("analysis_text", "")
    if analysis_text:
        # Remove JSON markers and clean up the text
        clean_text = analysis_text.replace("```json", "").replace("```", "").strip()
        
        try:
            import json
            import re
            
            # Try to parse as JSON and format nicely
            if clean_text.startswith('{'):
                parsed_data = json.loads(clean_text)
                output.append(format_parsed_analysis(parsed_data))
            else:
                output.append(f"\n📝 PHÂN TÍCH CHI TIẾT:")
                output.append(clean_text)
                
        except json.JSONDecodeError:
            # If not valid JSON, display as text
            output.append(f"\n📝 PHÂN TÍCH CHI TIẾT:")
            output.append(clean_text)
    
    # Fallback to basic info if available
    plant_type = result.get("plant_type")
    if plant_type:
        output.append(f"\n🔍 NHẬN DẠNG CÂY:")
        output.append(f"   Loại cây: {plant_type}")
    
    health_status = result.get("health_status")
    if health_status:
        output.append(f"\n💚 TÌNH TRẠNG SỨC KHỎE:")
        output.append(f"   Trạng thái: {health_status}")
    
    recommendations = result.get("recommendations", [])
    if recommendations:
        output.append(f"\n💡 KHUYẾN NGHỊ:")
        for i, rec in enumerate(recommendations[:5], 1):
            output.append(f"   {i}. {rec}")
    
    # Analysis metadata
    output.append(f"\n📊 THÔNG TIN PHÂN TÍCH:")
    output.append(f"   Loại phân tích: {result.get('analysis_type', 'N/A')}")
    output.append(f"   Model sử dụng: {result.get('model_used', 'N/A')}")
    
    if "image_info" in result:
        img_info = result["image_info"]
        output.append(f"   Kích thước ảnh: {img_info.get('size', 'N/A')}")
    
    return "\n".join(output)

def format_parsed_analysis(data: Dict[str, Any]) -> str:
    """Format parsed JSON analysis data for display."""
    output = []
    
    # Process each section
    for key, value in data.items():
        if "NHẬN DẠNG" in key or "NHAN DANG" in key:
            output.append(f"\n🔍 {key}")
            output.append("-" * 40)
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        output.append(f"   {sub_key}:")
                        for detail_key, detail_value in sub_value.items():
                            output.append(f"      • {detail_key}: {detail_value}")
                    else:
                        output.append(f"   • {sub_key}: {sub_value}")
        
        elif "TÌNH TRẠNG" in key or "TINH TRANG" in key:
            output.append(f"\n⚕️ {key}")
            output.append("-" * 40)
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        output.append(f"   {sub_key}:")
                        for detail_key, detail_value in sub_value.items():
                            output.append(f"      • {detail_value}")
                    else:
                        output.append(f"   • {sub_key}: {sub_value}")
        
        elif "SINH TRƯỞNG" in key or "SINH TRUONG" in key:
            output.append(f"\n📈 {key}")
            output.append("-" * 40)
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        output.append(f"   {sub_key}:")
                        for detail_key, detail_value in sub_value.items():
                            output.append(f"      • {detail_key}: {detail_value}")
                    else:
                        output.append(f"   • {sub_key}: {sub_value}")
        
        elif "KHUYẾN NGHỊ" in key or "KHUYEN NGHI" in key:
            output.append(f"\n💡 {key}")
            output.append("-" * 40)
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        output.append(f"   {sub_key}:")
                        for detail_key, detail_value in sub_value.items():
                            output.append(f"      • {detail_key}: {detail_value}")
                    else:
                        output.append(f"   • {sub_key}: {sub_value}")
        
        elif "THÔNG TIN" in key or "THONG TIN" in key:
            output.append(f"\n📋 {key}")
            output.append("-" * 40)
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        output.append(f"   {sub_key}:")
                        for detail_key, detail_value in sub_value.items():
                            output.append(f"      • {detail_key}: {detail_value}")
                    else:
                        output.append(f"   • {sub_key}: {sub_value}")
    
    return "\n".join(output)

def create_sample_images_info() -> List[Dict[str, str]]:
    """Create information about sample images for testing."""
    return [
        {
            "filename": "tomato_healthy.jpg",
            "description": "Cây cà chua khỏe mạnh",
            "expected_analysis": "plant_identification"
        },
        {
            "filename": "rice_disease.jpg", 
            "description": "Cây lúa bị bệnh",
            "expected_analysis": "disease_detection"
        },
        {
            "filename": "corn_growth.jpg",
            "description": "Cây ngô đang phát triển",
            "expected_analysis": "growth_analysis"
        }
    ]

def validate_image_path(image_path: str) -> bool:
    """Validate if image path exists and is supported format."""
    if not os.path.exists(image_path):
        return False
    
    ext = os.path.splitext(image_path)[1].lower()
    supported_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    
    return ext in supported_extensions

def measure_execution_time(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Add timing info to result if it's a dictionary
        if isinstance(result, dict):
            result["execution_time"] = execution_time
        
        return result
    return wrapper

def create_analysis_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Create a summary from multiple analysis results."""
    summary = {
        "total_analyses": len(results),
        "successful_analyses": 0,
        "failed_analyses": 0,
        "analysis_types": {},
        "common_plant_types": {},
        "common_health_issues": [],
        "timestamp": datetime.now().isoformat()
    }
    
    for filepath, result in results.items():
        if result.get("success", False):
            summary["successful_analyses"] += 1
            
            # Count analysis types
            analysis_type = result.get("analysis_type", "unknown")
            summary["analysis_types"][analysis_type] = summary["analysis_types"].get(analysis_type, 0) + 1
            
            # Count plant types
            plant_type = result.get("plant_type")
            if plant_type:
                summary["common_plant_types"][plant_type] = summary["common_plant_types"].get(plant_type, 0) + 1
            
            # Collect health issues
            health_status = result.get("health_status", "")
            if "bệnh" in health_status.lower() or "disease" in health_status.lower():
                summary["common_health_issues"].append(health_status)
        else:
            summary["failed_analyses"] += 1
    
    return summary

def setup_project_directories():
    """Set up necessary project directories."""
    directories = [
        "data/sample_images",
        "data/results", 
        "docs",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep files for empty directories
        gitkeep_path = Path(directory) / ".gitkeep"
        if not gitkeep_path.exists():
            gitkeep_path.touch()

def get_project_info() -> Dict[str, Any]:
    """Get information about the current project setup."""
    return {
        "project_name": "Plant Analysis AI",
        "version": "1.0.0",
        "description": "AI-powered plant analysis using OpenAI vision capabilities",
        "author": "Plant Analysis Team",
        "python_version": "3.8+",
        "main_dependencies": [
            "openai>=1.0.0",
            "pillow>=10.0.0", 
            "opencv-python>=4.8.0",
            "streamlit>=1.28.0",
            "fastapi>=0.104.0"
        ],
        "supported_analysis_types": [
            "plant_identification",
            "disease_detection",
            "growth_analysis", 
            "complete"
        ],
        "supported_image_formats": ["jpg", "jpeg", "png", "webp"]
    }
