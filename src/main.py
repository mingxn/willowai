"""
Command Line Interface for Plant Analysis AI.
"""
import argparse
import sys
import os
from pathlib import Path
from typing import List

# Add src to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent))

from src.core.plant_analyzer import PlantAnalyzer
from src.utils.helpers import (
    save_analysis_result,
    format_analysis_for_display,
    validate_image_path,
    setup_project_directories,
    get_project_info
)
from src.utils.config import config

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="🌿 Plant Analysis AI - Phân tích cây trồng bằng hình ảnh với OpenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python main.py --image photo.jpg --analysis complete
  python main.py --image photo.jpg --analysis disease_detection --save
  python main.py --image photo.jpg --enhance --remove-bg
  python main.py --info
  python main.py --test
        """
    )
    
    # Main arguments
    parser.add_argument(
        "--image", "-i",
        type=str,
        help="Đường dẫn đến file hình ảnh cần phân tích"
    )
    
    parser.add_argument(
        "--analysis", "-a",
        type=str,
        choices=["plant_identification", "disease_detection", "growth_analysis", "complete"],
        default="complete",
        help="Loại phân tích thực hiện (mặc định: complete)"
    )
    
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Lưu kết quả phân tích vào file JSON"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="data/results",
        help="Thư mục lưu kết quả (mặc định: data/results)"
    )
    
    # Image processing options
    parser.add_argument(
        "--enhance",
        action="store_true",
        help="Tăng cường chất lượng hình ảnh trước khi phân tích"
    )
    
    parser.add_argument(
        "--remove-bg",
        action="store_true",
        help="Loại bỏ background khỏi hình ảnh (thử nghiệm)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Hiển thị kết quả chi tiết đầy đủ"
    )
    
    # Utility commands
    parser.add_argument(
        "--test",
        action="store_true",
        help="Kiểm tra kết nối với OpenAI API"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Hiển thị thông tin về project"
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Thiết lập thư mục project"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle utility commands
    if args.info:
        show_project_info()
        return
    
    if args.setup:
        setup_project_directories()
        print("✅ Đã thiết lập thư mục project thành công!")
        return
    
    if args.test:
        test_api_connection()
        return
    
    # Validate main arguments
    if not args.image:
        print("❌ Lỗi: Vui lòng cung cấp đường dẫn hình ảnh với --image")
        parser.print_help()
        return
    
    if not validate_image_path(args.image):
        print(f"❌ Lỗi: File hình ảnh không tồn tại hoặc định dạng không được hỗ trợ: {args.image}")
        return
    
    # Perform analysis
    analyze_image(args)

def show_project_info():
    """Display project information."""
    info = get_project_info()
    
    print("🌿 PLANT ANALYSIS AI")
    print("=" * 50)
    print(f"Tên project: {info['project_name']}")
    print(f"Phiên bản: {info['version']}")
    print(f"Mô tả: {info['description']}")
    print(f"Python yêu cầu: {info['python_version']}")
    
    print(f"\n📦 Dependencies chính:")
    for dep in info['main_dependencies']:
        print(f"  - {dep}")
    
    print(f"\n🔍 Loại phân tích hỗ trợ:")
    for analysis_type in info['supported_analysis_types']:
        print(f"  - {analysis_type}")
    
    print(f"\n🖼️ Định dạng hình ảnh hỗ trợ:")
    for fmt in info['supported_image_formats']:
        print(f"  - {fmt}")

def test_api_connection():
    """Test OpenAI API connection."""
    print("🔄 Đang kiểm tra kết nối OpenAI API...")
    
    try:
        analyzer = PlantAnalyzer()
        result = analyzer.test_connection()
        
        if result["success"]:
            print("✅ Kết nối thành công!")
            print(f"💬 {result['message']}")
            if "available_models" in result:
                print(f"🤖 Một số model khả dụng: {', '.join(result['available_models'])}")
        else:
            print("❌ Kết nối thất bại!")
            print(f"🚫 Lỗi: {result['error']}")
            print("💡 Kiểm tra lại OPENAI_API_KEY trong file .env")
            
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra kết nối: {str(e)}")

def analyze_image(args):
    """Analyze the provided image."""
    print(f"🔄 Đang phân tích hình ảnh: {args.image}")
    print(f"📊 Loại phân tích: {args.analysis}")
    
    if args.enhance:
        print("✨ Sử dụng tăng cường chất lượng hình ảnh")
    
    if args.remove_bg:
        print("🎭 Sử dụng loại bỏ background (thử nghiệm)")
    
    try:
        # Initialize analyzer
        analyzer = PlantAnalyzer()
        
        # Perform analysis
        result = analyzer.analyze_plant_image(
            image_path=args.image,
            analysis_type=args.analysis,
            enhance_image=args.enhance,
            remove_background=args.remove_bg
        )
        
        # Display results
        if result.success:
            print("\n" + "=" * 60)
            
            if args.verbose:
                # Show detailed raw analysis
                print("📋 PHÂN TÍCH CHI TIẾT ĐẦY ĐỦ:")
                print("=" * 60)
                analysis_text = result.analysis_text
                if analysis_text:
                    # Clean up and display the text
                    clean_text = analysis_text.replace("```json", "").replace("```", "").strip()
                    print(clean_text)
                print("=" * 60)
            
            # Show formatted display
            formatted_result = format_analysis_for_display(result.to_dict())
            print(formatted_result)
            print("=" * 60)
            
            # Save results if requested
            if args.save:
                filepath = save_analysis_result(result.to_dict(), args.output)
                print(f"\n💾 Kết quả đã được lưu vào: {filepath}")
                
        else:
            print(f"\n❌ Phân tích thất bại: {result.error}")
            
    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình phân tích: {str(e)}")

if __name__ == "__main__":
    main()
