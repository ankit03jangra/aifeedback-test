from openai import OpenAI
import os
import sys
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GITHUB_TOKEN = os.getenv("YOUR_GITHUB_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN is not set.")
    sys.exit(1)  # Exit with error

REPO = "ankit03jangra/aifeedback-test"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

# Replace with your OpenAI API key
def analyze_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
                    {"role": "system", "content": "You are an expert code reviewer."},
                    {"role": "user", "content": f"""
                                                            Analyze the following code and provide specific, actionable feedback within 150 words:
                                                            - Focus on readability, structure, and maintainability.
                                                            - Highlight best practices and areas for improvement.
                                                            - Identify potential bugs, performance issues, or edge cases.
                                                            - Suggest improvements for security and efficiency.
                                                            - Point out missing tests or documentation.

                                                            Do not summarize the code or provide generic feedback. Provide concise, actionable comments.

                                                            Code to review:
                                                            {code}
                                                        """}
                ],
        max_tokens=150,
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except client.error.RateLimitError:
        print("Rate limit exceeded. Retrying...")
        time.sleep(60)  # Retry after 60 seconds (you can adjust the wait time)
        return analyze_code(file_path)  # Retry the function after delay
    except client.error.AuthenticationError:
        print("Invalid API key. Please check your key and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_changed_files():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    changed_files = []

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files = response.json()
            for file in files:
                changed_files.append(file['filename'])
            return changed_files
        else:
            print(f"Failed to fetch changed files: {response.status_code} {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

updated_files = get_updated_files()
os.makedirs("results", exist_ok=True)  # Ensure the output directory exists
if updated_files:
    print(f"Found updated files: {updated_files}")
    for file_path in updated_files:
        feedback = analyze_code(file_path)
        if feedback:
            # Write feedback to a file named after the analyzed file
            output_file_path = os.path.join("results", f"{os.path.basename(file_path)}-feedback.txt")
            with open(output_file_path, "w") as output_file:
                output_file.write(feedback)
            print(f"Feedback for {file_path} has been written to {output_file_path}")
else:
    print("No updated files to analyze.")