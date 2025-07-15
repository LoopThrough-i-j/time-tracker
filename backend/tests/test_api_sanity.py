import time
from datetime import datetime

import requests
from config import API_BASE_URL, BASE_URL, HEADERS, TEST_DATA

# Global flag for request/response logging
ENABLE_REQUEST_LOGGING = False


def log_request_response(method, url, request_data=None, headers=None, response=None):
    """Log request and response details if logging is enabled"""
    if not ENABLE_REQUEST_LOGGING:
        return
    
    print(f"\n📡 {method.upper()} {url}")
    
    if headers:
        print(f"   Headers: {headers}")
    
    if request_data:
        print(f"   Request: {request_data}")
    
    if response:
        print(f"   Status: {response.status_code}")
        try:
            response_json = response.json()
            print(f"   Response: {response_json}")
        except:
            print(f"   Response: {response.text[:200]}...")
    print("=" * 50)


def get_auth_token(employee_id):
    """Get authentication token for the employee"""
    try:
        # Step 1: Get a signup link
        signup_link_data = {"employee_id": employee_id, "expiry_hours": 24}
        signup_response = requests.post(f"{API_BASE_URL}/auth/get-signup-link", headers=HEADERS, json=signup_link_data)
        log_request_response("POST", f"{API_BASE_URL}/auth/get-signup-link", signup_link_data, HEADERS, signup_response)
        
        print(f"Signup link response: {signup_response.status_code}")
        if signup_response.status_code != 200:
            print(f"Signup link failed: {signup_response.text}")
            return None
            
        signup_data = signup_response.json()
        signup_url = signup_data["signup_link"]  # Use the correct field name
        # Extract token from URL (format: /auth/signup?token=TOKEN)
        token = signup_url.split("token=")[1] if "token=" in signup_url else None
        if not token:
            print("Failed to extract token from signup URL")
            return None
            
        print(f"Extracted token: {token[:20]}...")
        
        # Step 2: Use the token to signup via the HTML form endpoint
        signup_form_data = {
            "token": token,
            "email": TEST_DATA["employee"]["email"],
            "password": TEST_DATA["auth"]["password"]
        }
        
        # Use form data instead of JSON for the HTML form endpoint
        signup_form_headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        signup_form_response = requests.post(f"{BASE_URL}/auth/signup", headers=signup_form_headers, data=signup_form_data)
        log_request_response("POST", f"{BASE_URL}/auth/signup", signup_form_data, signup_form_headers, signup_form_response)
        
        print(f"Signup form response: {signup_form_response.status_code}")
        if signup_form_response.status_code not in [200, 302]:  # 302 might be a redirect to success page
            print(f"Signup form failed: {signup_form_response.text[:200]}")
            return None
            
        print("✅ Employee password set successfully")
        
        # Step 3: Login to get the JWT token
        login_data = {"email": TEST_DATA["employee"]["email"], "password": TEST_DATA["auth"]["password"]}
        login_response = requests.post(f"{API_BASE_URL}/auth/login", headers=HEADERS, json=login_data)
        log_request_response("POST", f"{API_BASE_URL}/auth/login", login_data, HEADERS, login_response)
        
        print(f"Login response: {login_response.status_code}")
        if login_response.status_code == 200:
            auth_data = login_response.json()
            access_token = auth_data.get("access_token")
            print("✅ Login successful, access token obtained")
            return access_token
        else:
            print(f"Login failed: {login_response.text}")
            
        return None
    except Exception as e:
        print(f"Auth error: {e}")
        return None


