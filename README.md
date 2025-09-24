# DataMuse - Chart Recommender System

**Transform your data into beautiful visualizations with intelligent chart recommendations**

DataMuse is a smart web application that analyzes your data and automatically suggests the most appropriate chart types based on your column selections. Upload your data, select columns, and let DataMuse guide you to the perfect visualization with real-time chart generation and download capabilities.

![DataMuse Banner](static/images/banner.png)

### 🎯 Smart Chart Recommendations
- **Intelligent Analysis**: Automatically detects column types (numeric, categorical, datetime)
- **Context-Aware Suggestions**: Recommends charts based on data types and combinations
- **Multiple Chart Types**: Supports 9+ different visualization types

### 📈 Supported Visualizations

| Chart Type | Best For | Column Requirements |
|------------|----------|-------------------|
| **Histogram** | Distribution of numeric data | 1 Numeric column |
| **Box Plot (Single)** | Statistical summary of numeric data | 1 Numeric column |
| **Count Plot** | Frequency of categories | 1 Categorical column |
| **Pie Chart** | Proportion of categories | 1 Categorical column |
| **Scatter Plot** | Relationship between two numeric variables | 2 Numeric columns |
| **Line Plot (Time-Series)** | Trends over time | 1 Datetime + 1 Numeric column |
| **Bar Plot (by Value)** | Comparison across categories | 1 Categorical + 1 Numeric column |
| **Box Plot (by Category)** | Distribution comparison across groups | 1 Categorical + 1 Numeric column |
| **Correlation Heatmap** | Relationships between all numeric variables | 2+ Numeric columns |

### 🎨 User Experience
- **Combined Interface**: Single-page design with split-screen layout (chart display + controls)
- **Real-time Chart Generation**: AJAX-powered instant chart updates without page refresh
- **One-Click Download**: Download high-quality PNG charts with smart filename generation
- **Modern UI**: Beautiful gradient design with glass morphism effects
- **Loading Animations**: Smooth animations using Anime.js with elegant loading screen
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Live Feedback**: Real-time chart type suggestions as you select columns
- **Customizable Display**: Adjustable X and Y axis label rotation for better readability
- **Network Ready**: Production configuration accessible from any device on your network

### 📁 File Support
- **CSV Files** (`.csv`)
- **Excel Files** (`.xlsx`, `.xls`)
- **Smart Data Type Detection**: Automatically identifies and converts datetime columns

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "DataMuse - Chart Recommender System"
   ```

2. **Install dependencies**
   ```bash
   pip install flask pandas matplotlib seaborn openpyxl
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - **Local access**: Navigate to `http://localhost:5000`
   - **Network access**: Navigate to `http://[your-ip-address]:5000` from any device on your network

## 🎯 How to Use

### Step 1: Upload Your Data
- Visit the homepage with an informative welcome section explaining DataMuse capabilities
- Click "Upload and Analyze" and select a CSV or Excel file from your computer
- Enjoy the elegant loading screen animation while your data is processed
- Supported formats: `.csv`, `.xlsx`, `.xls`

### Step 2: Generate Charts (Combined Interface)
- **Left Panel**: View your chart visualization in a large, high-quality display area
- **Right Panel**: Configure your chart settings with intuitive controls
- Choose your primary column (X-axis) from the dropdown menu
- Optionally select a second column (Y-axis) for relationships and comparisons
- DataMuse automatically detects column types (numeric, categorical, datetime)

### Step 3: Smart Recommendations & Customization
- View intelligent chart type recommendations based on your column selections
- Select your preferred chart type from the context-aware suggestions
- Customize axis label rotation (0°, 45°, 90°) for optimal readability
- See live previews as you make changes

### Step 4: Generate & Download
- Click "Generate Chart" to create your visualization instantly via AJAX
- View your beautiful, high-resolution chart (14x10 size, 200 DPI) in real-time
- Download your chart with one click using smart filename generation
- Filenames include column names and chart type (e.g., `datamuse_sales_vs_region_bar_plot.png`)

## 🏗️ Project Structure

