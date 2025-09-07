# Deploying JobRight Scraper to Render

## Prerequisites
- GitHub repository with your code
- Google Service Account JSON credentials
- Render account (free tier works)

## Deployment Steps

### 1. Prepare Your Repository
Make sure your GitHub repository contains these essential files:
- `app.py` (main Flask application)
- `enhanced_scraper_with_credentials.py` (scraper logic)
- `requirements.txt` (Python dependencies)
- `render.yaml` (Render configuration)
- `start.sh` (startup script)

### 2. Create Render Web Service

1. **Log into Render**: Go to [render.com](https://render.com) and sign in
2. **Connect GitHub**: Link your GitHub account if not already connected
3. **Create New Web Service**: 
   - Click "New" → "Web Service"
   - Connect your repository: `ajuraforce/Scrapper`
   - Choose the branch (usually `main`)

### 3. Configure Service Settings

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 app:app`
- **Instance Type**: `Free` (sufficient for this application)

### 4. Set Environment Variables

In the Render dashboard, add these environment variables:

**Required:**
- `GOOGLE_SERVICE_ACCOUNT_JSON`: Your complete Google Service Account JSON
  ```json
  {"type":"service_account","project_id":"sheets-autoexpor",...}
  ```

**Optional (if using GitHub features):**
- `GITHUB_OWNER`: Your GitHub username
- `GITHUB_REPO`: Repository name
- `GITHUB_TOKEN`: GitHub personal access token

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your application with Gunicorn
3. Monitor the deployment logs for any issues

### 6. Access Your Application

- Your app will be available at: `https://your-service-name.onrender.com`
- The web interface will load with the job scraping dashboard
- Test the Google Sheets integration to ensure credentials work

## Important Notes

### Google Service Account Setup
1. The JSON credentials must be stored as a single environment variable
2. Make sure your Google Sheet is shared with the service account email
3. Grant "Editor" permissions to the service account

### Free Tier Limitations
- Render free tier may sleep after 15 minutes of inactivity
- First request after sleep may take 30+ seconds to respond
- Consider upgrading to paid tier for production use

### Troubleshooting

**Common Issues:**
- **503 Service Unavailable**: Usually means the app is starting up (wait 30-60 seconds)
- **Google Sheets Authentication Error**: Check that `GOOGLE_SERVICE_ACCOUNT_JSON` is properly set
- **Build Failures**: Verify `requirements.txt` has correct package versions

**Checking Logs:**
- Go to Render dashboard → Your service → "Logs" tab
- Monitor for any Python errors or authentication issues

### Security
- Never commit `credentials.json` to your repository
- Use environment variables for all sensitive data
- The `.gitignore` file already excludes sensitive files

## Files Needed for Deployment

Your repository should contain:
- `app.py` - Flask web application
- `enhanced_scraper_with_credentials.py` - Scraping logic
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration
- `start.sh` - Startup script (optional)
- `.gitignore` - Security exclusions
- `README.md` - Documentation

The application will be fully functional on Render with the same features as your local version!