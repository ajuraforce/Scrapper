from flask import Flask, jsonify, render_template_string, request
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "simple-key-2025"

# Enhanced Modern UI
HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JobRight.ai Professional Scraper</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            pointer-events: none;
            z-index: 1;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            animation: slideDown 0.8s ease;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, #f0f9ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .header p {
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            font-weight: 300;
        }
        
        .main-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
            animation: slideUp 0.8s ease;
            position: relative;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .feature {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease;
        }
        
        .feature:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.15);
        }
        
        .feature i {
            font-size: 2rem;
            color: #10b981;
            margin-bottom: 10px;
        }
        
        .feature h3 {
            color: white;
            font-size: 1.1rem;
            margin-bottom: 8px;
        }
        
        .feature p {
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }
        
        .form-section {
            margin-top: 30px;
        }
        
        .form-group {
            margin-bottom: 25px;
            position: relative;
        }
        
        .form-group label {
            display: block;
            color: white;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        
        .form-group label i {
            margin-right: 8px;
            width: 20px;
        }
        
        .input-wrapper {
            position: relative;
        }
        
        .form-control {
            width: 100%;
            padding: 16px 20px;
            border: 2px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .form-control:focus {
            outline: none;
            border-color: #10b981;
            background: rgba(255,255,255,0.2);
            box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
        }
        
        .form-control::placeholder {
            color: rgba(255,255,255,0.6);
        }
        
        .help-text {
            color: rgba(255,255,255,0.7);
            font-size: 0.85rem;
            margin-top: 6px;
        }
        
        .btn-primary {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            margin-top: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .btn-primary::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn-primary:hover::before {
            left: 100%;
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(16, 185, 129, 0.4);
        }
        
        .btn-primary:active {
            transform: translateY(-1px);
        }
        
        .btn-primary:disabled {
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading-section {
            display: none;
            text-align: center;
            margin-top: 30px;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid #10b981;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        .loading-text {
            color: white;
            font-size: 1.1rem;
            margin-bottom: 10px;
        }
        
        .loading-subtext {
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }
        
        .results-section {
            display: none;
            margin-top: 30px;
            animation: slideUp 0.5s ease;
        }
        
        .success-header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .success-header i {
            font-size: 3rem;
            color: #10b981;
            margin-bottom: 10px;
        }
        
        .success-header h3 {
            color: white;
            font-size: 1.5rem;
            margin-bottom: 5px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .stat-card {
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: scale(1.05);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #10b981;
            display: block;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: white;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .details-section {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .detail-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .detail-item:last-child {
            border-bottom: none;
        }
        
        .detail-label {
            color: rgba(255,255,255,0.8);
            font-weight: 500;
        }
        
        .detail-value {
            color: white;
            font-weight: 600;
            text-align: right;
            max-width: 60%;
            word-break: break-word;
        }
        
        .btn-secondary {
            width: 100%;
            padding: 15px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }
        
        .btn-secondary:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .main-card {
                padding: 25px;
                margin: 10px;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-rocket"></i> JobRight.ai Scraper</h1>
            <p>Professional job data extraction with credential tracking</p>
        </div>
        
        <div class="main-card">
            <div class="features-grid">
                <div class="feature">
                    <i class="fas fa-database"></i>
                    <h3>Real Data</h3>
                    <p>100% authentic JobRight.ai jobs</p>
                </div>
                <div class="feature">
                    <i class="fas fa-table"></i>
                    <h3>Dual Sheets</h3>
                    <p>All jobs + filtered results</p>
                </div>
                <div class="feature">
                    <i class="fas fa-key"></i>
                    <h3>Credentials</h3>
                    <p>Account tracking included</p>
                </div>
                <div class="feature">
                    <i class="fas fa-filter"></i>
                    <h3>Smart Filter</h3>
                    <p>Keyword-based job matching</p>
                </div>
            </div>
            
            <div class="form-section">
                <form id="form">
                    <div class="form-group">
                        <label><i class="fas fa-link"></i> Google Sheet ID</label>
                        <div class="input-wrapper">
                            <input type="text" id="sheet" class="form-control" 
                                   placeholder="1iibXYJ5ZSFZzFIKUyM8d4u3x87FOereMESBfuFW7ZYI" 
                                   value="1iibXYJ5ZSFZzFIKUyM8d4u3x87FOereMESBfuFW7ZYI" required>
                        </div>
                        <div class="help-text">Enter just the Sheet ID (from your Google Sheets URL after '/d/'). Sheet must be shared with: sheetsservice@sheets-autoexpor.iam.gserviceaccount.com</div>
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-search"></i> Filter Keyword</label>
                        <div class="input-wrapper">
                            <input type="text" id="keyword" class="form-control" 
                                   placeholder="e.g., python, frontend, marketing, data scientist">
                        </div>
                        <div class="help-text">Leave empty to get all available jobs</div>
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-target"></i> Number of Jobs</label>
                        <div class="input-wrapper">
                            <select id="jobs" class="form-control">
                                <option value="5">5 Jobs</option>
                                <option value="25" selected>25 Jobs</option>
                                <option value="50">50 Jobs</option>
                                <option value="100">100 Jobs</option>
                            </select>
                        </div>
                        <div class="help-text">Select how many jobs to scrape</div>
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-envelope"></i> JobRight Email (Optional)</label>
                        <div class="input-wrapper">
                            <input type="email" id="custom_email" class="form-control" 
                                   placeholder="your@email.com">
                        </div>
                        <div class="help-text">Leave empty to use saved accounts, or enter custom email to use different account</div>
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-lock"></i> JobRight Password (Optional)</label>
                        <div class="input-wrapper">
                            <input type="password" id="custom_password" class="form-control" 
                                   placeholder="Your password">
                        </div>
                        <div class="help-text">Required only if custom email is provided</div>
                    </div>
                    
                    <button type="submit" id="btn" class="btn-primary">
                        <i class="fas fa-play"></i> Start Professional Scraping
                    </button>
                </form>
            </div>
            
            <div id="loading" class="loading-section">
                <div class="spinner"></div>
                <div class="loading-text">Scraping in Progress...</div>
                <div class="loading-subtext">Extracting real job data and creating Google Sheets</div>
            </div>
            
            <div id="results" class="results-section">
                <div class="success-header">
                    <i class="fas fa-check-circle"></i>
                    <h3>Scraping Complete!</h3>
                </div>
                
                <div class="stats-grid" id="stats">
                    <!-- Stats will be populated by JavaScript -->
                </div>
                
                <div class="details-section" id="details">
                    <!-- Details will be populated by JavaScript -->
                </div>
                
                <button class="btn-secondary" onclick="location.reload()">
                    <i class="fas fa-redo"></i> Run Another Scraping Session
                </button>
            </div>
        </div>
    </div>
    
    <script>
        // Ensure Sheet ID is prefilled when page loads
        document.addEventListener('DOMContentLoaded', function() {
            const sheetField = document.getElementById('sheet');
            console.log('Sheet field found:', sheetField);
            console.log('Current value:', sheetField ? sheetField.value : 'Field not found');
            
            if (!sheetField.value || sheetField.value.trim() === '') {
                sheetField.value = '1iibXYJ5ZSFZzFIKUyM8d4u3x87FOereMESBfuFW7ZYI';
                console.log('Sheet ID prefilled:', sheetField.value);
            }
            
            // Also add cache busting for potential caching issues
            const timestamp = new Date().getTime();
            console.log('Page loaded at:', timestamp);
        });
        
        document.getElementById('form').onsubmit = async function(e) {
            e.preventDefault();
            
            const btn = document.getElementById('btn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const stats = document.getElementById('stats');
            const details = document.getElementById('details');
            
            // Get form data - simple and clean like command line
            const formData = {
                sheet_url: document.getElementById('sheet').value.trim(),
                keyword: document.getElementById('keyword').value.trim(),
                target_jobs: parseInt(document.getElementById('jobs').value),
                custom_email: document.getElementById('custom_email').value.trim(),
                custom_password: document.getElementById('custom_password').value.trim()
            };
            
            // Simple Sheet ID validation
            if (!formData.sheet_url || formData.sheet_url.length < 5) {
                alert('Please enter a valid Google Sheet ID');
                return;
            }
            
            // Validate custom credentials if provided
            if (formData.custom_email && !formData.custom_password) {
                alert('Please enter password for the custom email');
                return;
            }
            
            if (formData.custom_password && !formData.custom_email) {
                alert('Please enter email for the custom password');
                return;
            }
            
            // Show loading state
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                console.log('Starting scrape with data:', formData);
                console.log('User agent:', navigator.userAgent);
                console.log('Browser info:', {
                    platform: navigator.platform,
                    language: navigator.language,
                    cookieEnabled: navigator.cookieEnabled
                });
                
                const response = await fetch('/scrape', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'User-Agent': navigator.userAgent 
                    },
                    body: JSON.stringify(formData)
                });
                
                console.log('Response status:', response.status);
                console.log('Response headers:', Object.fromEntries(response.headers.entries()));
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                console.log('Response data:', data);
                
                if (data.success) {
                    // Populate stats
                    stats.innerHTML = `
                        <div class="stat-card">
                            <span class="stat-number">${data.total_jobs}</span>
                            <span class="stat-label">Total Jobs</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">${data.filtered_jobs}</span>
                            <span class="stat-label">Filtered Jobs</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">1+</span>
                            <span class="stat-label">Sheets Updated</span>
                        </div>
                    `;
                    
                    // Populate details
                    details.innerHTML = `
                        <div class="detail-item">
                            <span class="detail-label"><i class="fas fa-envelope"></i> Account Used</span>
                            <span class="detail-value">${data.account_email}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label"><i class="fas fa-key"></i> Keyword Filter</span>
                            <span class="detail-value">${formData.keyword ? formData.keyword : 'No filter (all jobs)'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label"><i class="fas fa-table"></i> Multi-Account Status</span>
                            <span class="detail-value">✅ Account rotation active</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label"><i class="fas fa-clock"></i> Session Time</span>
                            <span class="detail-value">${new Date().toLocaleTimeString()}</span>
                        </div>
                    `;
                    
                    results.style.display = 'block';
                } else {
                    alert('Scraping failed: ' + (data.message || 'Unknown error'));
                }
            } catch (error) {
                console.error('Full error details:', error);
                let errorMsg = 'Connection failed. Please check your internet connection and try again.';
                if (error.message) {
                    if (error.message.includes('HTTP error! status: 500')) {
                        errorMsg = 'Server processing error. The backend had an issue - please check the configuration and try again.';
                    } else if (error.message.includes('HTTP error! status: 400')) {
                        errorMsg = 'Invalid request data. Please check your inputs and try again.';
                    } else if (error.message.includes('HTTP error')) {
                        errorMsg = `Server error (${error.message}). Please try again in a moment.`;
                    } else if (error.message.includes('fetch')) {
                        errorMsg = 'Network connection failed. Please check your internet and try again.';
                    }
                }
                alert('Error: ' + errorMsg);
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-play"></i> Start Professional Scraping';
                loading.style.display = 'none';
            }
        };
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "scraper_available": True
    })

@app.route('/debug')
def debug():
    """Debug endpoint to help troubleshoot client issues"""
    return jsonify({
        "server_time": datetime.now().isoformat(),
        "flask_version": "Working",
        "scraper_status": "Available",
        "demo_request": {
            "url": "/scrape",
            "method": "POST",
            "sample_data": {
                "sheet_url": "1iibXYJ5ZSFZzFIKUyM8d4u3x87FOereMESBfuFW7ZYI",
                "keyword": "test",
                "target_jobs": 5,
                "custom_email": "",
                "custom_password": ""
            }
        }
    })

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Log request details for debugging
        print(f"🔍 REQUEST DEBUG:")
        print(f"   Headers: {dict(request.headers)}")
        print(f"   Method: {request.method}")
        print(f"   Content-Type: {request.content_type}")
        print(f"   Data: {request.data}")
        
        data = request.json or {}
        print(f"   Parsed JSON: {data}")
        
        sheet_id = data.get('sheet_url', '').strip()  # Now expecting sheet ID directly
        keyword = data.get('keyword', '').strip()
        target_jobs = int(data.get('target_jobs', 100))
        custom_email = data.get('custom_email', '').strip()
        custom_password = data.get('custom_password', '').strip()
        
        print(f"📊 PROCESSING:")
        print(f"   Sheet ID: {sheet_id}")
        print(f"   Keyword: '{keyword}'")
        print(f"   Target Jobs: {target_jobs}")
        print(f"   Custom Email: {'***' if custom_email else 'None'}")
        print(f"   Custom Password: {'***' if custom_password else 'None'}")
        
        if not sheet_id:
            return jsonify({"success": False, "message": "Sheet ID required"})
        
        # Simple validation - just check length like command line would
        if len(sheet_id) < 10:
            return jsonify({"success": False, "message": "Invalid Sheet ID format. Please check and try again."})
        
        # Run scraper exactly like command line version - simple and direct
        try:
            from enhanced_scraper_with_credentials import EnhancedJobRightScraper
            scraper = EnhancedJobRightScraper()
            
            # Set custom credentials if provided
            if custom_email and custom_password:
                scraper.set_custom_credentials(custom_email, custom_password)
            
            # Call scraper exactly like command line does
            result = scraper.run_complete_scraper(
                sheet_url=sheet_id,  # Pass sheet ID directly like command line
                keyword=keyword,
                target_jobs=target_jobs
            )
            return jsonify(result)
            
        except ImportError as e:
            return jsonify({"success": False, "message": f"Scraper not available: {str(e)}"})
        except Exception as e:
            error_msg = str(e)
            print(f"❌ SCRAPER ERROR: {error_msg}")
            print(f"   Error type: {type(e).__name__}")
            
            # Enhanced error handling
            if "timeout" in error_msg.lower():
                error_msg = "Processing timeout - try with fewer jobs (5-25) for faster results"
            elif "permission" in error_msg.lower() or "credentials" in error_msg.lower():
                error_msg = "Google Sheets access error. Please share the sheet with: sheetsservice@sheets-autoexpor.iam.gserviceaccount.com"
            elif "not found" in error_msg.lower():
                error_msg = "Sheet not found. Please check the Sheet ID and sharing permissions."
            elif "connection" in error_msg.lower():
                error_msg = "Network connection issue. Please check your internet and try again."
            
            print(f"   Processed error: {error_msg}")
            return jsonify({"success": False, "message": f"Scraping failed: {error_msg}"})
        
    except Exception as e:
        error_details = str(e)
        print(f"💥 REQUEST ERROR: {error_details}")
        print(f"   Error type: {type(e).__name__}")
        return jsonify({"success": False, "message": f"Request error: {error_details}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)