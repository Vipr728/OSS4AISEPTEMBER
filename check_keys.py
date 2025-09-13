"""
Simple test to verify Streamlit app structure without duplicate keys
"""

print("🧪 Testing Streamlit App Structure...")

# Test 1: Check if files exist
import os
files_to_check = [
    "streamlit_app/config.py",
    "streamlit_app/pages/input_page.py", 
    "streamlit_app/pages/dashboard_page.py",
    "streamlit_app/pages/settings_page.py",
    "streamlit_app/pages/documentation_page.py"
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f"✅ {file_path} exists")
    else:
        print(f"❌ {file_path} missing")

# Test 2: Check for unique keys in files
print("\n🔑 Checking for potential duplicate keys...")

def check_file_for_keys(filepath):
    """Check a file for streamlit widget keys."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        keys = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'key=' in line:
                # Extract the key value
                start = line.find('key=') + 4
                end = line.find(')', start)
                if end == -1:
                    end = len(line)
                key_part = line[start:end].strip().strip('"').strip("'")
                keys.append((i+1, key_part))
        
        return keys
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return []

all_keys = {}
for file_path in files_to_check:
    if os.path.exists(file_path):
        keys = check_file_for_keys(file_path)
        for line_num, key in keys:
            if key in all_keys:
                print(f"⚠️  Potential duplicate key '{key}' found in {file_path}:{line_num} and {all_keys[key]}")
            else:
                all_keys[key] = f"{file_path}:{line_num}"
                print(f"✅ Unique key '{key}' in {file_path}")

print(f"\n📊 Summary: Found {len(all_keys)} unique widget keys")
print("🎉 App structure test completed!")