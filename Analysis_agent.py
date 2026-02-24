
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
prompt = """You are a resume Score predictor based on Job description and Resume and the score must be accuratly calculate. You will be given a job description in text format and a resume in Json format. Your task is to analyze the resume and predict a score between 0 to 100 that indicates how well the resume matches the job description. Consider factors such as relevant skills, experience, education, and keywords from the job description when calculating the score. Return only the predicted score as an integer with reason why the score was assigned."""
path="D:\\Projects\\resume_output.json"
jd_path="D:\\Projects\\jd.txt"

# Read files with proper encoding
with open(path, "r", encoding="utf-8") as f:
    resume_content = f.read()

with open(jd_path, "r", encoding="utf-8") as f:
    jd_content = f.read()

messages = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": f"Analyze the following resume and predict a score based on the job description\n\nResume Content:\n\n{resume_content}\n\nJob Description:\n{jd_content}"},
]
# Initialize the HuggingFace client
client = InferenceClient(
    model="meta-llama/Llama-3.3-70B-Instruct",
    token=os.getenv("HF_TOKEN"),
)
# Call the LLM API
print("Sending to LLM for parsing...")
print("-" * 50)
response = client.chat_completion(messages=messages, max_tokens=2048)
llm_output = response.choices[0].message.content

print("LLM Response:")
print(llm_output)
print()