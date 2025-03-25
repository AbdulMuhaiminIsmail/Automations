# Handling unicode encoding issues in Windows
import os
import sys 
sys.stdout.reconfigure(encoding='utf-8')

# Get the parent directory (go up one level)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# Importing required libraries
import os
import json
import time
import shutil
import pandas as pd
from Helpers.gemini import generate_response
from Helpers.extract_text import extract_text_from_pdf
from Helpers.job_description import uiux_job_description

# Define directories
input_folder = "Departments/UIUX/UIUX Resumes"
shortlisted_folder = "Departments/UIUX/UIUX Shortlisted"
rejected_folder = "Departments/UIUX/UIUX Rejected"
os.makedirs(shortlisted_folder, exist_ok=True)
os.makedirs(rejected_folder, exist_ok=True)

# Function to analyze resume using Gemini
def analyze_resume(resume_text):
    prompt = f"""
    You are an expert in resume screening and hiring. Your task is to analyze a candidate's resume against the given UI/UX Designer job description and provide a structured evaluation.

    ### **Job Description:**
    {uiux_job_description}

    ---

    ## **STRICT SCREENING RULES (MANDATORY COMPLIANCE REQUIRED)**

    ### **1. Experience Requirement (MANDATORY FILTER - DO NOT SKIP)**
    - The candidate **MUST** have at least **3 years of UI/UX design experience**.
    - If the candidate has **less than 3 years of experience**, return the following JSON **without performing further evaluation**:
        ```json
        {{
        "score": -1,
        "comment": "The candidate does not meet the minimum required experience of 3 years. No further evaluation performed."
        }}
        ```

    ### **2. Instant Rejection Criteria (IF ANY CONDITION IS MET, REJECT IMMEDIATELY)**
    - **No experience** with **international clients** or **e-commerce projects**.
    - **No proficiency** in **Adobe XD, Figma, or Sketch**.
    - **Weak or no portfolio** showcasing UI/UX & marketing designs.
    - **No experience** in **marketing design (emails, social media, ads)**.

    If the resume meets **any** of the above rejection conditions, return:
    ```json
    {{
    "score": -1,
    "comment": "The candidate does not meet the mandatory requirements (e.g., no international/e-commerce experience, missing design tool proficiency, weak portfolio, or no marketing design experience). No further evaluation performed."
    }}
    ```

    ### **3. Skills & Expertise Matching (Only if Candidate Passes Above Filters)**
    - **Required UI/UX Skills**:
    - **Design Tools**: Proficiency in **Adobe XD, Figma, or Sketch**.
    - **UI/UX Design**: Experience in **wireframes, prototypes, mockups**.
    - **Marketing Design**: Experience in **email designs, social media, ads**.
    - **User Research & Usability Testing**.
    - **Responsive Design & Accessibility Best Practices**.
    - **Collaboration**: Ability to work with developers & marketing teams.

    ### **4. Relevance Score Assignment (Only if Candidate Passes Above Filters)**
    - Assign a **score between 1 and 10**:
        - **1-3**: Weak match (some UI/UX experience but lacks key competencies).
        - **4-6**: Moderate match (relevant experience but missing some preferred skills).
        - **7-8**: Strong match (highly relevant skills and experience).
        - **9-10**: Excellent match (perfect alignment with job description).

    ### **5. Candidate Summary**
    - Provide a **brief, structured comment** explaining **why the candidate is a good or poor fit**.
    - Highlight **key strengths and weaknesses** relevant to the job.

    ---

    ## **Resume Text:**
    {resume_text}

    ---

    ## **STRICT OUTPUT FORMAT (DO NOT DEVIATE)**
    - **DO NOT** include any additional text, explanations, or formatting.
    - **Return ONLY a valid JSON object** in this exact structure:
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
    df.to_csv("uiux_results.csv", index=False)

    end_time = time.time()
    seconds_elapsed = end_time - start_time

    if (seconds_elapsed < 60):
        print(f"⏱️ Elapsed Time: {seconds_elapsed:.2f} seconds")
    else:
        minutes_elapsed = (end_time - start_time) / 60
        seconds_elapsed = (end_time - start_time) % 60
        print(f"⏱️ Elapsed Time: {minutes_elapsed:.0f} minutes {seconds_elapsed:.2f} seconds")
        
    print("✅ UI/UX Resume Screening Completed! Check the 'Shortlisted' folder & CSV report.")


if __name__ == "__main__":
    main()
