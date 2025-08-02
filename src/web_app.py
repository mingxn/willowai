"""
Streamlit Web Application for Plant Analysis AI.
"""
import streamlit as st
import sys
from pathlib import Path
from PIL import Image
import io

# Add src to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent))

from src.core.plant_analyzer import PlantAnalyzer
from src.utils.helpers import (
    save_analysis_result,
    format_analysis_for_display,
    get_project_info
)
from src.utils.config import config

# Page configuration
st.set_page_config(
    page_title="🌿 Plant Analysis AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main Streamlit application."""
    
    # Title and header
    st.title("🌿 Plant Analysis AI")
    st.subheader("Phân tích cây trồng bằng hình ảnh với OpenAI")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Cấu hình")
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Loại phân tích:",
            [
                ("complete", "🔍 Phân tích toàn diện"),
                ("plant_identification", "🌱 Nhận dạng cây"),
                ("disease_detection", "🔬 Phát hiện bệnh"),
                ("growth_analysis", "📈 Phân tích sinh trưởng")
            ],
            format_func=lambda x: x[1]
        )[0]
        
        # Image processing options
        st.subheader("🖼️ Xử lý hình ảnh")
        enhance_image = st.checkbox("Tăng cường chất lượng", value=True)
        remove_background = st.checkbox("Loại bỏ background (thử nghiệm)", value=False)
        
        # API configuration
        st.subheader("🔑 API Configuration")
        api_key_input = st.text_input(
            "OpenAI API Key (tùy chọn):", 
            type="password",
            help="Để trống để sử dụng key từ file .env"
        )
        
        # Test API connection
        if st.button("🧪 Kiểm tra kết nối API"):
            test_api_connection(api_key_input)
        
        # Project info
        if st.button("ℹ️ Thông tin project"):
            show_project_info()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload hình ảnh")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Chọn hình ảnh cây trồng:",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Hỗ trợ định dạng: JPG, JPEG, PNG, WEBP"
        )
        
        # Display uploaded image
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Hình ảnh đã upload", use_column_width=True)
            
            # Image info
            st.write(f"**Kích thước:** {image.size}")
            st.write(f"**Định dạng:** {image.format}")
            st.write(f"**Mode:** {image.mode}")
        
        # Analysis button
        if uploaded_file is not None:
            if st.button("🚀 Bắt đầu phân tích", type="primary"):
                perform_analysis(
                    uploaded_file, 
                    analysis_type, 
                    enhance_image, 
                    remove_background,
                    api_key_input
                )
    
    with col2:
        st.header("📊 Kết quả phân tích")
        
        # Results will be displayed here by perform_analysis function
        if "analysis_result" not in st.session_state:
            st.info("Upload hình ảnh và nhấn 'Bắt đầu phân tích' để xem kết quả.")

def test_api_connection(api_key: str = None):
    """Test OpenAI API connection."""
    with st.spinner("Đang kiểm tra kết nối..."):
        try:
            analyzer = PlantAnalyzer(api_key if api_key else None)
            result = analyzer.test_connection()
            
            if result["success"]:
                st.success("✅ Kết nối thành công!")
                st.info(f"💬 {result['message']}")
                if "available_models" in result:
                    st.write(f"🤖 Một số model khả dụng: {', '.join(result['available_models'])}")
            else:
                st.error("❌ Kết nối thất bại!")
                st.error(f"🚫 Lỗi: {result['error']}")
                st.warning("💡 Kiểm tra lại OPENAI_API_KEY trong file .env hoặc nhập API key ở sidebar")
                
        except Exception as e:
            st.error(f"❌ Lỗi khi kiểm tra kết nối: {str(e)}")

def show_project_info():
    """Display project information."""
    info = get_project_info()
    
    st.success("📋 Thông tin Project")
    
    st.write(f"**Tên:** {info['project_name']}")
    st.write(f"**Phiên bản:** {info['version']}")
    st.write(f"**Mô tả:** {info['description']}")
    st.write(f"**Python yêu cầu:** {info['python_version']}")
    
    st.write("**📦 Dependencies chính:**")
    for dep in info['main_dependencies'][:5]:  # Show first 5
        st.write(f"- {dep}")
    
    st.write("**🔍 Loại phân tích hỗ trợ:**")
    for analysis_type in info['supported_analysis_types']:
        st.write(f"- {analysis_type}")

