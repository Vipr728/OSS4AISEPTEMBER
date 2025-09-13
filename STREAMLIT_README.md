# 🎯 Social Media Analysis App - Debloated & Streamlined

A **comprehensive yet efficient** single-file Streamlit interface for multi-agent social media analysis.

## ✨ Features Restored & Consolidated

### 📊 **Full Dashboard**
- Interactive sentiment pie charts with Plotly
- Risk assessment gauge visualization  
- Comprehensive metrics display
- Detailed comment-by-comment analysis

### 📝 **Complete Input Methods**
- **Manual Entry**: Direct text area input
- **Demo Scenarios**: Pre-built test cases (Authentic Tech Review, Suspicious Promotional, Mixed Sentiment)
- **CSV Upload**: Bulk import capability

### ⚙️ **Streamlined Configuration**
- Sidebar navigation and API key management
- Session-based secure storage
- Single-click clear results

### 📚 **Built-in Documentation**
- System architecture overview
- Usage instructions and best practices
- Results interpretation guide

## 🎯 Debloating Success

**Before**: 6 separate files, 2,100+ lines of bloated code
**After**: 1 consolidated file, 481 lines (**77% reduction!**)

### What was consolidated:
- ❌ `streamlit_app/pages/input_page.py` (362 lines)
- ❌ `streamlit_app/pages/dashboard_page.py` (429 lines)  
- ❌ `streamlit_app/pages/settings_page.py` (402 lines)
- ❌ `streamlit_app/pages/documentation_page.py` (673 lines)
- ❌ `streamlit_app/config.py` (80 lines)
- ❌ `streamlit_app/demo_data.py` (225 lines)
- ✅ **Single `app.py`** (481 lines) - **All functionality preserved!**

### Benefits achieved:
- 🚀 **Faster loading** - Single file, no complex imports
- 🔧 **Easier maintenance** - All code in one place
- 📦 **Simpler deployment** - Fewer files to manage
- 🎯 **Better organization** - Logical function grouping
- 🔍 **Easier debugging** - Clear code flow

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gemini API key

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Usage
1. **Configure API Key**: Enter your Gemini API key in the sidebar
2. **Choose Input Method**: Manual, Demo scenarios, or CSV upload
3. **Analyze**: Run the multi-agent analysis pipeline
4. **Review Results**: Comprehensive dashboard with visualizations

## 📊 Input Methods

### Manual Entry
Simply paste comments into the text area, one per line:
```
This product is amazing! Really helped me.
I'm not sure if this is worth the price.
Great quality but shipping was slow.
```

### Demo Scenarios
Pre-built test cases:
- **Authentic Tech Review**: Genuine user feedback
- **Suspicious Promotional**: Potential bias indicators  
- **Mixed Sentiment**: Balanced positive/negative mix

### CSV Upload
Upload spreadsheet with comment data:
- Select the column containing comments
- Bulk analyze hundreds of comments
- Download results for further analysis

## 🔍 Understanding Results

### Risk Levels
- 🟢 **Low**: Normal, authentic engagement
- 🟡 **Medium**: Some suspicious patterns detected
- 🔴 **High**: Strong indicators of bias or manipulation

### Bias Signals
- **Brand Affinity**: Commercial relationships detected
- **Promotional Content**: Marketing language, discount codes
- **Account Credibility**: Profile authenticity indicators

### Dashboard Features
- **Sentiment Distribution**: Pie chart of positive/negative/neutral
- **Risk Assessment**: Gauge showing overall threat level
- **Detailed Analysis**: Comment-by-comment breakdown
- **Export Options**: Save results for reporting

## 🏗️ Architecture

The system uses a **multi-agent architecture**:

1. **Main Classifier Agent**: Initial sentiment and toxicity analysis
2. **Summary Agent**: Maintains running statistics and insights
3. **Bias Detection Agent**: Deep analysis of flagged content
4. **Orchestrator**: Coordinates all agents and manages pipeline

## 🤝 Contributing

This is a streamlined, single-file implementation optimized for:
- Minimal complexity
- Maximum functionality
- Easy customization
- Clear code organization

## 📝 License

MIT License - see LICENSE file for details.