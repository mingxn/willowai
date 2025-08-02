"""
Tests for the plant analyzer core functionality.
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.plant_analyzer import PlantAnalyzer, PlantAnalysisResult
from core.image_processor import ImageProcessor
from core.openai_client import OpenAIClient

class TestPlantAnalyzer(unittest.TestCase):
    """Test cases for PlantAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_key = "test-api-key"
    
    @patch('core.plant_analyzer.config')
    def test_analyzer_initialization(self, mock_config):
        """Test analyzer initialization."""
        mock_config.validate.return_value = True
        
        analyzer = PlantAnalyzer(self.mock_api_key)
        
        self.assertIsInstance(analyzer, PlantAnalyzer)
        self.assertIsInstance(analyzer.openai_client, OpenAIClient)
        self.assertIsInstance(analyzer.image_processor, ImageProcessor)
    
    def test_supported_analysis_types(self):
        """Test getting supported analysis types."""
        with patch('core.plant_analyzer.config') as mock_config:
            mock_config.validate.return_value = True
            
            analyzer = PlantAnalyzer(self.mock_api_key)
            types = analyzer.get_supported_analysis_types()
            
            expected_types = ["plant_identification", "disease_detection", "growth_analysis", "complete"]
            self.assertEqual(types, expected_types)

class TestPlantAnalysisResult(unittest.TestCase):
    """Test cases for PlantAnalysisResult class."""
    
    def test_successful_result_creation(self):
        """Test creating a successful analysis result."""
        raw_response = {
            "success": True,
            "analysis": "Test analysis text",
            "analysis_type": "complete",
            "model_used": "gpt-4-vision-preview"
        }
        
        result = PlantAnalysisResult(raw_response)
        
        self.assertTrue(result.success)
        self.assertEqual(result.analysis_type, "complete")
        self.assertEqual(result.model_used, "gpt-4-vision-preview")
        self.assertEqual(result.analysis_text, "Test analysis text")
    
    def test_failed_result_creation(self):
        """Test creating a failed analysis result."""
        raw_response = {
            "success": False,
            "error": "Test error message",
            "analysis_type": "complete"
        }
        
        result = PlantAnalysisResult(raw_response)
        
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Test error message")
        self.assertEqual(result.analysis_type, "complete")
    
    def test_to_dict_conversion(self):
        """Test converting result to dictionary."""
        raw_response = {
            "success": True,
            "analysis": "Test analysis",
            "analysis_type": "plant_identification",
            "model_used": "gpt-4"
        }
        
        result = PlantAnalysisResult(raw_response)
        result_dict = result.to_dict()
        
        self.assertIsInstance(result_dict, dict)
        self.assertTrue(result_dict["success"])
        self.assertEqual(result_dict["analysis_type"], "plant_identification")

class TestImageProcessor(unittest.TestCase):
    """Test cases for ImageProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = ImageProcessor()
    
    def test_processor_initialization(self):
        """Test image processor initialization."""
        self.assertIsInstance(self.processor, ImageProcessor)
        self.assertIsInstance(self.processor.max_size, int)
        self.assertGreater(self.processor.max_size, 0)
    
    def test_get_image_info(self):
        """Test getting image information."""
        # Mock PIL Image
        with patch('PIL.Image.Image') as mock_image:
            mock_image.size = (800, 600)
            mock_image.mode = "RGB"
            mock_image.format = "JPEG"
            mock_image.tobytes.return_value = b"test_bytes"
            
            info = self.processor.get_image_info(mock_image)
            
            self.assertIsInstance(info, dict)
            self.assertIn("size", info)
            self.assertIn("mode", info)
            self.assertIn("format", info)

class TestOpenAIClient(unittest.TestCase):
    """Test cases for OpenAIClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_key = "test-api-key"
    
    @patch('core.openai_client.openai.OpenAI')
    def test_client_initialization(self, mock_openai):
        """Test OpenAI client initialization."""
        client = OpenAIClient(self.mock_api_key)
        
        self.assertIsInstance(client, OpenAIClient)
        mock_openai.assert_called_once_with(api_key=self.mock_api_key)
    
    def test_prompt_generation(self):
        """Test prompt generation methods."""
        with patch('core.openai_client.openai.OpenAI'):
            client = OpenAIClient(self.mock_api_key)
            
            # Test prompt methods exist and return strings
            plant_prompt = client._get_plant_identification_prompt()
            disease_prompt = client._get_disease_detection_prompt()
            growth_prompt = client._get_growth_analysis_prompt()
            complete_prompt = client._get_complete_analysis_prompt()
            
            self.assertIsInstance(plant_prompt, str)
            self.assertIsInstance(disease_prompt, str)
            self.assertIsInstance(growth_prompt, str)
            self.assertIsInstance(complete_prompt, str)
            
            # Check that prompts contain relevant keywords
            self.assertIn("cây", plant_prompt.lower())
            self.assertIn("bệnh", disease_prompt.lower())
            self.assertIn("sinh trưởng", growth_prompt.lower())
            self.assertIn("toàn diện", complete_prompt.lower())

if __name__ == "__main__":
    unittest.main()
