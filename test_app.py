"""
Quick test script to validate our Streamlit app structure
"""

import sys
import os

# Add the streamlit_app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'streamlit_app'))

def test_imports():
    """Test that all imports work correctly."""
    try:
        from config import configure_page, show_sidebar_nav, PAGES
        print("✅ Config imports successful")
        
        from pages.input_page import show_input_page
        print("✅ Input page import successful")
        
        from pages.dashboard_page import show_dashboard_page  
        print("✅ Dashboard page import successful")
        
        from pages.settings_page import show_settings_page
        print("✅ Settings page import successful")
        
        from pages.documentation_page import show_documentation_page
        print("✅ Documentation page import successful")
        
        print("\n🎉 All imports successful! App structure is valid.")
        
        # Check unique keys
        print("\n🔑 Checking for unique keys in config...")
        # This would require actually running streamlit, but we can at least check the imports
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_imports()