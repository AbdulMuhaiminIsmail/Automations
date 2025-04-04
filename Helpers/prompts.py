# SEO Prompt
seo_prompt = """
    You are an expert in resume screening and hiring. Your task is to analyze a candidate's resume against the given job description and provide a structured evaluation.

    Here is the job description you need to match the candidate's resume with:
    {job_description}
    
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

# UI/UX Prompt
uiux_prompt = """
    You are an expert in resume screening and hiring. Your task is to analyze a candidate's resume against the given UI/UX Designer job description and provide a structured evaluation.

    ### **Job Description:**
    {job_description}

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