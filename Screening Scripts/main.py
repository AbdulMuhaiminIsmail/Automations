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
from Helpers.prompts import seo_prompt, uiux_prompt
from Helpers.job_descriptions import seo_executive_job_description, uiux_designer_job_description

# Function to analyze resumes using Gemini
def analyze_resume(job_role, resume_text):
    prompts = {
        "seo": seo_prompt,
        "uiux": uiux_prompt
    }

    job_descriptions = {
        "seo executive": seo_executive_job_description,
        "uiux designer": uiux_designer_job_description
    }
    
    job_description = job_descriptions.get(job_role.lower())
    if not job_description:
        raise ValueError(f"Unsupported job description for role: {job_role}")
    
    prompt = prompts.get(job_role.lower())
    if not prompt:
        raise ValueError(f"Unsupported job role: {job_role}")
    
    # Write the values of placeholders in the prompt
    prompt = prompt.format(job_description=job_description, resume_text=resume_text)

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

def main(job_role, input_folder, shortlisted_folder, rejected_folder):
    results = []

    # Create folders if they don't exist
    os.makedirs(shortlisted_folder, exist_ok=True)
    os.makedirs(rejected_folder, exist_ok=True)

    # Start the screening process
    start_time = time.time()
    print(f"{job_role} Resume Screening Started!")

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            try:
                print(f"Processing file: {filename}")
                file_path = os.path.join(input_folder, filename)
                resume_text = extract_text_from_pdf(file_path)
                
                # Analyze with Gemini
                score, comment = analyze_resume(job_role, resume_text)

                # Move file based on score
                if score == 0:
                    pass
                elif score == -1 or score < 6:
                    shutil.move(file_path, os.path.join(rejected_folder, filename))
                else:
                    shutil.move(file_path, os.path.join(shortlisted_folder, filename))

                # Store result
                results.append({"Filename": filename, "Score": score, "Comment": comment})
            except Exception as e:
                print(f"Error processing file '{filename}': {str(e)}")

    # Save results to CSV
    df = pd.DataFrame(results)
    output_filename = job_role.lower().replace(" ", "_") + "_results.csv"
    df.to_csv(output_filename, index=False)

    end_time = time.time()

    # Calculate elapsed time
    seconds_elapsed = end_time - start_time

    if (seconds_elapsed < 60):
        print(f"⏱️ Elapsed Time: {seconds_elapsed:.2f} seconds")
    else:
        minutes_elapsed = (end_time - start_time) / 60
        seconds_elapsed = (end_time - start_time) % 60
        print(f"⏱️ Elapsed Time: {minutes_elapsed:.0f} minutes {seconds_elapsed:.2f} seconds")
        
    print(f"{job_role} Resume Screening Completed! Check the 'Shortlisted' folder & CSV report.")
