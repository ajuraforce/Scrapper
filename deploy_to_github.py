#!/usr/bin/env python3
"""
GitHub Deployment Script for JobRight Scraper
Pushes all necessary files to GitHub repository using Personal Access Token
"""

import os
import subprocess
import sys
from pathlib import Path

class GitHubDeployer:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_PAT')
        self.github_owner = os.getenv('GITHUB_OWNER')
        self.github_repo = os.getenv('GITHUB_REPO')
        
        if not all([self.github_token, self.github_owner, self.github_repo]):
            print("❌ Error: Missing required environment variables:")
            print("   - GITHUB_PAT (Personal Access Token)")
            print("   - GITHUB_OWNER (GitHub username/organization)")
            print("   - GITHUB_REPO (Repository name)")
            sys.exit(1)
    
    def run_command(self, command, check=True):
        """Run shell command and return result"""
        try:
            print(f"🔧 Running: {command}")
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            if e.stderr:
                print(f"   Error: {e.stderr}")
            if check:
                sys.exit(1)
            return e
    
    def create_gitignore(self):
        """Create .gitignore file with essential exclusions"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local

# Sensitive files (keep these local)
credentials.json
*.key
*.pem

# Replit specific
.replit
replit.nix

# Account tracking
.last_account

# Temporary files
*.tmp
*.temp
"""
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
    
    def create_requirements_txt(self):
        """Create requirements.txt with all dependencies"""
        requirements = """flask==3.0.0
flask-cors==4.0.0
gunicorn==23.0.0
requests==2.31.0
gspread==6.0.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
python-dotenv==1.0.0
apscheduler==3.10.4
beautifulsoup4==4.12.2
pandas==2.1.3
trafilatura==1.7.0
urllib3==2.1.0
"""
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        print("✅ Created requirements.txt")
    
    def setup_git_config(self):
        """Configure git for deployment"""
        # Set up git user (required for commits)
        self.run_command('git config user.name "JobRight Scraper Bot"')
        self.run_command('git config user.email "scraper@jobright.local"')
        
        # Set up remote with token authentication
        remote_url = f"https://{self.github_token}@github.com/{self.github_owner}/{self.github_repo}.git"
        
        # Remove existing origin if it exists
        self.run_command('git remote remove origin', check=False)
        
        # Add new origin with token
        self.run_command(f'git remote add origin {remote_url}')
        print("✅ Git configuration complete")
    
    def prepare_files(self):
        """Prepare files for deployment"""
        print("📋 Preparing files for deployment...")
        
        # Create essential files
        self.create_gitignore()
        self.create_requirements_txt()
        
        # List of essential files to include
        essential_files = [
            'app.py',
            'enhanced_scraper_with_credentials.py',
            'README.md',
            'requirements.txt',
            '.gitignore',
            'replit.md'
        ]
        
        # Check which files exist
        existing_files = []
        missing_files = []
        
        for file in essential_files:
            if Path(file).exists():
                existing_files.append(file)
                print(f"✅ Found: {file}")
            else:
                missing_files.append(file)
                print(f"⚠️ Missing: {file}")
        
        if missing_files:
            print(f"\n⚠️ Warning: {len(missing_files)} files are missing:")
            for file in missing_files:
                print(f"   - {file}")
            print("Continuing with available files...")
        
        return existing_files
    
    def commit_and_push(self, files):
        """Commit and push files to GitHub"""
        print("\n🚀 Deploying to GitHub...")
        
        # Initialize git repo if needed
        if not Path('.git').exists():
            self.run_command('git init')
            print("✅ Initialized git repository")
        
        # Add files
        for file in files:
            self.run_command(f'git add {file}')
        
        # Check if there are changes to commit
        result = self.run_command('git status --porcelain', check=False)
        if not result.stdout.strip():
            print("ℹ️ No changes to commit")
            return
        
        # Commit changes
        commit_message = "🚀 Deploy JobRight Scraper with multi-account rotation and Google Sheets integration"
        self.run_command(f'git commit -m "{commit_message}"')
        
        # Push to GitHub
        print(f"📤 Pushing to GitHub repository: {self.github_owner}/{self.github_repo}")
        self.run_command('git push -u origin main', check=False)
        
        # Try master branch if main fails
        result = self.run_command('git push -u origin master', check=False)
        
        if result.returncode == 0:
            print("✅ Successfully deployed to GitHub!")
            print(f"🌐 Repository URL: https://github.com/{self.github_owner}/{self.github_repo}")
        else:
            print("❌ Failed to push to both main and master branches")
            print("   Check if the repository exists and you have write access")
    
    def deploy(self):
        """Main deployment process"""
        print("🚀 GitHub Deployment Tool for JobRight Scraper")
        print("=" * 50)
        print(f"📦 Target Repository: {self.github_owner}/{self.github_repo}")
        print("=" * 50)
        
        # Prepare files
        files = self.prepare_files()
        
        if not files:
            print("❌ No files to deploy!")
            sys.exit(1)
        
        # Setup git
        self.setup_git_config()
        
        # Deploy
        self.commit_and_push(files)
        
        print("\n✅ Deployment process completed!")
        print(f"🔗 Your repository: https://github.com/{self.github_owner}/{self.github_repo}")
        print("\n📋 Next steps:")
        print("   1. Verify files are uploaded correctly")
        print("   2. Add credentials.json to your deployment environment")
        print("   3. Configure environment variables as needed")
        print("   4. Deploy to your preferred hosting platform")

def main():
    """Main function"""
    deployer = GitHubDeployer()
    deployer.deploy()

if __name__ == "__main__":
    main()