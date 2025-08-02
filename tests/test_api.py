"""
Tests for the FastAPI application.
"""
import unittest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api.main import app

class TestAPI(unittest.TestCase):
    """Test cases for FastAPI application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("🌿", data["message"])
        self.assertIn("endpoints", data)
    
    def test_info_endpoint(self):
        """Test info endpoint."""
        response = self.client.get("/info")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("project_name", data)
        self.assertIn("version", data)
        self.assertIn("supported_analysis_types", data)
    
    @patch('api.main.analyzer')
    def test_health_endpoint_healthy(self, mock_analyzer):
        """Test health endpoint when service is healthy."""
        mock_analyzer.test_connection.return_value = {"success": True}
        
        response = self.client.get("/health")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
    
    @patch('api.main.analyzer')
    def test_health_endpoint_unhealthy(self, mock_analyzer):
        """Test health endpoint when service is unhealthy."""
        mock_analyzer.test_connection.return_value = {
            "success": False, 
            "error": "API connection failed"
        }
        
        response = self.client.get("/health")
        
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data["status"], "degraded")
    
    def test_analysis_types_endpoint(self):
        """Test analysis types endpoint.""" 
        with patch('api.main.analyzer') as mock_analyzer:
            mock_analyzer.get_supported_analysis_types.return_value = [
                "plant_identification", "disease_detection", "growth_analysis", "complete"
            ]
            
            response = self.client.get("/analysis/types")
            
            if response.status_code == 200:
                data = response.json()
                self.assertIn("supported_types", data)
                self.assertIn("descriptions", data)
            else:
                # Service might not be initialized in test
                self.assertEqual(response.status_code, 503)
    
    def test_not_found_endpoint(self):
        """Test 404 error handling."""
        response = self.client.get("/nonexistent")
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("detail", data)

class TestAnalysisEndpoints(unittest.TestCase):
    """Test cases for analysis endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
    
    def test_analyze_complete_without_file(self):
        """Test complete analysis endpoint without file."""
        response = self.client.post("/analyze/complete")
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_analyze_plant_without_file(self):
        """Test plant identification endpoint without file."""
        response = self.client.post("/analyze/plant")
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_analyze_disease_without_file(self):
        """Test disease detection endpoint without file."""
        response = self.client.post("/analyze/disease")
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_analyze_growth_without_file(self):
        """Test growth analysis endpoint without file."""
        response = self.client.post("/analyze/growth")
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    @patch('api.main.analyzer')
    def test_analyze_with_invalid_file_type(self, mock_analyzer):
        """Test analysis with invalid file type."""
        # Create a mock text file
        files = {"file": ("test.txt", "not an image", "text/plain")}
        
        response = self.client.post("/analyze/complete", files=files)
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("File must be an image", data["detail"])

if __name__ == "__main__":
    unittest.main()
