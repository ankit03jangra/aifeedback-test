from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Get the list of updated files from the latest commit
def get_updated_files():
    try:
        # Fetch the list of files changed in the latest commit or pull request
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Return only files with specific extensions
        files = [f for f in result.stdout.splitlines() if f.endswith(('.java', '.py'))]
        return files
    except Exception as e:
        print(f"Error retrieving updated files: {e}")
        return []

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