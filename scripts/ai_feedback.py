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
                    {"role": "user", "content": f"Analyze the following code and provide feedback:\n\n{code}"}
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

# Example usage
feedback = analyze_code("src/main/java/com/javatechie/DevopsIntegrationApplication.java")
os.makedirs("results", exist_ok=True)  # Ensure the output directory exists
with open("results/ai-feedback.txt", "w") as output_file:
   output_file.write(feedback)
print("AI feedback has been written to results/ai-feedback.txt")