def perform_analysis(uploaded_file, analysis_type, enhance_image, remove_background, api_key):
    """Perform plant analysis on uploaded image."""
    
    with st.spinner(f"Đang thực hiện {analysis_type}..."):
        try:
            # Convert uploaded file to PIL Image
            image = Image.open(uploaded_file)
            
            # Initialize analyzer
            analyzer = PlantAnalyzer(api_key if api_key else None)
            
            # Perform analysis using PIL Image directly
            result = analyzer.analyze_plant_image(
                image_path=image,  # Pass PIL Image directly
                analysis_type=analysis_type,
                enhance_image=enhance_image,
                remove_background=remove_background
            )
            
            # Store result in session state
            st.session_state.analysis_result = result
            
            # Display results
            display_analysis_results(result)
            
        except Exception as e:
            st.error(f"❌ Lỗi trong quá trình phân tích: {str(e)}")

def display_analysis_results(result):
    """Display analysis results in the UI."""
    
    if result.success:
        st.success("✅ Phân tích hoàn thành!")
        
        # Display formatted results
        result_dict = result.to_dict()
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Tóm tắt", "🔍 Chi tiết", "📄 JSON"])
        
        with tab1:
            # Summary view
            st.markdown("### 📊 Kết quả tóm tắt")
            
            # Plant type
            plant_type = result.get_plant_type()
            if plant_type:
                st.info(f"🌱 **Loại cây:** {plant_type}")
            
            # Health status
            health_status = result.get_health_status()
            if health_status:
                if "khỏe" in health_status.lower() or "healthy" in health_status.lower():
                    st.success(f"💚 **Tình trạng sức khỏe:** {health_status}")
                else:
                    st.warning(f"⚠️ **Tình trạng sức khỏe:** {health_status}")
            
            # Recommendations
            recommendations = result.get_recommendations()
            if recommendations:
                st.markdown("### 💡 Khuyến nghị:")
                for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
                    st.write(f"{i}. {rec}")
        
        with tab2:
            # Detailed view
            st.markdown("### 🔍 Phân tích chi tiết")
            st.text(result.analysis_text)
        
        with tab3:
            # JSON view
            st.markdown("### 📄 Dữ liệu JSON")
            st.json(result_dict)
        
        # Download options
        st.markdown("### 💾 Tải xuống kết quả")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as JSON
            json_str = str(result_dict)
            st.download_button(
                label="📄 Tải JSON",
                data=json_str,
                file_name=f"plant_analysis_{result.analysis_type}.json",
                mime="application/json"
            )
        
        with col2:
            # Download as text
            text_result = format_analysis_for_display(result_dict)
            st.download_button(
                label="📝 Tải Text",
                data=text_result,
                file_name=f"plant_analysis_{result.analysis_type}.txt",
                mime="text/plain"
            )
        
    else:
        st.error("❌ Phân tích thất bại!")
        st.error(f"🚫 Lỗi: {result.error}")

def modify_openai_client():
    """Modify the OpenAI client to work with uploaded images."""
    # This is a patch to make the analyzer work with uploaded files
    from core.openai_client import OpenAIClient
    
    original_analyze = OpenAIClient.analyze_plant_image
    
    def patched_analyze(self, image_path_or_pil, analysis_type="complete"):
        if hasattr(image_path_or_pil, 'read'):  # It's a file-like object
            # Convert to PIL Image
            image = Image.open(image_path_or_pil)
            return original_analyze(self, image, analysis_type)
        else:
            return original_analyze(self, image_path_or_pil, analysis_type)
    
    OpenAIClient.analyze_plant_image = patched_analyze

# Apply the patch
modify_openai_client()

if __name__ == "__main__":
    main()
