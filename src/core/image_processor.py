"""
Image processing utilities for plant analysis.
"""
import os
from typing import Tuple, Optional
import cv2
import numpy as np
from PIL import Image, ImageEnhance

try:
    from ..utils.config import config
except ImportError:
    from src.utils.config import config

class ImageProcessor:
    """Handle image preprocessing and enhancement for plant analysis."""
    
    def __init__(self, max_size: int = None):
        """Initialize image processor."""
        self.max_size = max_size or config.MAX_IMAGE_SIZE
    
    def load_image(self, image_path: str) -> Image.Image:
        """Load and validate image file."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Check file extension
        ext = os.path.splitext(image_path)[1].lower().replace('.', '')
        if ext not in config.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {ext}. Supported: {config.SUPPORTED_FORMATS}")
        
        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")
    
    def resize_image(self, image: Image.Image, max_size: Optional[int] = None) -> Image.Image:
        """Resize image while maintaining aspect ratio."""
        max_size = max_size or self.max_size
        
        # Calculate new dimensions
        width, height = image.size
        if max(width, height) <= max_size:
            return image
        
        if width > height:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_height = max_size
            new_width = int((width * max_size) / height)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def enhance_image(self, image: Image.Image, auto_enhance: bool = True) -> Image.Image:
        """Enhance image quality for better analysis."""
        if not auto_enhance:
            return image
        
        enhanced = image.copy()
        
        # Auto-adjust brightness and contrast
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.2)
        
        # Auto-adjust sharpness
        enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        # Auto-adjust color saturation
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        return enhanced
    
    def remove_background(self, image: Image.Image, method: str = "grabcut") -> Image.Image:
        """Remove background from plant image (experimental)."""
        try:
            # Convert PIL to OpenCV
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            if method == "grabcut":
                return self._grabcut_background_removal(opencv_image)
            elif method == "threshold":
                return self._threshold_background_removal(opencv_image)
            else:
                return image
                
        except Exception as e:
            print(f"Background removal failed: {e}")
            return image
    
    def _grabcut_background_removal(self, opencv_image: np.ndarray) -> Image.Image:
        """Use GrabCut algorithm for background removal."""
        height, width = opencv_image.shape[:2]
        
        # Create initial mask
        mask = np.zeros((height, width), np.uint8)
        
        # Define rectangle around the center (assuming plant is in center)
        rect = (width//4, height//4, width//2, height//2)
        
        # Initialize foreground and background models
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # Apply GrabCut
        cv2.grabCut(opencv_image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        
        # Create final mask
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # Apply mask
        result = opencv_image * mask2[:, :, np.newaxis]
        
        # Convert back to PIL
        return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    
    def _threshold_background_removal(self, opencv_image: np.ndarray) -> Image.Image:
        """Use color thresholding for background removal."""
        # Convert to HSV
        hsv = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2HSV)
        
        # Define green color range (for plants)
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([85, 255, 255])
        
        # Create mask
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Apply morphological operations
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Apply mask
        result = cv2.bitwise_and(opencv_image, opencv_image, mask=mask)
        
        # Convert back to PIL
        return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    
    def preprocess_for_analysis(self, image_path: str, enhance: bool = True, remove_bg: bool = False) -> Image.Image:
        """Complete preprocessing pipeline for plant analysis."""
        # Load image
        image = self.load_image(image_path)
        
        # Resize if needed
        image = self.resize_image(image)
        
        # Enhance image quality
        if enhance:
            image = self.enhance_image(image)
        
        # Remove background if requested
        if remove_bg:
            image = self.remove_background(image)
        
        return image
    
    def get_image_info(self, image: Image.Image) -> dict:
        """Get detailed information about the image."""
        return {
            "size": image.size,
            "mode": image.mode,
            "format": image.format,
            "has_transparency": image.mode in ('RGBA', 'LA') or 'transparency' in image.info,
            "estimated_file_size_kb": len(image.tobytes()) // 1024
        }
