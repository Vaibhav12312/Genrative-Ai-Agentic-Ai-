
# EPFOSathi – Day 4

EPFOSathi is an EPFO FAQ service built using FastAPI, Pandas and Scikit-learn.

## Features

- FastAPI REST API
- EPFO FAQ record listing
- Individual FAQ retrieval
- HTTP 404 for missing records
- TF-IDF based smart search
- Cosine similarity ranking
- Question submission endpoint
- Pandas-based dataset analysis

## Project Structure

```text
Day_4/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── smart_search.py
├── analysis/
│   └── explore.py
├── data/
│   └── records.json
├── README.md
└── requirements.txt
```

## How to Run

### 1. Install dependencies

```bash
pip install fastapi uvicorn pandas scikit-learn
```

### 2. Run data analysis

```bash
python analysis/explore.py
```

### 3. Start the API server

```bash
uvicorn app.main:app --reload
```

### 4. Open API documentation

Visit:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Check API health |
| GET | /records?limit=10 | List FAQ records |
| GET | /records/{id} | Get FAQ by ID |
| GET | /search?q=pf | Search FAQs |
| POST | /questions | Submit an EPFO question |

## Smart Search

EPFOSathi uses:

- TF-IDF (Term Frequency-Inverse Document Frequency)
- Cosine Similarity
- Relevance-based FAQ ranking

## Dataset

The project uses 20 EPFO FAQ records sourced from:

https://www.epfo.gov.in/faq-epfo/

## Technologies

- Python
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
