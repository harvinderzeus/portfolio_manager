import requests
import time
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

DATABRICKS_INSTANCE = "https://adb-1883699785453254.14.azuredatabricks.net"
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_JOB_ID = "63234248856896"

def run_db_job(confidence_level):
    # Step 1: Trigger the Databricks job
    url = f"{DATABRICKS_INSTANCE}/api/2.1/jobs/run-now"
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}"
    }
    json_data = {
        "job_id": DATABRICKS_JOB_ID,
        "notebook_params": {
            "confidence_level": str(confidence_level)  # Passing confidence level
        }
    }
    
    response = requests.post(url, headers=headers, json=json_data)
    
    if response.status_code == 200:
        run_id = response.json()['run_id']  # Get run_id from the response
        
        # Step 2: Poll the job status using the run_id
        status_url = f"{DATABRICKS_INSTANCE}/api/2.1/jobs/runs/get"
        while True:
            status_response = requests.get(status_url, headers=headers, params={"run_id": run_id})
            
            if status_response.status_code == 200:
                state = status_response.json()['state']['life_cycle_state']
                if state == 'TERMINATED':
                    # Job is completed, check result
                    result_state = status_response.json()['state']['result_state']
                    if result_state == 'SUCCESS':
                        return True  # Job completed successfully
                    else:
                        return False  # Job failed
                elif state in ['PENDING', 'RUNNING']:
                    # Job is still running, wait and poll again
                    time.sleep(10)  # Wait for 10 seconds before polling again
            else:
                print("Error getting job status")
                return False
    else:
        print("Error triggering job")
        return False


# # Example usage:

# confidence_level = 0.95  # Example confidence level

# # Trigger the job and wait for it to complete, returning True if successful, False if failed
# job_completed = run_db_job_and_poll(confidence_level)

# if job_completed:
#     print("Job completed successfully")
# else:
#     print("Job failed or error occurred")
