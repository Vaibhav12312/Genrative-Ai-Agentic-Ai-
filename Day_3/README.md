# EPFOSathi – EPFO FAQ Data Ingestion Pipeline

## Project Overview

EPFOSathi is a Python-based project designed to organize Employees' Provident Fund (EPF) information into structured data for a future FAQ question-answering application.

**Day 3 focuses on data ingestion, record validation, JSON generation, and downloading supporting EPFO documents.**

## Objectives

- Create a reusable FAQ data model using Python dataclasses.
- Maintain structured EPFO employee FAQ records.
- Clean and validate FAQ data.
- Handle invalid records using exception handling.
- Generate structured JSON output.
- Download multiple PDF documents using the Requests library.
- Implement timeouts, HTTP validation, and error handling.

## Project Structure

```text
Day_3/
├── app/
│   ├── models.py
│   ├── fetch.py
│   └── ingest.py
├── data/
│   ├── raw/
│   │   ├── sample_records.py
│   │   ├── epfo_annual_report_2014_15.pdf
│   │   ├── epfo_annual_report_2023_24.pdf
│   │   └── epfo_annual_report_2024_25.pdf
│   └── records.json
├── .gitignore
├── README.md
└── requirements.txt
```

## Main Components

### 1. Data Model – `app/models.py`

Defines a `Record` dataclass representing an EPFO FAQ.

Each record contains six fields:

| Field | Description |
|---|---|
| `faq_number` | FAQ identification number |
| `category` | FAQ category |
| `question` | Employee question |
| `answer` | Answer to the question |
| `related_form` | Related EPFO form, if applicable |
| `source_url` | Reference URL for the FAQ |

The model also performs input normalization and validation.

### 2. Document Downloader – `app/fetch.py`

Downloads three EPFO annual-report PDF documents into `data/raw/`.

Features include:

- HTTP requests using Python Requests.
- Connection and read timeouts.
- HTTP status-code validation.
- Streaming file downloads.
- PDF signature verification.
- Temporary-file handling.
- Exception handling and logging.

### 3. FAQ Ingestion – `app/ingest.py`

Processes the prepared FAQ dataset from `data/raw/sample_records.py`.

The ingestion pipeline:

1. Reads the source FAQ records.
2. Validates individual records.
3. Cleans and normalizes text fields.
4. Handles missing or invalid values.
5. Converts valid records into structured dictionaries.
6. Saves the cleaned dataset as JSON.

Invalid records are logged and skipped without interrupting the complete ingestion process.

## Dataset Information

| Attribute | Value |
|---|---|
| Dataset | EPFO Employee FAQs |
| Total records | 20 |
| Category | Employee |
| Output format | JSON |
| Required fields | 6 |
| Output location | `data/records.json` |

The dataset covers topics including:

- EPF membership eligibility
- Employee and employer contributions
- Interest on EPF accounts
- PF account transfers
- Provident Fund withdrawals
- Retirement-related queries

## Installation

Requirements:

- Python 3.10 or later
- pip

Install dependencies from the Day_3 directory:

```powershell
python -m pip install -r requirements.txt
```

## Running the Project

Open PowerShell and navigate to the Day_3 directory:

```powershell
cd Day_3
```

Run the document downloader:

```powershell
python -m app.fetch
```

Run the FAQ ingestion pipeline:

```powershell
python -m app.ingest
```

The cleaned output will be generated at:

```text
data/records.json
```

## Validate the JSON Output

Run this command from the repository root:

```powershell
python -c "import json; p=json.load(open('Day_3/data/records.json',encoding='utf-8')); required={'faq_number','category','question','answer','related_form','source_url'}; print('Total records:',len(p)); print('All six fields present:',all(required.issubset(r) for r in p))"
```

Expected output:

```text
Total records: 20
All six fields present: True
```

## Technologies Used

- Python
- Dataclasses
- Requests
- JSON
- pathlib
- Logging
- Exception Handling

## Output

The primary output of this module is:

`data/records.json`

This structured dataset can be used by subsequent EPF FAQ application components, including search, retrieval, and question-answering workflows.

## Future Scope

- Expand the EPFO FAQ dataset.
- Add automated document text extraction.
- Implement data deduplication.
- Integrate the dataset with a vector database.
- Develop a retrieval-augmented generation (RAG) pipeline.

## GitHub Repository

[Genrative-Ai-Agentic-Ai](https://github.com/Vaibhav12312/Genrative-Ai-Agentic-Ai-)

**Module:** Day 3 – EPFOSathi Data Ingestion Pipeline
