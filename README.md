# 🛡️ Autonomous Insurance Claims Processing Agent

A lightweight Python application that processes First Notice of Loss (FNOL) documents, extracts structured claim information, validates mandatory fields, detects inconsistencies, and routes claims according to the business rules defined in the assessment brief.


## 🎥 Demo Video

[▶️ Watch the short demo video](https://drive.google.com/file/d/122LNqYu-DbiOQd95rfxkOiI1fK7v-u7n/view?usp=drive_link)


## 🎯 Problem Statement

The application automates an initial insurance-claim processing workflow by:

- Extracting key information from FNOL documents
- Identifying missing mandatory fields
- Detecting inconsistent claim information
- Classifying claims based on predefined rules
- Routing claims to the appropriate workflow
- Providing an explanation for the routing decision
- Returning the result in JSON format

---

## ✨ Features

- Upload PDF or TXT FNOL documents
- Extract policy information
- Extract incident information
- Extract claimant and third-party information
- Extract asset and damage information
- Detect missing mandatory fields
- Detect inconsistent estimated and initial damage values
- Detect investigation-related keywords
- Route injury claims to the specialist queue
- Route low-value claims to fast-track
- Generate explainable routing decisions
- Display structured JSON output
- Download the final claim result as JSON
- Streamlit-based web interface

---

## 🏗️ System Architecture

```text
                FNOL Document
                      │
                      ▼
              Document Extraction
                      │
                      ▼
               Field Extraction
                      │
                      ▼
                 Validation
             ┌────────┴────────┐
             │                 │
       Missing Fields    Inconsistencies
             │                 │
             └────────┬────────┘
                      ▼
                Routing Engine
                      │
                      ▼
             Explainable Decision
                      │
                      ▼
                  JSON Output
```
                  ---

## 🔄 Processing Workflow

1. Upload an FNOL document in PDF or TXT format.
2. Extract the text from the uploaded document.
3. Extract the required claim fields.
4. Validate the mandatory fields.
5. Check for missing or inconsistent information.
6. Apply the predefined routing rules.
7. Generate a short explanation for the routing decision.
8. Display the extracted information and final JSON result.


---

## 📋 Fields Extracted

### Policy Information

- Policy Number
- Policyholder Name
- Effective Dates

### Incident Information

- Incident Date
- Incident Time
- Location
- Description

### Involved Parties

- Claimant
- Third Parties
- Contact Details

### Asset Details

- Asset Type
- Asset ID
- Estimated Damage

### Other Mandatory Information

- Claim Type
- Attachments
- Initial Estimate

---

## 🔀 Routing Rules

The application evaluates each claim using the business rules provided in the assessment brief.

| Condition | Recommended Route |
|---|---|
| Estimated damage < ₹25,000 and mandatory fields are present | Fast-track |
| Any mandatory field is missing | Manual review |
| Description contains `fraud`, `inconsistent`, or `staged` | Investigation Flag |
| Claim type is `injury` | Specialist Queue |
| Claim information is inconsistent | Manual review |

### Rule Handling

The routing engine applies the predefined business rules deterministically so that the same input produces the same routing decision.

Claims with missing or inconsistent information are routed for manual verification rather than being automatically fast-tracked.


---

## 🤖 AI / Intelligent Processing

The current implementation uses Python-based document extraction, validation, and deterministic business rules to provide reliable and explainable claim routing.

AI-assisted development tools were used during implementation to accelerate development, debugging, and code refinement.

The extraction layer is modular and can be extended with an LLM-based extraction component in the future to handle more unstructured FNOL documents.

The current application does not require an external AI API key to run.


---

## 🛠️ Tech Stack

- Python
- Streamlit
- PyMuPDF
- Regular Expressions
- JSON


---

## 📁 Project Structure

```text
autonomous-insurance-claims-agent/
│
├── app.py
├── extractor.py
├── validator.py
├── router.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── sample_documents/
    ├── fnol_fast_track.txt
    ├── fnol_missing_field.txt
    ├── fnol_investigation.txt
    ├── fnol_injury.txt
    └── fnol_inconsistent.txt


---
```
## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Navigate to the project

```bash
cd autonomous_insurance_claims_agent
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

---

## 🧪 Test Scenarios

The application was tested using synthetic FNOL documents covering the major routing conditions defined in the assessment brief.

| Test Case | Scenario | Expected Route |
|---|---|---|
| 1 | All mandatory fields present and estimated damage < ₹25,000 | Fast-track |
| 2 | Mandatory field missing | Manual review |
| 3 | Description contains investigation keywords | Investigation Flag |
| 4 | Claim type is Injury | Specialist Queue |
| 5 | Claim information is inconsistent | Manual review |

### Sample Documents

The following synthetic FNOL documents are included in the repository:

- `fnol_fast_track.txt`
- `fnol_missing_field.txt`
- `fnol_investigation.txt`
- `fnol_injury.txt`
- `fnol_inconsistent.txt`

These documents were created as dummy test data based on the fields and business rules provided in the assessment brief.


---

## 📤 Output Format

The application returns the processed claim in a structured JSON format:

```json
{
  "extractedFields": {},
  "missingFields": [],
  "recommendedRoute": "",
  "reasoning": ""
}
```

### Output Components

- **extractedFields** – Contains the information extracted from the FNOL document.
- **missingFields** – Lists mandatory fields that were not provided.
- **recommendedRoute** – Contains the workflow selected by the routing engine.
- **reasoning** – Provides a short explanation for the routing decision.

The processed JSON result can also be downloaded directly from the Streamlit application.


---

## 📄 Assessment Sample Documents

The original assessment brief mentioned that sample FNOL documents would be provided. Since the sample documents were not available during development, synthetic FNOL documents were created for testing.

The synthetic documents were designed based on the fields and business rules specified in the assessment brief.

These documents contain dummy data and do not represent real insurance customers or claims.

---

## 🚀 Future Enhancements

- Integrate an LLM-based extraction layer for more unstructured FNOL documents
- Add OCR support for scanned documents
- Add a database for storing processed claims
- Add authentication and role-based access
- Maintain claim processing history and audit logs
- Add REST API support
- Improve automated claim classification
- Deploy the application to a cloud platform