"""
FastAPI application for Plant Analysis AI.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
import tempfile
import os
import sys
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(src_dir.parent))

from src.core.plant_analyzer import PlantAnalyzer
from src.utils.helpers import save_analysis_result, get_project_info
from src.utils.config import config

# Create FastAPI app
app = FastAPI(
    title="🌿 Plant Analysis AI API",
    description="API cho phân tích cây trồng bằng hình ảnh sử dụng OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance
analyzer = None

@app.on_event("startup")
async def startup_event():
    """Initialize the analyzer on startup."""
    global analyzer
    try:
        analyzer = PlantAnalyzer()
        print("✅ Plant Analyzer initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Plant Analyzer: {e}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    info = get_project_info()
    return {
        "message": "🌿 Welcome to Plant Analysis AI API",
        "project": info["project_name"],
        "version": info["version"],
        "description": info["description"],
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

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global analyzer
    
    if analyzer is None:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": "Analyzer not initialized"}
        )
    
    try:
        # Test API connection
        test_result = analyzer.test_connection()
        
        if test_result["success"]:
            return {
                "status": "healthy",
                "message": "API is running and OpenAI connection is working",
                "openai_status": "connected"
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "degraded", 
                    "message": "API is running but OpenAI connection failed",
                    "openai_status": "disconnected",
                    "error": test_result.get("error")
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}"
            }
        )

@app.get("/info")
async def get_info():
    """Get project and API information."""
    return get_project_info()

@app.post("/analyze/complete")
async def analyze_complete(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    enhance_image: bool = Form(True),
    remove_background: bool = Form(False),
    save_result: bool = Form(False)
):
    """Perform complete plant analysis."""
    return await _analyze_image(
        file=file,
        analysis_type="complete",
        enhance_image=enhance_image,
        remove_background=remove_background,
        save_result=save_result,
        background_tasks=background_tasks
    )

@app.post("/analyze/plant")
async def analyze_plant_identification(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    enhance_image: bool = Form(True),
    remove_background: bool = Form(False),
    save_result: bool = Form(False)
):
    """Perform plant identification analysis."""
    return await _analyze_image(
        file=file,
        analysis_type="plant_identification",
        enhance_image=enhance_image,
        remove_background=remove_background,
        save_result=save_result,
        background_tasks=background_tasks
    )

@app.post("/analyze/disease")
async def analyze_disease_detection(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    enhance_image: bool = Form(True),
    remove_background: bool = Form(False),
    save_result: bool = Form(False)
):
    """Perform disease detection analysis."""
    return await _analyze_image(
        file=file,
        analysis_type="disease_detection",
        enhance_image=enhance_image,
        remove_background=remove_background,
        save_result=save_result,
        background_tasks=background_tasks
    )

@app.post("/analyze/growth")
async def analyze_growth_analysis(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    enhance_image: bool = Form(True),
    remove_background: bool = Form(False),
    save_result: bool = Form(False)
):
    """Perform growth analysis."""
    return await _analyze_image(
        file=file,
        analysis_type="growth_analysis",
        enhance_image=enhance_image,
        remove_background=remove_background,
        save_result=save_result,
        background_tasks=background_tasks
    )

async def _analyze_image(
    file: UploadFile,
    analysis_type: str,
    enhance_image: bool,
    remove_background: bool,
    save_result: bool,
    background_tasks: BackgroundTasks
) -> dict:
    """Internal function to analyze images."""
    global analyzer
    
    if analyzer is None:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format. Allowed: {allowed_extensions}"
        )
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Perform analysis
        result = analyzer.analyze_plant_image(
            image_path=temp_file_path,
            analysis_type=analysis_type,
            enhance_image=enhance_image,
            remove_background=remove_background
        )
        
        response_data = result.to_dict()
        
        # Add request metadata
        response_data["request_metadata"] = {
            "filename": file.filename,
            "file_size": len(content),
            "analysis_type": analysis_type,
            "enhance_image": enhance_image,
            "remove_background": remove_background
        }
        
        # Save result if requested
        if save_result and result.success:
            background_tasks.add_task(
                save_analysis_result,
                response_data,
                "data/results"
            )
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file_path)
        except:
            pass

@app.post("/analyze/batch")
async def analyze_batch(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    analysis_type: str = Form("complete"),
    enhance_image: bool = Form(True),
    remove_background: bool = Form(False),
    save_results: bool = Form(False)
):
    """Analyze multiple images in batch."""
    global analyzer
    
    if analyzer is None:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files per batch")
    
    results = {}
    
    for file in files:
        try:
            result = await _analyze_image(
                file=file,
                analysis_type=analysis_type,
                enhance_image=enhance_image,
                remove_background=remove_background,
                save_result=save_results,
                background_tasks=background_tasks
            )
            results[file.filename] = result
            
        except Exception as e:
            results[file.filename] = {
                "success": False,
                "error": str(e),
                "analysis_type": analysis_type
            }
    
    return {
        "batch_results": results,
        "total_files": len(files),
        "successful_analyses": sum(1 for r in results.values() if r.get("success", False)),
        "failed_analyses": sum(1 for r in results.values() if not r.get("success", False))
    }

@app.get("/analysis/types")
async def get_analysis_types():
    """Get supported analysis types."""
    global analyzer
    
    if analyzer is None:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    
    return {
        "supported_types": analyzer.get_supported_analysis_types(),
        "descriptions": {
            "plant_identification": "Nhận dạng loại cây trồng",
            "disease_detection": "Phát hiện bệnh trên cây", 
            "growth_analysis": "Phân tích tình trạng sinh trưởng",
            "complete": "Phân tích toàn diện (bao gồm tất cả)"
        }
    }

# Error handlers
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )

@app.exception_handler(404) 
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found", "message": "Check API documentation at /docs"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
