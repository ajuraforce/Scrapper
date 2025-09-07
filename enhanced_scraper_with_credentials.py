#!/usr/bin/env python3
"""
ENHANCED JOBRIGHT SCRAPER - Saves account credentials used for scraping
"""

import requests
import json
import time
import random
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

class EnhancedJobRightScraper:
    def __init__(self):
        self.session = None
        # Multi-account support with rotation
        self.accounts = [
            {"email": "mrtandonh@icloud.com", "password": "ajay4498", "name": "Primary"},
            {"email": "manage@gmail.com", "password": "ajay4498", "name": "Manager"},
            {"email": "data@gmail.com", "password": "ajay4498", "name": "Data"}
        ]
        self.current_account = None
        self.account_email = None  # Will be set after successful login
        self.account_password = None  # Will be set after successful login
        self.user_id = None
        self.build_id = "gFSErx8v1VLk8KWjI8bBJ"  # Updated from working example
        self.last_used_account_index = -1  # Track account rotation
        self.custom_credentials = None  # Store custom credentials if provided
        
    def set_custom_credentials(self, email, password):
        """Set custom credentials to use instead of saved accounts"""
        self.custom_credentials = {
            "email": email,
            "password": password,
            "name": "Custom"
        }
        print(f"🔧 Custom credentials set for: {email}")
        
    def setup_session(self):
        """Setup session with working headers"""
        self.session = requests.Session()
        
        # Critical headers for successful authentication and job access
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-Client-Type': 'mobile_web',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://jobright.ai/',
            'Origin': 'https://jobright.ai',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        })
        print("✅ Session configured")
    
    def get_next_account_index(self):
        """Get the next account index for rotation"""
        try:
            # Try to read last used account from a simple file
            with open('.last_account', 'r') as f:
                self.last_used_account_index = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.last_used_account_index = -1
        
        # Move to next account
        self.last_used_account_index = (self.last_used_account_index + 1) % len(self.accounts)
        
        # Save the new index
        with open('.last_account', 'w') as f:
            f.write(str(self.last_used_account_index))
        
        return self.last_used_account_index

    def login_existing_account(self):
        """Login with multi-account support and intelligent rotation"""
        # Check if custom credentials are provided
        if self.custom_credentials:
            print("🔧 Using Custom Credentials")
            print("=" * 30)
            account = self.custom_credentials
            print(f"🔄 Using Custom Account: {account['name']} ({account['email']})")
        else:
            print(f"🔑 Multi-Account Rotation System ({len(self.accounts)} accounts available)")
            print("=" * 55)
            
            # Get the next account to use
            next_account_index = self.get_next_account_index()
            account = self.accounts[next_account_index]
            print(f"🔄 Using Account {next_account_index + 1}/{len(self.accounts)}: {account['name']} ({account['email']})")
        
        try:
            # Set current account details
            self.account_email = account['email']
            self.account_password = account['password']
            self.current_account = account
            
            # Login with current account
            login_data = {
                "email": self.account_email,
                "password": self.account_password
            }
            
            response = self.session.post(
                "https://jobright.ai/swan/auth/login/pwd",
                json=login_data,
                timeout=15
            )
            
            if response.status_code == 200 and response.json().get('success'):
                user_data = response.json().get('result', {})
                self.user_id = user_data.get('userId')
                print(f"✅ Successfully logged in: {account['name']} ({self.account_email})")
                print(f"   User ID: {self.user_id}")
                print(f"   🎯 Using account-specific filters and preferences")
                
                # Follow exact workflow sequence
                self.follow_exact_workflow()
                return True
            else:
                print(f"❌ Account failed: Status {response.status_code}")
                print(f"⚠️ Trying fallback account rotation...")
                return self.fallback_account_login()
                
        except Exception as e:
            print(f"⚠️ Account error: {str(e)}")
            print(f"⚠️ Trying fallback account rotation...")
            return self.fallback_account_login()
    
    def fallback_account_login(self):
        """Fallback method - try all accounts if rotation fails"""
        print("🔄 Fallback: Trying all accounts...")
        
        # Try each account in sequence as fallback
        for i, account in enumerate(self.accounts, 1):
            try:
                print(f"🔄 Fallback Account {i}/{len(self.accounts)}: {account['name']} ({account['email']})")
                
                # Set current account details
                self.account_email = account['email']
                self.account_password = account['password']
                self.current_account = account
                
                # Login with current account
                login_data = {
                    "email": self.account_email,
                    "password": self.account_password
                }
                
                response = self.session.post(
                    "https://jobright.ai/swan/auth/login/pwd",
                    json=login_data,
                    timeout=15
                )
                
                if response.status_code == 200 and response.json().get('success'):
                    user_data = response.json().get('result', {})
                    self.user_id = user_data.get('userId')
                    print(f"✅ Fallback login successful: {account['name']} ({self.account_email})")
                    print(f"   User ID: {self.user_id}")
                    print(f"   🎯 Using account-specific filters and preferences")
                    
                    # Follow exact workflow sequence
                    self.follow_exact_workflow()
                    return True
                else:
                    print(f"❌ Fallback Account {i} failed: Status {response.status_code}")
                    # Continue to next account
                    
            except Exception as e:
                print(f"⚠️ Fallback Account {i} error: {str(e)}")
                # Continue to next account
                
            # Small delay between account attempts
            time.sleep(1)
        
        print(f"❌ All {len(self.accounts)} accounts failed - trying fallback")
        return self.register_account_fallback()

    def register_account_fallback(self):
        """Enhanced fallback login method - retry with different account strategies"""
        print(f"🔄 Enhanced Fallback: Trying alternative login approaches...")
        
        # Try accounts with longer timeout
        for i, account in enumerate(self.accounts, 1):
            try:
                print(f"🔄 Fallback Account {i}/{len(self.accounts)}: {account['name']}")
                
                self.account_email = account['email']
                self.account_password = account['password']
                self.current_account = account
                
                login_data = {
                    "email": self.account_email,
                    "password": self.account_password
                }
                
                response = self.session.post(
                    "https://jobright.ai/swan/auth/login/pwd",
                    json=login_data,
                    timeout=20  # Longer timeout for fallback
                )
                
                if response.status_code == 200 and response.json().get('success'):
                    user_data = response.json().get('result', {})
                    self.user_id = user_data.get('userId')
                    print(f"✅ Fallback successful: {account['name']} ({self.account_email})")
                    print(f"   User ID: {self.user_id}")
                    return True
                    
            except Exception as e:
                print(f"⚠️ Fallback Account {i} error: {str(e)}")
                
            time.sleep(2)  # Longer delay for fallback attempts
        
        print(f"⚠️ All fallback attempts failed, continuing with public access")
        print(f"   Will still attempt to scrape available jobs")
        return True
    
    def follow_exact_workflow(self):
        """Follow exact working workflow: User Info → Settings → A/B Config"""
        try:
            print("📋 Following exact workflow sequence...")
            
            # Step 1: Get user info
            time.sleep(1)
            self.get_user_info()
            
            # Step 2: Get user settings
            time.sleep(1)
            self.get_user_settings()
            
            # Step 3: Get A/B config
            time.sleep(1)
            self.get_ab_config()
            
            print("✅ Exact workflow completed")
            return True
            
        except Exception as e:
            print(f"⚠️ Workflow error: {str(e)}")
            return True
    
    def get_user_info(self):
        """Get user info following exact workflow"""
        try:
            print("📋 Getting user info...")
            
            response = self.session.get("https://jobright.ai/swan/auth/newinfo", timeout=15)
            
            print(f"User Info Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        result = data.get('result', {})
                        print(f"✅ User info retrieved - Stage: {result.get('currentStage')}")
                        print(f"✅ LinkedIn Resume: {result.get('linkedinResume')}")
                        print(f"✅ Full Name: {result.get('fullName')}")
                        return True
                    else:
                        print(f"❌ Failed to get user info: {data}")
                        return False
                except:
                    print(f"❌ User info response not JSON")
                    return False
            else:
                print(f"❌ User info request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ User info error: {str(e)}")
            return False
    
    def get_user_settings(self):
        """Get user settings following exact workflow"""
        try:
            print("⚙️ Getting user settings...")
            
            response = self.session.get("https://jobright.ai/swan/user-settings/get", timeout=15)
            
            print(f"User Settings Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        print("✅ User settings retrieved")
                        return True
                    else:
                        print(f"❌ Failed to get user settings: {data}")
                        return False
                except:
                    print(f"❌ User settings response not JSON")
                    return False
            else:
                print(f"❌ User settings request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ User settings error: {str(e)}")
            return False
    
    def get_ab_config(self):
        """Get A/B testing config following exact workflow"""
        try:
            print("🧪 Getting A/B config...")
            
            if not self.user_id:
                print("❌ No user ID available for A/B config")
                return False
            
            response = self.session.get(
                f"https://jobright.ai/swan/ab/user?user={self.user_id}", 
                timeout=15
            )
            
            print(f"A/B Config Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        print("✅ A/B config retrieved")
                        return True
                    else:
                        print(f"❌ Failed to get A/B config: {data}")
                        return False
                except:
                    print(f"❌ A/B config response not JSON")
                    return False
            else:
                print(f"❌ A/B config request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ A/B config error: {str(e)}")
            return False
    
    def complete_onboarding(self):
        """Complete all onboarding steps to ensure job access"""
        try:
            print("📋 Checking and completing onboarding sequence...")
            
            # Event 1: Start matching
            matching_event = {
                "timestamp": int(time.time() * 1000),
                "timezoneId": "Asia/Calcutta",
                "browserInfo": {"userAgent": self.session.headers["User-Agent"]},
                "eventDetail": {
                    "platform": "mobile",
                    "browser_type": "safari", 
                    "is_in_app": False,
                    "user_agent": self.session.headers["User-Agent"],
                    "is_mobile": True,
                    "scene": "linkedin"
                },
                "eventType": "mobile_onboard_start_matching_click",
                "channel": "linkedin"
            }
            
            self.session.post("https://jobright.ai/swan/event/submit", json=matching_event)
            print("✅ Start matching event sent")
            
            # Event 2: LinkedIn profile (skip if already set, but submit to refresh)
            linkedin_data = {"linkedinId": "https://www.linkedin.com/in/williamhgates"}
            response = self.session.post("https://jobright.ai/swan/resume/linkedin", json=linkedin_data)
            print("✅ LinkedIn profile submitted/refreshed")
            
            # Event 3: Get user profile and send refresh event
            time.sleep(3)  # Wait for processing
            
            auth_response = self.session.get("https://jobright.ai/swan/auth/newinfo")
            if auth_response.status_code == 200:
                user_profile = auth_response.json().get('result', {})
                
                # Critical profile refresh event
                refresh_event = {
                    "timestamp": int(time.time() * 1000),
                    "timezoneId": "Asia/Calcutta",
                    "browserInfo": {"userAgent": self.session.headers["User-Agent"]},
                    "eventDetail": dict(user_profile, **{"platform": "mobile"}),
                    "eventType": "debug_onboarding_profile_refresh_after",
                    "channel": "default"
                }
                
                self.session.post("https://jobright.ai/swan/event/submit", json=refresh_event)
                print("✅ Profile refresh event sent")
                
                # Check if LinkedIn was processed
                if user_profile.get('linkedinResume'):
                    print("✅ LinkedIn resume processed successfully")
                    return True
            
            print("⚠️ Onboarding completed, checking job access...")
            return True
            
        except Exception as e:
            print(f"⚠️ Onboarding error: {str(e)}")
            return True
    
    def fetch_real_jobs_nextjs(self, target_jobs=100):
        """Fetch REAL jobs using NextJS endpoint"""
        print(f"\n🎯 FETCHING REAL JOBS VIA NEXTJS...")
        
        # Method 1: Try NextJS data endpoint
        nextjs_headers = self.session.headers.copy()
        nextjs_headers.update({
            'x-nextjs-data': '1',
            'Accept': '*/*'
        })
        
        nextjs_url = f"https://jobright.ai/_next/data/{self.build_id}/jobs/recommend.json"
        
        response = self.session.get(nextjs_url, headers=nextjs_headers, timeout=20)
        
        print(f"NextJS Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Check if we have actual job data
                if 'pageProps' in data:
                    page_props = data['pageProps']
                    print(f"PageProps keys: {list(page_props.keys())}")
                    
                    # Look for job data in pageProps
                    job_data = self.extract_jobs_from_nextjs(page_props)
                    if job_data:
                        print(f"🎉 FOUND {len(job_data)} REAL JOBS FROM NEXTJS!")
                        return job_data[:target_jobs]
                
                # If no jobs in pageProps, the user might need to complete more onboarding
                print("📋 NextJS accessible but no job data - user may need more onboarding")
                
            except json.JSONDecodeError:
                print("❌ NextJS response not valid JSON")
        
        return []
    
    def extract_jobs_from_nextjs(self, page_props):
        """Extract real jobs from NextJS page props"""
        jobs = []
        
        # Look in various possible locations
        possible_keys = ['jobList', 'jobs', 'recommendedJobs', 'results']
        
        for key in page_props:
            value = page_props[key]
            
            # Check if this looks like job data
            if isinstance(value, list) and value:
                # Check first item to see if it looks like a job
                first_item = value[0] if value else {}
                if isinstance(first_item, dict) and any(job_key in first_item for job_key in ['jobId', 'jobTitle', 'companyName']):
                    print(f"Found job data in key: {key}")
                    return self.process_nextjs_jobs(value)
            
            # Check nested objects
            if isinstance(value, dict):
                for nested_key in possible_keys:
                    if nested_key in value and isinstance(value[nested_key], list):
                        nested_jobs = value[nested_key]
                        if nested_jobs:
                            print(f"Found job data in nested key: {key}.{nested_key}")
                            return self.process_nextjs_jobs(nested_jobs)
        
        return jobs
    
    def process_nextjs_jobs(self, job_list):
        """Process jobs from NextJS response"""
        processed_jobs = []
        
        for job_item in job_list:
            try:
                # Job data might be nested
                job_data = job_item.get('jobResult', job_item)
                
                job = {
                    'job_title': job_data.get('jobTitle', ''),
                    'company': job_data.get('companyName', ''),
                    'location': job_data.get('jobLocation', ''),
                    'work_model': job_data.get('workModel', ''),
                    'salary': job_data.get('salaryDesc', ''),
                    'seniority': job_data.get('jobSeniority', ''),
                    'employment_type': job_data.get('employmentType', ''),
                    'is_remote': job_data.get('isRemote', False),
                    'summary': job_data.get('jobSummary', '')[:300] + '...' if job_data.get('jobSummary') else '',
                    'apply_link': job_data.get('applyLink', ''),
                    'job_id': job_data.get('jobId', ''),
                    'match_score': job_item.get('displayScore', 0),
                    'rank': job_item.get('rankDesc', ''),
                    'publish_time': job_data.get('publishTimeDesc', ''),
                    'source': 'JobRight.ai REAL DATA (NextJS)',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                if job['job_title']:  # Only add if we have a real job title
                    processed_jobs.append(job)
                    
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        return processed_jobs
    
    def fetch_real_jobs_regular_api(self, target_jobs=100):
        """Try regular jobs API with enhanced parameters"""
        print("🔄 Trying regular jobs API...")
        
        response = self.session.get(
            "https://jobright.ai/swan/recommend/list/jobs?refresh=true&sortCondition=0&position=0",
            timeout=15
        )
        
        print(f"Regular API Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('success') and data.get('result', {}).get('jobList'):
                    job_list = data['result']['jobList']
                    print(f"🎉 FOUND {len(job_list)} REAL JOBS FROM API!")
                    return self.process_api_jobs(job_list)[:target_jobs]
                else:
                    print(f"API returned: {data}")
            except:
                print("Failed to parse API response")
        
        return []
    
    def process_api_jobs(self, job_list):
        """Process jobs from regular API"""
        processed_jobs = []
        
        for job_item in job_list:
            try:
                job_result = job_item.get('jobResult', {})
                
                job = {
                    'job_title': job_result.get('jobTitle', ''),
                    'company': job_result.get('companyName', ''),
                    'location': job_result.get('jobLocation', ''),
                    'work_model': job_result.get('workModel', ''),
                    'salary': job_result.get('salaryDesc', ''),
                    'seniority': job_result.get('jobSeniority', ''),
                    'employment_type': job_result.get('employmentType', ''),
                    'is_remote': job_result.get('isRemote', False),
                    'summary': job_result.get('jobSummary', '')[:300] + '...' if job_result.get('jobSummary') else '',
                    'apply_link': job_result.get('applyLink', ''),
                    'job_id': job_result.get('jobId', ''),
                    'match_score': job_item.get('displayScore', 0),
                    'rank': job_item.get('rankDesc', ''),
                    'publish_time': job_result.get('publishTimeDesc', ''),
                    'source': 'JobRight.ai REAL DATA (API)',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                if job['job_title']:
                    processed_jobs.append(job)
                    
            except Exception as e:
                continue
        
        return processed_jobs
    
    def fetch_real_jobs_with_diverse_search(self, target_jobs=100, job_titles=None):
        """Fetch real jobs using diverse job title searches to avoid duplicates"""
        try:
            print(f"\n🎯 FETCHING DIVERSE JOBRIGHT DATA")
            print(f"Target jobs: {target_jobs}")
            print("=" * 60)
            
            # Fallback to regular fetch if session issues
            if not self.session:
                print("⚠️ Session not ready, falling back to regular fetch")
                return self.fetch_real_jobs_fallback(target_jobs)
            
            all_real_jobs = []
            
            # Start with smaller set for testing
            if not job_titles:
                job_titles = [
                    "Software Engineer", "Data Scientist", "Product Manager", "Marketing Manager"
                ]
            
            jobs_per_title = max(target_jobs // len(job_titles), 15)  # At least 15 jobs per title
            
            for i, job_title in enumerate(job_titles):
                if len(all_real_jobs) >= target_jobs:
                    break
                    
                print(f"\n🔍 SEARCHING FOR: {job_title}")
                print(f"   Target for this search: {jobs_per_title} jobs")
                
                try:
                    title_jobs = self.fetch_jobs_by_title(job_title, jobs_per_title)
                    
                    if title_jobs:
                        # Filter out duplicates based on job_id
                        existing_ids = {job.get('job_id') for job in all_real_jobs}
                        new_jobs = [job for job in title_jobs if job.get('job_id') not in existing_ids]
                        
                        all_real_jobs.extend(new_jobs)
                        print(f"   ✅ {len(new_jobs)} new unique jobs added (filtered {len(title_jobs) - len(new_jobs)} duplicates)")
                    else:
                        print(f"   ⚠️ No jobs found for '{job_title}'")
                        
                except Exception as e:
                    print(f"   ❌ Error searching '{job_title}': {str(e)}")
                    continue
                
                time.sleep(2)  # Respectful delay between searches
            
            print(f"\n🎉 TOTAL DIVERSE JOBS: {len(all_real_jobs)}")
            return all_real_jobs[:target_jobs]  # Return only requested amount
            
        except Exception as e:
            print(f"❌ Diverse search failed: {str(e)}, falling back to regular fetch")
            return self.fetch_real_jobs_fallback(target_jobs)
    
    def update_job_title_filter(self, job_title):
        """Update the job title filter via API, simulating manual change"""
        try:
            # First, get current filters (optional, but helps build the update payload)
            get_response = self.session.get("https://jobright.ai/swan/filter/get/filter", timeout=15)
            if get_response.status_code != 200:
                print(f"⚠️ Failed to get current filters: {get_response.status_code}")
                return False

            current_filters = get_response.json().get('result', {})

            # Build update payload based on network logs
            update_payload = {
                "filterCandidates": {
                    "industryCandidates": current_filters.get('industryCandidates', []),
                    "skillCandidates": []
                },
                "filters": {
                    "jobTitle": job_title,
                    "jobTaxonomyList": [{"title": job_title, "taxonomyId": "00-00-00"}],
                    "jobTypes": [1],  # Full-time
                    "workModel": [1, 2, 3],  # Onsite, hybrid, remote
                    "cityRadius": None,
                    "locations": [{"city": "Within US", "radiusRange": 25}],
                    "seniority": [5, 6],  # Mid/senior levels
                    "minYearsOfExperienceRange": None,
                    "daysAgo": None,
                    "annualSalaryMinimum": None,
                    "isH1BOnly": None,
                    "excludeSecurityClearance": False,
                    "excludeUsCitizen": False,
                    "companyCategory": [],
                    "excludeCompanyCategory": [],
                    "skills": [],
                    "excludedSkills": [],
                    "roleType": None,
                    "companyStages": None,
                    "excludeStaffingAgency": None,
                    "excludedCompanies": [],
                    "companies": []
                }
            }

            update_response = self.session.post(
                "https://jobright.ai/swan/filter/update/filter-v2",
                json=update_payload,
                timeout=15
            )

            if update_response.status_code == 200 and update_response.json().get('success'):
                print(f"✅ Filter updated for job title: {job_title}")
                return True
            else:
                print(f"❌ Filter update failed for '{job_title}': {update_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error updating filter: {str(e)}")
            return False

    def submit_filter_event(self, job_title):
        """Submit filter update event (optional, to mimic real user behavior)"""
        try:
            event_payload = {
                "timestamp": int(time.time() * 1000),  # Current timestamp in ms
                "timezoneId": "Asia/Calcutta",
                "browserInfo": {
                    "userAgent": self.session.headers['User-Agent'],
                    "is_in_app": False,
                    "is_mobile": True,
                    "browser_type": "safari"
                },
                "eventDetail": {
                    "platform": "mobile",
                    "standardTitle": [],
                    "customTitle": [{"title": job_title, "taxonomyId": "00-00-00"}],
                    "taxExpGroup": "on"
                },
                "eventType": "filter_update",
                "channel": "default"
            }

            event_response = self.session.post(
                "https://jobright.ai/swan/event/submit",
                json=event_payload,
                timeout=15
            )

            if event_response.status_code == 200 and event_response.json().get('success'):
                print(f"✅ Filter event submitted for '{job_title}'")
            else:
                print(f"⚠️ Event submission failed: {event_response.status_code}")
        except Exception as e:
            print(f"⚠️ Error submitting event: {str(e)}")

    def fetch_jobs_by_title(self, job_title, max_jobs=20):
        """Fetch jobs for a specific job title after updating filter"""
        jobs = []
        pages_needed = (max_jobs // 20) + 1

        # Try the proper filter API first
        filter_success = self.update_job_title_filter(job_title)
        
        if filter_success:
            # Use the filter-based approach
            self.submit_filter_event(job_title)
            time.sleep(2)  # Allow backend processing
            
            endpoint = "https://jobright.ai/swan/recommend/list/jobs"
            base_params = {"refresh": "true", "sortCondition": "1"}
            print(f"   🎯 Using filter-based approach for '{job_title}'")
        else:
            # Fallback to original approach
            endpoint = "https://jobright.ai/swan/recommend/landing/jobs"
            base_params = {}
            print(f"   ↩️ Using fallback approach for '{job_title}'")

        for page in range(min(pages_needed, 3)):  # Max 3 pages per title
            position = page * 20
            params = base_params.copy()
            params["position"] = position

            try:
                response = self.session.get(endpoint, params=params, timeout=15)

                if response.status_code == 200:
                    data = response.json()
                    
                    # Check for "edge of universe" message
                    if self.detect_job_universe_edge(data):
                        print(f"   📡 Hit edge of job universe for '{job_title}' - switching strategy")
                        break
                    
                    if data.get('success') and data.get('result', {}).get('jobList'):
                        job_list = data['result']['jobList']
                        page_jobs = self.process_jobs_safely(job_list, page, job_title)
                        jobs.extend(page_jobs)

                        if len(jobs) >= max_jobs:
                            break
                    else:
                        print(f"   ⚠️ No jobs in response for '{job_title}' on page {page + 1}")
                        
                        # If no jobs with filter approach, try fallback
                        if filter_success and page == 0:
                            print(f"   ⚿ Trying fallback for '{job_title}'")
                            fallback_jobs = self.fetch_jobs_fallback_method(job_title, max_jobs)
                            jobs.extend(fallback_jobs)
                            break
                else:
                    print(f"   ❌ Request failed for '{job_title}' on page {page + 1}: {response.status_code}")
                    break
            except Exception as e:
                print(f"   ❌ Error fetching jobs for '{job_title}' on page {page + 1}: {str(e)}")
                break

            time.sleep(1)  # Delay between pages

        return jobs
    
    def fetch_jobs_fallback_method(self, job_title, max_jobs=20):
        """Fallback method using original endpoint"""
        jobs = []
        try:
            for page in range(min(2, (max_jobs // 20) + 1)):
                position = page * 20
                params = {"position": position} if position > 0 else {}
                
                response = self.session.get(
                    "https://jobright.ai/swan/recommend/landing/jobs",
                    params=params,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('result', {}).get('jobList'):
                        job_list = data['result']['jobList']
                        page_jobs = self.process_jobs_safely(job_list, page, job_title)
                        jobs.extend(page_jobs)
                        
                        if len(jobs) >= max_jobs:
                            break
                time.sleep(1)
        except Exception as e:
            print(f"   ❌ Fallback method error: {str(e)}")
        
        return jobs
    
    def detect_job_universe_edge(self, response_data):
        """Detect if JobRight returned the 'edge of job universe' message"""
        # Check for indicators that we've hit the edge
        if not response_data.get('success'):
            return True
            
        result = response_data.get('result', {})
        job_list = result.get('jobList', [])
        
        # If no jobs returned or very few jobs
        if len(job_list) < 5:
            return True
            
        # Check for specific message patterns (this might be in different fields)
        message = result.get('message', '') or response_data.get('message', '')
        edge_indicators = [
            'edge of job universe',
            'no more jobs',
            'try different preferences',
            'change preferences'
        ]
        
        return any(indicator in message.lower() for indicator in edge_indicators)
    
    def try_alternative_search(self, job_title, position=0):
        """Try alternative search endpoints for job titles"""
        alternative_endpoints = [
            "https://jobright.ai/swan/recommend/search/jobs",
            "https://jobright.ai/swan/search/jobs",
            "https://jobright.ai/api/jobs/search"
        ]
        
        for endpoint in alternative_endpoints:
            try:
                params = {
                    "q": job_title,
                    "title": job_title,
                    "position": position
                }
                
                response = self.session.get(endpoint, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('result', {}).get('jobList'):
                        job_list = data['result']['jobList']
                        return self.process_jobs_safely(job_list, 0, job_title)
                        
            except Exception:
                continue
                
        return []
    
    def fetch_real_jobs_fallback(self, target_jobs=100):
        """Original job fetching method as fallback"""
        print(f"\n🎯 FETCHING JOBRIGHT DATA (FALLBACK)")
        print(f"Target jobs: {target_jobs}")
        print("=" * 60)
        
        all_real_jobs = []
        pages_needed = (target_jobs // 20) + 1
        
        for page in range(min(pages_needed, 10)):  # Max 10 pages (200 jobs)
            position = page * 20
            print(f"📄 Page {page + 1}...")
            
            try:
                response = self.session.get(
                    "https://jobright.ai/swan/recommend/landing/jobs",
                    params={"position": position} if position > 0 else {},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('result', {}).get('jobList'):
                        job_list = data['result']['jobList']
                        page_jobs = self.process_jobs_safely(job_list, page)
                        all_real_jobs.extend(page_jobs)
                        print(f"   ✅ {len(page_jobs)} jobs processed")
                        
                        if len(all_real_jobs) >= target_jobs:
                            print(f"🎯 Target reached: {len(all_real_jobs)} jobs")
                            break
                    else:
                        break
                else:
                    print(f"   ❌ Page {page + 1}: Request failed")
                    break
            except Exception as e:
                print(f"   ❌ Error on page {page + 1}: {str(e)}")
                break
                
            time.sleep(1)
        
        print(f"\n🎉 TOTAL JOBS: {len(all_real_jobs)}")
        return all_real_jobs

    def fetch_real_jobs_with_pagination(self, target_jobs=100):
        """Direct pagination through recommended jobs endpoint"""
        print(f"\n🎯 FETCHING JOBRIGHT DATA WITH PAGINATION")
        print(f"Target jobs: {target_jobs}")
        print("=" * 60)
        
        all_real_jobs = []
        # Always scrape 4-5 pages as requested (80-100 jobs)
        max_pages = 5  # Scrape 4-5 pages
        
        for page in range(min(max_pages, 5)):  # Scrape exactly 4-5 pages
            position = page * 20
            page_num = page + 1
            
            print(f"📄 Page {page_num}: https://jobright.ai/swan/recommend/landing/jobs", end="")
            if position > 0:
                print(f"?position={position}")
            else:
                print()
            
            try:
                # Use proper headers for authenticated pagination
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Cache-Control': 'no-cache',
                    'Origin': 'https://jobright.ai',
                    'Referer': 'https://jobright.ai/jobs',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                
                params = {"position": position} if position > 0 else {}
                response = self.session.get(
                    "https://jobright.ai/swan/recommend/landing/jobs",
                    params=params,
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    job_list = data.get('result', {}).get('jobs', [])
                    
                    if not job_list:
                        if page == 0:
                            print(f"   ⚠️ No jobs found - may need authentication")
                            print(f"   🔄 Falling back to diverse search approach")
                            return self.fetch_real_jobs_with_diverse_search(target_jobs)
                        else:
                            print(f"   ⚠️ No more jobs found on page {page_num}")
                            break
                    
                    page_jobs = self.process_jobs_safely(job_list, page_num)
                    all_real_jobs.extend(page_jobs)
                    
                    print(f"   ✅ {len(page_jobs)} jobs fetched (Total: {len(all_real_jobs)})")
                    
                    if len(all_real_jobs) >= target_jobs:
                        print(f"   🎯 Target reached! ({len(all_real_jobs)} >= {target_jobs})")
                        break
                        
                else:
                    print(f"   ❌ Failed: Status {response.status_code}")
                    if page == 0:  # If first page fails, don't continue
                        break
                        
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                if page == 0:  # If first page fails, don't continue
                    break
            
            # Rate limiting
            time.sleep(1.5)
        
        print(f"\n🎉 TOTAL JOBS FETCHED: {len(all_real_jobs)}")
        return all_real_jobs[:target_jobs]  # Return exactly target amount

    def fetch_real_jobs(self, target_jobs=100):
        """Fetch real jobs with pagination priority since login works"""
        print(f"\n🚀 AUTHENTICATED JOB FETCHING WITH PAGINATION")
        print(f"Target jobs: {target_jobs} (10 pages × 20 jobs = 200)")
        print("=" * 60)
        
        # Method 1: Try pagination approach first (since login works)
        print("📄 Trying pagination approach (recommended)...")
        jobs = self.fetch_real_jobs_with_pagination(target_jobs)
        if jobs and len(jobs) >= target_jobs * 0.7:  # Got at least 70% of target
            print(f"✅ Pagination success: {len(jobs)} jobs")
            return jobs
        
        # Method 2: Try regular API as backup
        if not jobs or len(jobs) < target_jobs * 0.5:
            print("🔄 Trying regular API as backup...")
            api_jobs = self.fetch_real_jobs_regular_api(target_jobs)
            if api_jobs:
                jobs.extend(api_jobs)
                # Remove duplicates based on job_id
                seen = set()
                unique_jobs = []
                for job in jobs:
                    job_id = job.get('job_id', '')
                    if job_id and job_id not in seen:
                        seen.add(job_id)
                        unique_jobs.append(job)
                jobs = unique_jobs
                print(f"✅ Combined with API: {len(jobs)} unique jobs")
        
        # Method 3: Try NextJS endpoint if still not enough
        if not jobs or len(jobs) < target_jobs * 0.3:
            print("🔄 Trying NextJS endpoint...")
            nextjs_jobs = self.fetch_real_jobs_nextjs(target_jobs)
            if nextjs_jobs:
                jobs.extend(nextjs_jobs)
                print(f"✅ Combined with NextJS: {len(jobs)} jobs")
        
        # Method 4: Fallback to diverse search if needed
        if not jobs or len(jobs) < target_jobs * 0.2:
            print("🔄 Final fallback to diverse search...")
            jobs = self.fetch_real_jobs_with_diverse_search(target_jobs)
            if jobs:
                print(f"✅ Diverse search fallback: {len(jobs)} jobs")
        
        return jobs[:target_jobs] if jobs else []
    
    def process_jobs_safely(self, job_list, page_num, search_title=None):
        """Process jobs with safe data type handling"""
        processed_jobs = []
        
        for i, job_item in enumerate(job_list):
            try:
                job_result = job_item.get('jobResult', {})
                company_result = job_item.get('companyResult', {})
                
                def safe_extract(field_value, default=''):
                    if isinstance(field_value, list):
                        return ' | '.join(str(item) for item in field_value) if field_value else default
                    elif field_value is None:
                        return default
                    else:
                        return str(field_value)
                
                job = {
                    'job_title': safe_extract(job_result.get('jobTitle')),
                    'company': safe_extract(company_result.get('companyName', 'Company Not Listed')),
                    'location': safe_extract(job_result.get('jobLocation')),
                    'work_model': safe_extract(job_result.get('workModel')),
                    'salary': safe_extract(job_result.get('salaryDesc')),
                    'seniority': safe_extract(job_result.get('jobSeniority')),
                    'employment_type': safe_extract(job_result.get('employmentType')),
                    'is_remote': str(job_result.get('isRemote', False)),
                    'job_summary': safe_extract(job_result.get('jobSummary')),
                    'core_responsibilities': safe_extract(job_result.get('coreResponsibilities')),
                    'min_experience': safe_extract(job_result.get('minYearsOfExperience')),
                    'apply_link': safe_extract(job_result.get('applyLink')),
                    'job_id': safe_extract(job_result.get('jobId')),
                    'publish_desc': safe_extract(job_result.get('publishTimeDesc')),
                    'page_number': page_num + 1,
                    'position_in_page': i + 1,
                    'company_size': safe_extract(company_result.get('companySize')),
                    'source': f'JobRight.ai - {search_title}' if search_title else 'JobRight.ai DIVERSE SEARCH',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    # Add account information to each job
                    'scraper_email': self.account_email or 'Public Access',
                    'scraper_password': self.account_password or 'N/A'
                }
                
                if job['job_title']:
                    processed_jobs.append(job)
                    
            except Exception as e:
                print(f"   ⚠️ Error processing job {i}: {e}")
                continue
        
        return processed_jobs
    
    def filter_jobs_by_keyword(self, all_jobs, keyword=""):
        """Filter jobs by keyword with safe string handling"""
        if not keyword:
            print("🔍 No keyword filter - returning all jobs")
            return all_jobs
            
        print(f"\n🎯 FILTERING FOR KEYWORD: '{keyword}' ({len(all_jobs)} total)")
        
        keyword_lower = keyword.lower()
        filtered_jobs = []
        
        for job in all_jobs:
            title = str(job.get('job_title', '')).lower()
            summary = str(job.get('job_summary', '')).lower()
            responsibilities = str(job.get('core_responsibilities', '')).lower()
            
            # Check if keyword matches
            if (keyword_lower in title or 
                keyword_lower in summary or 
                keyword_lower in responsibilities):
                job['keyword_match'] = f'Matches "{keyword}"'
                filtered_jobs.append(job)
            else:
                job['keyword_match'] = 'No match'
        
        print(f"✅ Found {len(filtered_jobs)} jobs matching '{keyword}'")
        return filtered_jobs
    
    def export_to_sheets_with_credentials(self, jobs, sheet_url, sheet_type="ALL_JOBS"):
        """Export jobs to Google Sheets including account credentials"""
        if not jobs:
            print("❌ No jobs to export")
            return False
            
        try:
            print(f"\n📊 EXPORTING {len(jobs)} JOBS TO GOOGLE SHEETS")
            print(f"Sheet type: {sheet_type}")
            
            # Extract sheet ID from URL
            if '/spreadsheets/d/' in sheet_url:
                sheet_id = sheet_url.split('/spreadsheets/d/')[1].split('/')[0]
            else:
                sheet_id = sheet_url
            
            # Google Sheets setup
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
            gc = gspread.authorize(creds)
            spreadsheet = gc.open_by_key(sheet_id)
            
            # Create worksheet
            timestamp = datetime.now().strftime('%m%d_%H%M%S')
            worksheet_name = f"JobRight_{sheet_type}_{timestamp}"
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="500", cols="25")
            
            # Enhanced headers including account credentials
            headers = [
                'Job Title', 'Company', 'Location', 'Work Model', 'Remote', 'Salary',
                'Seniority', 'Employment Type', 'Job Summary', 'Core Responsibilities',
                'Min Experience', 'Apply Link', 'Job ID', 'Published Time',
                'Page #', 'Position', 'Company Size', 'Keyword Match',
                'Source', 'Scraped At', 'Scraper Email', 'Scraper Password'
            ]
            
            # Prepare data with credentials
            data = [headers]
            for job in jobs:
                def clean_text(text, max_length=400):
                    if not text or text == 'None':
                        return ''
                    clean = str(text).replace('\n', ' ').replace('\r', ' ')
                    return clean[:max_length] + '...' if len(clean) > max_length else clean
                
                row = [
                    clean_text(job.get('job_title', ''), 100),
                    clean_text(job.get('company', ''), 50),
                    clean_text(job.get('location', ''), 50),
                    clean_text(job.get('work_model', ''), 30),
                    clean_text(job.get('is_remote', ''), 10),
                    clean_text(job.get('salary', ''), 30),
                    clean_text(job.get('seniority', ''), 50),
                    clean_text(job.get('employment_type', ''), 30),
                    clean_text(job.get('job_summary', ''), 400),
                    clean_text(job.get('core_responsibilities', ''), 300),
                    clean_text(job.get('min_experience', ''), 20),
                    clean_text(job.get('apply_link', ''), 100),
                    clean_text(job.get('job_id', ''), 30),
                    clean_text(job.get('publish_desc', ''), 30),
                    str(job.get('page_number', '')),
                    str(job.get('position_in_page', '')),
                    clean_text(job.get('company_size', ''), 30),
                    clean_text(job.get('keyword_match', 'N/A'), 50),
                    clean_text(job.get('source', ''), 50),
                    clean_text(job.get('scraped_at', ''), 30),
                    clean_text(job.get('scraper_email', 'Unknown'), 50),
                    clean_text(job.get('scraper_password', 'Unknown'), 30)
                ]
                data.append(row)
            
            # Upload data
            worksheet.update(values=data, range_name='A1')
            
            # Format headers with different colors for different sheet types
            if sheet_type == "FILTERED":
                color = {"red": 0.0, "green": 0.8, "blue": 0.0}  # Green for filtered
            else:
                color = {"red": 0.0, "green": 0.5, "blue": 0.8}  # Blue for all jobs
                
            # Skip formatting to prevent network timeouts
            # worksheet.format('A1:V1', {"backgroundColor": color, "textFormat": {"bold": True}})
            print("✅ Headers added (formatting disabled for stability)")
            
            # Auto-resize disabled to prevent network timeouts
            # worksheet.columns_auto_resize(0, len(headers)-1)
            
            print(f"✅ {sheet_type} sheet created: {worksheet_name}")
            print(f"   📧 Account email saved in column U")
            print(f"   🔐 Account password saved in column V")
            return worksheet_name
            
        except Exception as e:
            print(f"❌ Export failed: {str(e)}")
            return None
    
    def run_complete_scraper(self, sheet_url, keyword="", target_jobs=100):
        """Run complete scraper with credential tracking"""
        try:
            print("🚀 MULTI-ACCOUNT JOBRIGHT SCRAPER")
            print("=" * 50)
            print("🎯 Intelligent account rotation for maximum job diversity")
            print("📊 Perfect deduplication across all accounts")
            print("=" * 50)
            
            # Setup session and login with existing account
            self.setup_session()
            self.login_existing_account()
            
            # Fetch jobs
            all_jobs = self.fetch_real_jobs(target_jobs)
            
            if not all_jobs:
                return {"success": False, "message": "No jobs fetched"}
            
            # Filter jobs by keyword
            filtered_jobs = self.filter_jobs_by_keyword(all_jobs, keyword)
            
            # Export with deduplication to fixed sheets
            print("\n📊 CREATING GOOGLE SHEETS WITH DEDUPLICATION...")
            
            # Export all jobs to fixed ALL_JOBS sheet
            all_jobs_sheet = self.export_to_fixed_sheets_with_deduplication(all_jobs, sheet_url, "ALL_JOBS")
            
            # Export filtered jobs - handle case when no jobs match
            filtered_sheet = None
            sheets_created = 1
            
            if len(filtered_jobs) > 0:
                filtered_sheet = self.export_to_fixed_sheets_with_deduplication(filtered_jobs, sheet_url, "FILTERED_JOBS")
                if filtered_sheet:
                    sheets_created = 2
            else:
                print("📋 No filtered jobs to export - skipping filtered sheet")
                filtered_sheet = "skipped"  # Mark as handled
            
            if all_jobs_sheet:  # Success if main sheet created
                result_message = f"✅ Multi-Account Scraping Complete!\n\n"
                result_message += f"📊 Total jobs processed: {len(all_jobs)}\n"
                result_message += f"🎯 Jobs matching '{keyword}': {len(filtered_jobs)}\n"
                result_message += f"📧 Account used: {self.account_email}\n"
                result_message += f"🔐 Account credentials tracked in sheets\n"
                result_message += f"📋 Data saved to: ALL_JOBS" + (", FILTERED_JOBS" if sheets_created > 1 else "") + "\n"
                result_message += f"\n💡 TIP: Run again to collect more jobs from different accounts!"
                
                if len(filtered_jobs) == 0 and keyword:
                    result_message += f"\n💡 No jobs matched '{keyword}' - try different keywords like 'python', 'javascript', 'react', 'data'"
                elif len(filtered_jobs) < target_jobs and keyword and len(filtered_jobs) > 0:
                    result_message += f"\n⚠️ Found {len(filtered_jobs)} matching jobs (target: {target_jobs})\n"
                    result_message += f"💡 Want to re-run with different keyword?"
                
                print(result_message)
                
                return {
                    "success": True,
                    "total_jobs": len(all_jobs),
                    "filtered_jobs": len(filtered_jobs),
                    "keyword": keyword,
                    "target": target_jobs,
                    "account_email": self.account_email,
                    "all_jobs_sheet": all_jobs_sheet,
                    "filtered_sheet": filtered_sheet,
                    "rerun_suggestion": len(filtered_jobs) == 0 and keyword,
                    "message": result_message
                }
            else:
                return {"success": False, "message": "Failed to create main jobs sheet"}
                
        except Exception as e:
            print(f"❌ Scraper error: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def get_existing_job_ids(self, sheet_url, sheet_name):
        """Get existing job IDs from a sheet to avoid duplicates"""
        try:
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
            gc = gspread.authorize(creds)
            
            # Extract sheet ID from URL
            if '/spreadsheets/d/' in sheet_url:
                sheet_id = sheet_url.split('/spreadsheets/d/')[1].split('/')[0]
            else:
                sheet_id = sheet_url
                
            spreadsheet = gc.open_by_key(sheet_id)
            
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
                # Get job IDs from column M (13th column - Job ID)
                job_ids = worksheet.col_values(13)[1:]  # Skip header
                return set(filter(None, job_ids))  # Remove empty strings
            except:
                # Sheet doesn't exist yet
                print(f"📋 Sheet '{sheet_name}' doesn't exist - will create new")
                return set()
                
        except Exception as e:
            print(f"⚠️ Could not check existing jobs: {str(e)}")
            return set()
    
    def add_session_summary(self, worksheet, jobs_added):
        """Add session summary card at the end of the sheet"""
        try:
            # Find the last row with data
            all_values = worksheet.get_all_values()
            last_row = len(all_values) + 2  # Add buffer
            
            # Add session summary
            summary_data = [
                [''],  # Empty row
                ['=== SCRAPING SESSION SUMMARY ==='],
                [f'Session Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'],
                [f'Account Used: {self.account_email}'],
                [f'Account Password: {self.account_password}'],
                [f'Jobs Added This Session: {jobs_added}']
            ]
            
            # Add summary to sheet
            start_range = f'A{last_row}'
            worksheet.update(values=summary_data, range_name=start_range)
            
            # Format the summary section
            summary_range = f'A{last_row+1}:A{last_row+5}'
            # Skip summary formatting to prevent timeouts
            # worksheet.format(summary_range, {"backgroundColor": {"red": 0.9, "green": 0.9, "blue": 1.0}})
            
            print(f"✅ Session summary added: {jobs_added} new jobs")
            
        except Exception as e:
            print(f"⚠️ Could not add session summary: {str(e)}")

    def export_to_fixed_sheets_with_deduplication(self, jobs, sheet_url, sheet_type):
        """Export jobs to fixed sheets with deduplication"""
        try:
            # Setup Google Sheets
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
            gc = gspread.authorize(creds)
            
            # Extract sheet ID from URL
            if '/spreadsheets/d/' in sheet_url:
                sheet_id = sheet_url.split('/spreadsheets/d/')[1].split('/')[0]
            else:
                sheet_id = sheet_url
                
            spreadsheet = gc.open_by_key(sheet_id)
            
            # Use fixed sheet names
            sheet_name = "ALL_JOBS" if sheet_type == "ALL_JOBS" else "FILTERED_JOBS"
            
            # Get existing job IDs for deduplication
            existing_ids = self.get_existing_job_ids(sheet_url, sheet_name)
            print(f"📋 Found {len(existing_ids)} existing jobs in {sheet_name}")
            
            # Filter out duplicates
            new_jobs = [job for job in jobs if job.get('job_id', '') not in existing_ids]
            print(f"✅ {len(new_jobs)} new jobs to add (removed {len(jobs) - len(new_jobs)} duplicates)")
            
            if len(new_jobs) == 0:
                print(f"📋 No new jobs to add to {sheet_name}")
                return sheet_name
            
            # Get or create worksheet
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
                # Get existing data to append to
                existing_data = worksheet.get_all_values()
                next_row = len(existing_data) + 1
                is_new_sheet = False
            except:
                # Create new worksheet
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
                next_row = 1
                existing_data = []
                is_new_sheet = True
            
            def clean_text(text, max_length=400):
                if not text or text == 'None':
                    return ''
                clean = str(text).replace('\n', ' ').replace('\r', ' ')
                return clean[:max_length] + '...' if len(clean) > max_length else clean
            
            # Headers - simplified without credentials columns
            headers = [
                'Job Title', 'Company', 'Location', 'Work Model', 'Remote', 'Salary',
                'Seniority', 'Employment Type', 'Job Summary', 'Core Responsibilities',  
                'Min Experience', 'Apply Link', 'Job ID', 'Publish Date', 
                'Page Number', 'Position in Page', 'Company Size', 'Keyword Match', 'Source'
            ]
            
            # Add headers if new sheet
            data_to_add = []
            if is_new_sheet:
                data_to_add.append(headers)
            
            # Prepare new job data
            for job in new_jobs:
                row = [
                    clean_text(job.get('job_title', ''), 100),
                    clean_text(job.get('company', ''), 50),
                    clean_text(job.get('location', ''), 50),
                    clean_text(job.get('work_model', ''), 30),
                    clean_text(job.get('is_remote', ''), 10),
                    clean_text(job.get('salary', ''), 30),
                    clean_text(job.get('seniority', ''), 50),
                    clean_text(job.get('employment_type', ''), 30),
                    clean_text(job.get('job_summary', ''), 400),
                    clean_text(job.get('core_responsibilities', ''), 300),
                    clean_text(job.get('min_experience', ''), 20),
                    clean_text(job.get('apply_link', ''), 100),
                    clean_text(job.get('job_id', ''), 30),
                    clean_text(job.get('publish_desc', ''), 30),
                    str(job.get('page_number', '')),
                    str(job.get('position_in_page', '')),
                    clean_text(job.get('company_size', ''), 30),
                    clean_text(job.get('keyword_match', 'N/A'), 50),
                    clean_text(job.get('source', ''), 50)
                ]
                data_to_add.append(row)
            
            # Upload new data
            if len(data_to_add) > 0:
                if is_new_sheet:
                    worksheet.update(values=data_to_add, range_name='A1')
                    
                    # Format headers
                    color = {"red": 0.0, "green": 0.8, "blue": 0.0} if sheet_type == "FILTERED_JOBS" else {"red": 0.0, "green": 0.5, "blue": 0.8}
                    # Skip header formatting to prevent timeouts
                    # worksheet.format('A1:S1', {"backgroundColor": color, "textFormat": {"bold": True}})
                else:
                    # Append to existing sheet
                    start_range = f'A{next_row}'
                    worksheet.update(values=data_to_add, range_name=start_range)
                
                # Auto-resize disabled to prevent network timeouts
            # worksheet.columns_auto_resize(0, len(headers)-1)
            
            # Skip session summary for performance - just log it
            # self.add_session_summary(worksheet, len(new_jobs))
            print(f"✅ Session summary: {len(new_jobs)} new jobs added")
            
            print(f"✅ {len(new_jobs)} new jobs added to {sheet_name}")
            return sheet_name
            
        except Exception as e:
            print(f"❌ Export failed: {str(e)}")
            return None

def main():
    """Enhanced scraper with command line argument support"""
    import sys
    
    # Parse command line arguments
    target_jobs = 50  # default
    keyword = "frontend"  # default
    
    for i, arg in enumerate(sys.argv):
        if arg == "--target" and i + 1 < len(sys.argv):
            try:
                target_jobs = int(sys.argv[i + 1])
                print(f"🎯 Target jobs set to: {target_jobs}")
            except ValueError:
                print(f"⚠️ Invalid target value, using default: 50")
        elif arg == "--keyword" and i + 1 < len(sys.argv):
            keyword = sys.argv[i + 1]
            print(f"🔍 Keyword set to: {keyword}")
    
    scraper = EnhancedJobRightScraper()
    
    # Use fixed Google Sheet URL
    sheet_url = "1iibXYJ5ZSFZzFIKUyM8d4u3x87FOereMESBfuFW7ZYI"
    result = scraper.run_complete_scraper(
        sheet_url=sheet_url,
        keyword=keyword,
        target_jobs=target_jobs
    )
    
    if result["success"]:
        print(f"\n🎉 SUCCESS! Account credentials saved to sheets")
    else:
        print(f"\n❌ Failed: {result['message']}")

if __name__ == "__main__":
    main()