<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Plant Analysis AI - Copilot Instructions

## Project Overview
This is a Python project for plant analysis using images with OpenAI Vision API. The application can identify plants, detect diseases, analyze growth status, and provide care recommendations.

## Key Technologies
- **Python 3.8+**
- **OpenAI API** (GPT-4 Vision) for image analysis
- **FastAPI** for REST API
- **Streamlit** for web interface
- **PIL/Pillow** for image processing
- **OpenCV** for advanced image processing
- **NumPy** for numerical operations

## Project Structure
- `src/core/` - Core analysis modules (plant_analyzer, openai_client, image_processor)
- `src/api/` - FastAPI application and routes
- `src/models/` - Data models and structures
- `src/utils/` - Configuration and helper functions
- `src/web_app.py` - Streamlit web interface
- `src/main.py` - Command line interface
- `tests/` - Unit tests
- `data/` - Sample images and results storage

## Coding Guidelines

### General Principles
- Use type hints for all function parameters and return values
- Write comprehensive docstrings for all classes and functions
- Follow PEP 8 style guidelines
- Use Vietnamese comments and messages for user-facing text
- Use English for code comments and documentation

### Error Handling
- Always use try-catch blocks for API calls and file operations
- Provide meaningful error messages in Vietnamese for users
- Log errors appropriately for debugging
- Return structured error responses with success/failure status

### Image Processing
- Always validate image formats before processing
- Use PIL for basic image operations
- Use OpenCV for advanced processing (background removal, enhancement)
- Resize images to reasonable dimensions before API calls
- Handle both file paths and PIL Image objects

### OpenAI API Integration
- Always check for API key presence before making calls
- Use proper error handling for API failures
- Structure prompts in Vietnamese for better analysis results
- Parse responses robustly (handle both JSON and text responses)
- Include confidence levels and metadata in responses

### Data Models
- Use dataclasses for structured data representation
- Provide conversion methods (to_dict, from_dict)
- Include proper validation for data fields
- Use Optional types for nullable fields

### API Design
- Use FastAPI for REST endpoints
- Include proper request/response models
- Implement file upload handling with validation
- Provide comprehensive error responses
- Include request metadata in responses
- Support batch operations where appropriate

### Web Interface
- Use Streamlit for interactive web UI
- Provide clear instructions and help text in Vietnamese
- Show progress indicators for long operations
- Allow file downloads of analysis results
- Display results in multiple formats (summary, detailed, JSON)

### Testing
- Write unit tests for all core functionality
- Mock external API calls in tests
- Test error conditions and edge cases
- Include integration tests for API endpoints
- Test file upload and processing workflows

### Configuration
- Use environment variables for sensitive data (API keys)
- Provide example configuration files
- Validate configuration on startup
- Support different analysis modes and parameters

## Common Patterns

### Analysis Result Structure
```python
{
    "success": bool,
    "analysis_type": str,
    "model_used": str,
    "analysis_text": str,
    "structured_data": dict,
    "plant_type": Optional[str],
    "health_status": Optional[str], 
    "recommendations": List[str],
    "error": Optional[str]
}
```

### Error Response Structure
```python
{
    "success": False,
    "error": "Error message in Vietnamese",
    "error_code": "ERROR_CODE",
    "details": "Additional details for debugging"
}
```

### File Processing Pattern
```python
try:
    # Load and validate image
    image = image_processor.load_image(path)
    # Process image
    processed = image_processor.preprocess_for_analysis(image)
    # Analyze with AI
    result = analyzer.analyze_plant_image(processed)
    return result
except Exception as e:
    return error_response(str(e))
```

## Special Considerations
- This application deals with agricultural and botanical content
- Analysis prompts should be in Vietnamese for better results with Vietnamese plants
- Consider seasonal variations and regional plant varieties
- Provide practical care recommendations suitable for Vietnamese climate
- Support common Vietnamese plant names alongside scientific names
- Handle low-quality or unclear images gracefully
- Provide confidence levels for all identifications and recommendations
