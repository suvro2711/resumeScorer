import openai
import pdfplumber
import os

# Set up OpenAI API key
openai.api_key = "your_openai_api_key_here"

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
    return text

# Function to analyze and score the resume using OpenAI API
def score_resume(resume_text):
    prompt = f"""
    Please analyze the following resume and score it based on the following criteria:
    1. Relevant work experience
    2. Skills and expertise
    3. Education background
    4. Professional achievements and certifications
    Provide a score between 1 and 10 for each of the criteria and give an overall score at the end.

    Resume:
    {resume_text}

    Scoring:
    """

    try:
        # OpenAI API call for analysis and scoring
        response = openai.ChatCompletion.create(
            engine="text-davinci-003",  # You can replace with a different engine if needed
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )

        # Extracting the score from the response
        return response.choices[0].text.strip()

    except Exception as e:
        return f"Error scoring resume: {str(e)}"

# Main function to process PDF resumes in a directory
def process_resumes_in_directory(directory_path):
    resume_scores = {}

    # Iterate through all PDF files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            print(f"Processing {filename}...")

            # Extract text from PDF
            resume_text = extract_text_from_pdf(pdf_path)

            # Score the resume
            if resume_text.strip():  # Ensure there's text extracted
                score = score_resume(resume_text)
                resume_scores[filename] = score
                print(f"Score for {filename}: {score}")
            else:
                print(f"Error: No text extracted from {filename}.")

    return resume_scores

# Example usage
if __name__ == "__main__":
    directory = "path_to_your_pdf_directory"  # Replace with your folder path containing resumes
    scores = process_resumes_in_directory(directory)
    print("\nFinal Scores for Resumes:")
    for filename, score in scores.items():
        print(f"{filename}: {score}")