def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_employee_crud():
    print("\n--- Testing Employee CRUD ---")

    try:
        response = requests.post(f"{API_BASE_URL}/employee/", headers=HEADERS, json=TEST_DATA["employee"])
        log_request_response("POST", f"{API_BASE_URL}/employee/", TEST_DATA["employee"], HEADERS, response)

        if response.status_code == 200:
            employee = response.json()
            employee_id = employee["id"]
            print(f"✅ Employee created: {employee_id}")

            get_response = requests.get(f"{API_BASE_URL}/employee/{employee_id}", headers=HEADERS)
            log_request_response("GET", f"{API_BASE_URL}/employee/{employee_id}", None, HEADERS, get_response)
            if get_response.status_code == 200:
                print("✅ Employee retrieved successfully")
            else:
                print(f"❌ Employee retrieval failed: {get_response.status_code}")

            list_response = requests.get(f"{API_BASE_URL}/employee/", headers=HEADERS)
            log_request_response("GET", f"{API_BASE_URL}/employee/", None, HEADERS, list_response)
            if list_response.status_code == 200:
                print("✅ Employee list retrieved successfully")
            else:
                print(f"❌ Employee list failed: {list_response.status_code}")

            return employee_id
        else:
            print(f"❌ Employee creation failed: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"❌ Employee CRUD error: {e}")
        return None


def test_project_crud(employee_id):
    print("\n--- Testing Project CRUD ---")

    if not employee_id:
        print("❌ Skipping project tests - no employee ID")
        return None

    try:
        project_data = {**TEST_DATA["project"], "employees": [employee_id]}

        response = requests.post(f"{API_BASE_URL}/project/", headers=HEADERS, json=project_data)

        if response.status_code == 200:
            project = response.json()
            project_id = project["id"]
            print(f"✅ Project created: {project_id}")

            get_response = requests.get(f"{API_BASE_URL}/project/{project_id}", headers=HEADERS)
            if get_response.status_code == 200:
                print("✅ Project retrieved successfully")
            else:
                print(f"❌ Project retrieval failed: {get_response.status_code}")

            return project_id
        else:
            print(f"❌ Project creation failed: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"❌ Project CRUD error: {e}")
        return None


def test_task_crud(project_id, employee_id):
    print("\n--- Testing Task CRUD ---")

    if not project_id or not employee_id:
        print("❌ Skipping task tests - missing project or employee ID")
        return None

    try:
        task_data = {**TEST_DATA["task"], "project_id": project_id, "employees": [employee_id]}

        response = requests.post(f"{API_BASE_URL}/task/", headers=HEADERS, json=task_data)

        if response.status_code == 200:
            task = response.json()
            task_id = task["id"]
            print(f"✅ Task created: {task_id}")

            get_response = requests.get(f"{API_BASE_URL}/task/{task_id}", headers=HEADERS)
            if get_response.status_code == 200:
                print("✅ Task retrieved successfully")
            else:
                print(f"❌ Task retrieval failed: {get_response.status_code}")

            return task_id
        else:
            print(f"❌ Task creation failed: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"❌ Task CRUD error: {e}")
        return None


def test_time_log_creation(employee_id, project_id, task_id):
    print("\n--- Testing Time Log Creation and Management ---")

    if not all([employee_id, project_id, task_id]):
        print("❌ Skipping time log tests - missing required IDs")
        return

    try:
        # Get authentication token
        token = get_auth_token(employee_id)
        if not token:
            print("❌ Failed to get authentication token - testing endpoint structure only")
            # Fallback to testing endpoint structure without auth
            auth_headers = {**HEADERS, "Authorization": "Bearer dummy_token"}
            
            start_time_log_data = {
                "type": "manual",
                "projectId": project_id,
                "taskId": task_id,
                "timezoneOffset": -18000000,  # -5 hours in milliseconds
                "user": "testuser",
                "note": "Test time log entry",
                "operatingSystem": "macOS",
                "overtime": False
            }

            start_response = requests.post(f"{API_BASE_URL}/time-log/start", headers=auth_headers, json=start_time_log_data)
            
            if start_response.status_code == 401:
                print("✅ Time log start endpoint properly requires authentication")
            else:
                print(f"ℹ️ Time log start response: {start_response.status_code}")
            return

        # Full authentication flow successful - test complete time log functionality
        auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

        start_time_log_data = {
            "type": "manual",
            "projectId": project_id,
            "taskId": task_id,
            "timezoneOffset": -18000000,  # -5 hours in milliseconds
            "user": "testuser",
            "note": "Test time log entry",
            "operatingSystem": "macOS",
            "overtime": False
        }

        # Test starting a time log
        start_response = requests.post(f"{API_BASE_URL}/time-log/start", headers=auth_headers, json=start_time_log_data)
        log_request_response("POST", f"{API_BASE_URL}/time-log/start", start_time_log_data, auth_headers, start_response)

        if start_response.status_code == 200:
            time_log = start_response.json()
            time_log_id = time_log["id"]
            print(f"✅ Time log started successfully: {time_log_id}")
            
            # Verify the time log has start and end times (end should equal start for active logs)
            if time_log["start"] == time_log["end"]:
                print("✅ Active time log detected (start == end)")
            else:
                print("❌ Unexpected time log state")
                
            
            time.sleep(15)
            update_response = requests.put(f"{API_BASE_URL}/time-log/{time_log_id}/update", headers=auth_headers)
            log_request_response("PUT", f"{API_BASE_URL}/time-log/{time_log_id}/update", None, auth_headers, update_response)
            
            if update_response.status_code == 200:
                updated_log = update_response.json()
                print("✅ Time log updated/stopped successfully")
                
                # Verify the time log now has different start and end times
                if updated_log["start"] != updated_log["end"]:
                    duration = updated_log["end"] - updated_log["start"]
                    print(f"✅ Completed time log detected (duration: {duration}ms)")
                else:
                    print("❌ Time log was not properly stopped")
            else:
                print(f"❌ Time log update failed: {update_response.status_code} - {update_response.text}")
        else:
            print(f"❌ Time log creation failed: {start_response.status_code} - {start_response.text}")

    except Exception as e:
        print(f"❌ Time log error: {e}")


def test_analytics_endpoints():
    print("\n--- Testing Analytics Endpoints ---")
    
    try:
        now = datetime.now()
        start_time = int((now.timestamp() - 3600) * 1000)  # 1 hour ago
        end_time = int(now.timestamp() * 1000)  # now
        
        # Test window analytics
        window_response = requests.get(
            f"{API_BASE_URL}/analytics/window?start={start_time}&end={end_time}",
            headers=HEADERS
        )
        log_request_response("GET", f"{API_BASE_URL}/analytics/window?start={start_time}&end={end_time}", None, HEADERS, window_response)
        
        if window_response.status_code == 200:
            print("✅ Window analytics endpoint working")
        else:
            print(f"⚠️ Window analytics returned {window_response.status_code} (may need debugging)")
            print(f"   Response: {window_response.text[:100]}...")
            
        # Test project time analytics
        project_response = requests.get(
            f"{API_BASE_URL}/analytics/project-time?start={start_time}&end={end_time}",
            headers=HEADERS
        )
        log_request_response("GET", f"{API_BASE_URL}/analytics/project-time?start={start_time}&end={end_time}", None, HEADERS, project_response)
        
        if project_response.status_code == 200:
            print("✅ Project time analytics endpoint working")
        else:
            print(f"❌ Project time analytics failed: {project_response.status_code}")
            
    except Exception as e:
        print(f"❌ Analytics error: {e}")


def main():
    global ENABLE_REQUEST_LOGGING
    
    print("🚀 Starting API Sanity Tests")
    print("=" * 50)
    
    # Ask user about request/response logging
    log_choice = input("Do you want to enable detailed request/response logging? (y/n): ").lower().strip()
    if log_choice in ['y', 'yes']:
        ENABLE_REQUEST_LOGGING = True
        print("✅ Request/response logging enabled")
    else:
        print("❌ Request/response logging disabled")
    
    print("=" * 50)

    if not test_health():
        print("❌ Health check failed - aborting tests")
        return

    employee_id = test_employee_crud()
    project_id = test_project_crud(employee_id)
    task_id = test_task_crud(project_id, employee_id)
    test_time_log_creation(employee_id, project_id, task_id)
    test_analytics_endpoints()

    print("\n" + "=" * 50)
    print("🏁 API Sanity Tests Completed")


if __name__ == "__main__":
    main()
