# JobRight Production Scraper

## Overview

The JobRight Production Scraper is a web-based application designed to automate job data collection from JobRight.ai. The system features a Flask web interface for monitoring and controlling scraping operations, with Google Sheets integration for data storage and credential management. The application is built for production deployment with a focus on reliability and ease of use.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Web Interface**: Simple HTML-based dashboard served through Flask templates
- **Styling**: CSS with gradient backgrounds and glassmorphism effects for modern UI
- **Responsive Design**: Mobile-first approach with viewport meta tags

### Backend Architecture
- **Framework**: Flask web application with minimal dependencies
- **Session Management**: Built-in Flask sessions with configurable secret keys
- **Logging**: Python logging module configured for production-level monitoring
- **API Structure**: RESTful endpoints for scraping operations and status monitoring

### Authentication & Account Management
- **Dynamic Account Creation**: Automated generation of unique email/password combinations
- **Credential Storage**: Secure handling of account credentials for scraping operations
- **Session-based Authentication**: Flask session management for web interface access

### Data Collection Architecture
- **Web Scraping Engine**: Requests-based HTTP client with mobile user agent simulation
- **Rate Limiting**: Built-in delays and randomization to avoid detection
- **Error Handling**: Comprehensive timeout and retry mechanisms

### Deployment Architecture
- **Production-Ready**: Gunicorn-compatible WSGI application
- **Environment Configuration**: Environment variable support for sensitive data
- **Containerization-Ready**: Simple structure suitable for Docker deployment

## External Dependencies

### Google Services Integration
- **Google Sheets API**: Data storage and export functionality via gspread library
- **Service Account Authentication**: OAuth2 service account credentials for automated access
- **Credentials Management**: JSON-based service account key handling

### Third-Party APIs
- **JobRight.ai API**: Target platform for job data scraping
- **HTTP Client**: Requests library for web scraping operations

### Development Dependencies
- **Flask**: Web framework for dashboard and API endpoints
- **gspread**: Google Sheets Python integration
- **google-auth**: OAuth2 authentication for Google services
- **requests**: HTTP client library for web scraping

### Production Dependencies
- **Gunicorn**: WSGI HTTP Server for production deployment
- **Environment Variables**: Configuration management for sensitive data
- **Logging**: Production-grade logging and monitoring capabilities