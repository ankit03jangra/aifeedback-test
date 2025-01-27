import requests
import os
import sys

GITHUB_TOKEN = os.getenv("YOUR_GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN is not set.")
    sys.exit(1)  # Exit with error

REPO = "ankit03jangra/aifeedback-test"
PR_NUMBER = os.getenv("PR_NUMBER")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

def post_comment(comment):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    payload = {"body": comment}
    print(url)
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print(f"Failed to post comment: {response.text}")

feedback_combined = ""

# Iterate through all files in the artifact directory
for file_name in os.listdir("results"):
    file_path = os.path.join("results", file_name)
    if os.path.isfile(file_path):  # Process only files
        try:
            with open(file_path, "r") as feedback_file:
                comment = feedback_file.read()
                feedback_combined += f"### Feedback for {file_name}\n{comment}\n\n"
        except Exception as e:
            print(f"Error reading or posting comment for {file_path}: {e}")

if feedback_combined:
    post_comment(feedback_combined)
else:
    print("No feedback to post.")