```
DataMuse - Chart Recommendation System/
├── app.py                    # Main Flask application with AJAX endpoints
├── requirements.txt          # Python dependencies
├── sample_data.csv          # Example dataset for testing
├── static/
│   ├── charts/              # Generated high-resolution chart images
│   └── images/
│       ├── DATAMUSE.png     # Logo and branding
│       └── banner.png       # Project banner image
├── templates/
│   ├── upload.html          # File upload page with welcome section
│   └── generate_chart.html  # Combined chart interface (split-screen)
├── uploads/                 # User uploaded data files
└── README.md               # Project documentation
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Lightweight Python web framework with AJAX endpoint support
- **pandas**: Advanced data manipulation and automatic type detection
- **matplotlib**: High-resolution chart generation (200 DPI, 14x10 size)
- **seaborn**: Statistical data visualization with professional styling
- **numpy**: Numerical computing support

### Frontend
- **HTML5 & CSS3**: Modern semantic markup with responsive grid layouts
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **Anime.js**: Smooth JavaScript animation library for loading screens
- **AJAX/Fetch API**: Real-time chart generation without page refresh
- **Glass Morphism**: Modern UI design with backdrop blur effects

### Data Processing
- **openpyxl**: Excel file processing (.xlsx, .xls support)
- **Smart Type Detection**: Automatic datetime conversion with error handling
- **File Validation**: Comprehensive upload validation and error messages
- **Dynamic Column Analysis**: Real-time data type detection and categorization

## 🎨 Design Philosophy

DataMuse embraces a **"data-first"** approach to visualization with modern UX principles:

1. **Intelligent Automation**: The system analyzes your data structure and suggests the most appropriate visualizations automatically
2. **Split-Screen Efficiency**: Combined interface shows both chart generation controls and live visualization results
3. **Real-time Feedback**: Instant chart generation with AJAX eliminates wait times and page refreshes
4. **Progressive Enhancement**: Start with simple column selection, get sophisticated chart recommendations with one-click download
5. **Visual Clarity**: Clean, modern interface with glass morphism effects that enhance rather than distract from data insights
6. **Accessibility First**: Responsive design with smooth animations that works seamlessly across devices and screen sizes

## ⚙️ Technical Features

### AJAX-Powered Real-time Generation
- **Endpoint**: `/generate_chart_ajax` for asynchronous chart creation
- **JSON Response**: Returns chart URLs and success status
- **Error Handling**: Comprehensive error messages and validation
- **No Page Refresh**: Seamless user experience with instant updates

### Smart Download System
- **Dynamic Filenames**: Automatically generated based on columns and chart type
- **High Resolution**: 200 DPI PNG output for professional use
- **Browser Compatible**: Uses HTML5 download attribute for universal support
- **One-Click Process**: No additional dialogs or complicated steps

### Enhanced Data Processing
- **Automatic Type Detection**: Smart conversion of datetime columns with error handling
- **Multi-format Support**: CSV, XLS, and XLSX file processing
- **Column Analysis**: Real-time categorization into numeric, categorical, and datetime types
- **Error Recovery**: Graceful handling of malformed data with user feedback

## 🔧 Configuration

### Application Settings
The application uses the following default configurations:
- `UPLOAD_FOLDER`: `uploads/` (where uploaded files are stored)
- `CHART_FOLDER`: `static/charts/` (where generated charts are saved)
- `DEBUG`: `False` (production-ready configuration)
- `HOST`: `0.0.0.0` (accessible from any network interface)
- `PORT`: `5000` (default Flask port)
- `CHART_DPI`: `200` (high-resolution output)
- `CHART_SIZE`: `(14, 10)` (professional dimensions)

### Customization Options
- **Chart Styling**: Modify seaborn themes and matplotlib parameters in `app.py`
- **Chart Quality**: Adjust DPI (currently 200) and figure size (currently 14x10) for different output requirements
- **UI Colors**: Update Tailwind classes in HTML templates for custom branding
- **File Size Limits**: Configure Flask upload limits in application configuration
- **Animation Speed**: Modify Anime.js timing parameters for different animation preferences
- **Download Filenames**: Customize the smart filename generation logic in JavaScript

## 🤝 Contributing

We welcome contributions! Here are some ways you can help:

- 🐛 **Bug Reports**: Found an issue? Open a GitHub issue
- 💡 **Feature Requests**: Have an idea? We'd love to hear it
- 🔧 **Pull Requests**: Code improvements and new features
- 📖 **Documentation**: Help improve our docs

## 🙏 Acknowledgments

- **matplotlib** and **seaborn** communities for excellent visualization libraries
- **Flask** team for the lightweight web framework
- **Tailwind CSS** for the utility-first CSS framework
- **Anime.js** for smooth animations

---

**Made with ❤️ for data enthusiasts**

Transform your numbers into insights with DataMuse - where data meets visual clarity.
