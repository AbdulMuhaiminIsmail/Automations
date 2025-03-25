# Handling unicode encoding issues in Windows
import sys 
sys.stdout.reconfigure(encoding='utf-8')

# Importing required libraries
import os
import json
import time
import shutil
import pandas as pd
from Helpers.gemini import generate_response
from Helpers.extract_text import extract_text_from_pdf
from Helpers.job_description import seo_job_description

# Define directories
input_folder = "../SEO/SEO Resumes"
shortlisted_folder = "../SEO/SEO Shortlisted"
rejected_folder = "../SEO/SEO Rejected"
os.makedirs(shortlisted_folder, exist_ok=True)
os.makedirs(rejected_folder, exist_ok=True)

# Function to analyze resume using Gemini
def analyze_resume(resume_text):
    prompt = f"""
    You are an expert in resume screening and hiring. Your task is to analyze a candidate's resume against the given job description and provide a structured evaluation.

    Here is the job description you need to match the candidate's resume with:
    {seo_job_description}
    
    ## **Rules (STRICT COMPLIANCE REQUIRED)**
    1. **Experience Requirement (MANDATORY FILTER - DO NOT SKIP)**:
    - The candidate **MUST** have at least **3 years of SEO experience**.
    - If the candidate has **less than 3 years of experience**, return the following JSON:
        ```json
        {{
        "score": -1,
        "comment": "The candidate does not meet the minimum required experience of 3 years. No further evaluation performed."
        }}
        ```
    - **DO NOT proceed with further evaluation** if this condition is not met.

    2. **Skills & Expertise Matching (Only if 3+ Years Experience)**:
    - Identify relevant SEO skills:
        - On-page, Off-page, and Technical SEO.
        - SEO tools: Ahrefs, SEMrush, Google Search Console, GA4, Moz, Screaming Frog.
        - Experience with international markets (USA/Canada preferred).

    3. **Relevance Score Assignment (Only if 3+ Years Experience)**:
    - If the candidate meets the **minimum experience requirement (3+ years)**, assign a **score between 1 and 10**:
        - **1-3**: Weak match (some SEO skills but lacks key competencies).
        - **4-6**: Moderate match (relevant experience but missing some preferred skills).
        - **7-8**: Strong match (highly relevant skills and experience).
        - **9-10**: Excellent match (perfect alignment with job description).

    4. **Candidate Summary**:
    - Provide a **brief, structured comment** explaining **why the candidate is a good or poor fit**.

    ---

    ## **Resume Text:**
    {resume_text}

    ## **STRICT OUTPUT FORMAT (DO NOT DEVIATE)**
    - **DO NOT** include any additional text, explanations, or formatting.
    - **Return ONLY a valid JSON object** following this exact structure:
    ```json
    {{
    "score": X,
    "comment": "Brief evaluation of the candidate's suitability, strengths, and weaknesses."
    }}
    ```
    """

    try:
        response = generate_response(prompt)
    except:
        score, comment = 0, "Error in generating AI response."
        return score, comment

    try:
        response = json.loads(response)
        score = response["score"]
        comment = response["comment"]
    except Exception as e:
        print(f"Error occured while AI response parsing: {str(e)}")
        score, comment = 0, "Error in AI response parsing."

    return score, comment

def main():
    results = []

    start_time = time.time()
    print("🚀 Resume Screening Started!")

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            try:
                print(f"Processing file: {filename}")
                file_path = os.path.join(input_folder, filename)
                resume_text = extract_text_from_pdf(file_path)
                
                # Analyze with Gemini
                score, comment = analyze_resume(resume_text)

                # Move file based on score
                if score == 0:
                    pass
                elif score == -1:
                    shutil.move(file_path, os.path.join(rejected_folder, filename))
                # elif score < 6:
                #     shutil.move(file_path, os.path.join(rejected_folder, filename))
                else:
                    shutil.move(file_path, os.path.join(shortlisted_folder, filename))

                # Store result
                results.append({"Filename": filename, "Score": score, "Comment": comment})
            except Exception as e:
                print(f"Error processing file '{filename}': {str(e)}")

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv("seo_results.csv", index=False)

    end_time = time.time()
    seconds_elapsed = end_time - start_time

    if (seconds_elapsed < 60):
        print(f"⏱️ Elapsed Time: {seconds_elapsed:.2f} seconds")
    else:
        minutes_elapsed = (end_time - start_time) / 60
        seconds_elapsed = (end_time - start_time) % 60
        print(f"⏱️ Elapsed Time: {minutes_elapsed:.0f} minutes {seconds_elapsed:.2f} seconds")
        
    print("✅ SEO Resume Screening Completed! Check the 'Shortlisted' folder & CSV report.")


if __name__ == "__main__":
    main()
