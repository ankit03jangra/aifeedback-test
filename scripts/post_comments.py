import requests
import os

GITHUB_TOKEN = os.getenv("YOUR_GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN is not set.")
    sys.exit(1)  # Exit with error

REPO = "ankit03jangra/aifeedback-test"
PR_NUMBER = 1  # Replace with the pull request number

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

with open("results/ai-feedback.txt", "r") as feedback_file:
    comment = feedback_file.read()

post_comment(comment)
