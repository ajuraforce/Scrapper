# JobRight Production Scraper

A powerful web-based application for automated job data collection from JobRight.ai with intelligent account rotation, Google Sheets integration, and comprehensive deduplication.

## 🚀 Features

- **Multi-Account Rotation**: Automatically cycles through 3 pre-configured accounts for maximum job diversity
- **Google Sheets Integration**: Exports data to separate sheets (ALL_JOBS and FILTERED_JOBS) with real-time updates
- **Smart Deduplication**: Prevents duplicate jobs across all scraping sessions
- **Keyword Filtering**: Filter jobs by specific keywords with separate filtered results
- **Modern Web Interface**: Clean, responsive dashboard with glassmorphism design
- **Custom Credentials**: Support for user-provided JobRight credentials
- **Production Ready**: Built with Flask and Gunicorn for reliable deployment

## 📋 Prerequisites

- Python 3.11+
- Google Service Account with Sheets API access
- JobRight.ai accounts (3 pre-configured or custom)
- Google Sheet ID for data storage

## 🛠 Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd jobright-scraper
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Google Sheets API

#### Create Service Account:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create a Service Account
5. Download the JSON credentials file
6. Rename it to `credentials.json` and place in project root

#### Share Your Google Sheet:
1. Create a new Google Sheet
2. Copy the Sheet ID from the URL: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
3. Share the sheet with your service account email: `sheetsservice@sheets-autoexpor.iam.gserviceaccount.com`
4. Give it "Editor" permissions

### 4. Environment Setup
```bash
# Set required environment variables (optional - defaults provided)
export GOOGLE_CREDENTIALS=path/to/credentials.json
export SESSION_SECRET=your-secret-key
```

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the Application**:
   ```bash
   python app.py
   ```
   Or for production:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

2. **Access the Dashboard**:
   - Open browser to `http://localhost:5000`
   - The Google Sheet ID is pre-filled with the default sheet
   - Enter keywords to filter jobs (optional)
   - Select job count: 5, 25, 50, or 100
   - Add custom credentials if needed (optional)

3. **Run Scraping**:
   - Click "Start Smart Scraping"
   - Monitor real-time progress
   - View results in your Google Sheet

### Direct Python Usage

```python
from enhanced_scraper_with_credentials import EnhancedJobRightScraper

scraper = EnhancedJobRightScraper()
result = scraper.run_complete_scraper(
    sheet_url='your-google-sheet-id',
    keyword='software engineer',  # Optional
    target_jobs=100
)
```

## 📊 How It Works

### Account Rotation System
- **3 Pre-configured Accounts**: Automatically rotates through saved JobRight accounts
- **Intelligent Switching**: Each run uses a different account for diverse results
- **Custom Credentials**: Override with your own JobRight account if needed

### Data Collection Process
1. **Authentication**: Logs into JobRight using rotated account
2. **Multi-Strategy Scraping**: 
   - Pagination approach (recommended)
   - Diverse keyword searches (Software Engineer, Data Scientist, etc.)
   - Fallback API endpoints
3. **Smart Deduplication**: Removes duplicates across all sessions
4. **Google Sheets Export**: Creates/updates two sheets:
   - `ALL_JOBS`: All scraped jobs
   - `FILTERED_JOBS`: Jobs matching your keyword filter

### Data Structure
Each job record includes:
- Company name and details
- Job title and description
- Location and salary information
- Application link and requirements
- Scraping metadata (account used, timestamp)

## 🔧 Configuration

### Pre-configured Accounts
The system includes 3 JobRight accounts:
- Primary: `mrtandonh@icloud.com`
- Manager: `manage@gmail.com`
- Data: `data@gmail.com`

### Google Sheet Setup
- **Default Sheet ID**: `1iibXYJ5ZSFZzFIKUyM8d4u3x87FOereMESBfuFW7ZYI`
- **Required Permissions**: Editor access for service account
- **Auto-Creation**: Creates ALL_JOBS and FILTERED_JOBS sheets automatically

## 🚀 Deployment

### Replit (Recommended)
1. Import this repository to Replit
2. Add `credentials.json` to the project
3. Configure workflows in `.replit` file
4. Deploy using Replit's hosting

### Manual Deployment
1. Set up Python environment
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run with Gunicorn: `gunicorn --bind 0.0.0.0:5000 main:app`

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## 🛡 Security Features

- **Secure Credential Handling**: Service account authentication
- **Session Management**: Flask sessions with configurable secrets
- **Rate Limiting**: Built-in delays to avoid detection
- **Error Handling**: Comprehensive timeout and retry mechanisms

## 📈 Performance

- **Intelligent Deduplication**: Prevents processing duplicate jobs
- **Account Rotation**: Maximizes job diversity
- **Concurrent Processing**: Efficient multi-strategy scraping
- **Real-time Updates**: Live progress tracking in web interface

## 🔍 Troubleshooting

### Common Issues

1. **Google Sheets Permission Error**:
   - Verify service account email has access to your sheet
   - Check `credentials.json` file is in project root

2. **JobRight Login Failed**:
   - Accounts may need re-authentication
   - Try using custom credentials option

3. **No Jobs Found**:
   - Check internet connection
   - Verify JobRight.ai is accessible
   - Try different keywords or increase job count

### Debug Endpoints
- `/health` - Check server status
- `/debug` - View system information
- Browser console - Check for JavaScript errors

## 📝 API Reference

### Web Endpoints

#### `GET /`
Main dashboard interface

#### `POST /scrape`
Start scraping process
```json
{
  "sheet_url": "google-sheet-id",
  "keyword": "optional-filter",
  "target_jobs": 100,
  "custom_email": "optional",
  "custom_password": "optional"
}
```

#### `GET /health`
Server health check

#### `GET /debug`
System debug information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and personal use. Please respect JobRight.ai's terms of service.

## ⚡ Quick Start

1. **Get Google Sheet ID**: Create a sheet and copy ID from URL
2. **Share with Service Account**: `sheetsservice@sheets-autoexpor.iam.gserviceaccount.com`
3. **Run Application**: `python app.py`
4. **Access Dashboard**: `http://localhost:5000`
5. **Start Scraping**: Fill form and click "Start Smart Scraping"

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review browser console for errors
- Verify Google Sheets permissions
- Test with different browsers or networks

---

**Built with ❤️ for efficient job data collection and analysis**