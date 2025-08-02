"""
Main plant analyzer class that combines image processing and AI analysis.
"""
import json
from typing import Dict, Any, Optional
from PIL import Image

try:
    from .openai_client import OpenAIClient
    from .image_processor import ImageProcessor
    from ..utils.config import config
except ImportError:
    from src.core.openai_client import OpenAIClient
    from src.core.image_processor import ImageProcessor
    from src.utils.config import config

class PlantAnalysisResult:
    """Container for plant analysis results."""
    
    def __init__(self, raw_response: Dict[str, Any]):
        """Initialize with raw API response."""
        self.raw_response = raw_response
        self.success = raw_response.get("success", False)
        self.analysis_type = raw_response.get("analysis_type", "unknown")
        self.model_used = raw_response.get("model_used", "unknown")
        
        if self.success:
            self.analysis_text = raw_response.get("analysis", "")
            self._parse_analysis()
        else:
            self.error = raw_response.get("error", "Unknown error")
    
    def _parse_analysis(self):
        """Parse the analysis text and extract structured data."""
        try:
            # Try to parse as JSON first
            if self.analysis_text.strip().startswith('{'):
                self.structured_data = json.loads(self.analysis_text)
            else:
                # If not JSON, create structured data from text
                self.structured_data = {
                    "raw_analysis": self.analysis_text,
                    "summary": self._extract_summary()
                }
        except json.JSONDecodeError:
            self.structured_data = {
                "raw_analysis": self.analysis_text,
                "summary": self._extract_summary()
            }
    
    def _extract_summary(self) -> str:
        """Extract a brief summary from the analysis text."""
        lines = self.analysis_text.split('\n')
        summary_lines = []
        
        for line in lines[:5]:  # Take first 5 lines
            line = line.strip()
            if line and not line.startswith('#'):
                summary_lines.append(line)
        
        return ' '.join(summary_lines)[:200] + "..." if len(' '.join(summary_lines)) > 200 else ' '.join(summary_lines)
    
    def get_plant_type(self) -> Optional[str]:
        """Extract plant type from analysis."""
        if hasattr(self, 'structured_data'):
            return (self.structured_data.get("plant_identification", {}).get("scientific_name") or
                   self.structured_data.get("plant_type") or
                   self.structured_data.get("scientific_name"))
        return None
    
    def get_health_status(self) -> Optional[str]:
        """Extract health status from analysis."""
        if hasattr(self, 'structured_data'):
            return (self.structured_data.get("health_status", {}).get("overall") or
                   self.structured_data.get("health_status") or
                   self.structured_data.get("overall_health"))
        return None
    
    def get_recommendations(self) -> list:
        """Extract recommendations from analysis."""
        if hasattr(self, 'structured_data'):
            recommendations = (self.structured_data.get("recommendations") or
                             self.structured_data.get("care_recommendations", []))
            if isinstance(recommendations, str):
                return [recommendations]
            elif isinstance(recommendations, list):
                return recommendations
        return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        result = {
            "success": self.success,
            "analysis_type": self.analysis_type,
            "model_used": self.model_used
        }
        
        if self.success:
            result.update({
                "analysis_text": self.analysis_text,
                "structured_data": getattr(self, 'structured_data', {}),
                "plant_type": self.get_plant_type(),
                "health_status": self.get_health_status(),
                "recommendations": self.get_recommendations()
            })
        else:
            result["error"] = self.error
        
        return result

class PlantAnalyzer:
    """Main class for analyzing plants from images."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the plant analyzer."""
        config.validate()  # Validate configuration
        
        self.openai_client = OpenAIClient(api_key, base_url)
        self.image_processor = ImageProcessor()
    
    def analyze_plant_image(self, 
                          image_path: str, 
                          analysis_type: str = "complete",
                          enhance_image: bool = True,
                          remove_background: bool = False) -> PlantAnalysisResult:
        """
        Analyze a plant image.
        
        Args:
            image_path: Path to the image file
            analysis_type: Type of analysis ("plant_identification", "disease_detection", 
                         "growth_analysis", "complete")
            enhance_image: Whether to enhance image quality
            remove_background: Whether to attempt background removal
        
        Returns:
            PlantAnalysisResult: Analysis results
        """
        try:
            # Preprocess image
            processed_image = self.image_processor.preprocess_for_analysis(
                image_path=image_path,
                enhance=enhance_image,
                remove_bg=remove_background
            )
            
            # Analyze with OpenAI
            raw_result = self.openai_client.analyze_plant_image(
                image_path_or_pil=processed_image,
                analysis_type=analysis_type
            )
            
            # Add image info to result
            image_info = self.image_processor.get_image_info(processed_image)
            raw_result["image_info"] = image_info
            
            return PlantAnalysisResult(raw_result)
            
        except Exception as e:
            return PlantAnalysisResult({
                "success": False,
                "error": str(e),
                "analysis_type": analysis_type
            })
    
    def analyze_multiple_images(self, 
                              image_paths: list, 
                              analysis_type: str = "complete") -> Dict[str, PlantAnalysisResult]:
        """
        Analyze multiple plant images.
        
        Args:
            image_paths: List of paths to image files
            analysis_type: Type of analysis to perform
        
        Returns:
            Dict mapping image paths to analysis results
        """
        results = {}
        
        for image_path in image_paths:
            try:
                result = self.analyze_plant_image(image_path, analysis_type)
                results[image_path] = result
            except Exception as e:
                results[image_path] = PlantAnalysisResult({
                    "success": False,
                    "error": str(e),
                    "analysis_type": analysis_type
                })
        
        return results
    
    def get_supported_analysis_types(self) -> list:
        """Get list of supported analysis types."""
        return ["plant_identification", "disease_detection", "growth_analysis", "complete"]
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to OpenAI API."""
        try:
            # Try a simple API call
            response = self.openai_client.client.models.list()
            return {
                "success": True,
                "message": "OpenAI API connection successful",
                "available_models": [model.id for model in response.data if "gpt" in model.id][:5]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to connect to OpenAI API"
            }
