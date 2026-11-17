# EPFOSathi — S1 & S2: Document Chunking, Embeddings and Semantic Search

A modular Retrieval-Augmented Generation (RAG) retrieval layer for the EPFOSathi project. This implementation processes EPFO FAQ documents, generates semantic embeddings, stores document chunks in a persistent Chroma vector database, and provides a FastAPI endpoint for semantic search.

The implementation focuses on document traceability, persistent vector storage, semantic retrieval, and reproducible evaluation.

---

## 1. Project Overview

This project implements two major components:

### S1 — Document Chunking, Embeddings and Semantic Search Evaluation

- `app/chunking.py`: Loads supported EPFOSathi documents and splits their content into smaller, overlapping chunks.
- `app/embed.py`: Generates semantic embeddings using Sentence Transformers.
- Document metadata: Preserves source, title, page, document ID, and chunk index.
- `eval/questions.json`: Contains 10 semantic retrieval evaluation questions.
- `eval/run_evaluation.py`: Executes the evaluation questions against the indexed vector collection.
- `eval/search_results.md`: Records actual retrieved search results, including titles, sources, page metadata, and similarity information.

### S2 — Persistent Vector Database and Semantic Search API

- `app/vectorstore.py`: Generates and stores document embeddings and metadata in a persistent Chroma collection.
- `app/main.py`: Provides the FastAPI application and semantic search endpoint.
- Chroma collection: `epfosathi_documents`.
- API endpoint: `GET /search/semantic?q=...`.
- Health endpoint: `GET /health`.

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Sentence Transformers | Semantic embedding generation |
| `all-MiniLM-L6-v2` | Embedding model |
| ChromaDB | Persistent vector database |
| FastAPI | REST API framework |
| Uvicorn | API development server |
| Pytest | Automated testing |
| Hugging Face | Embedding model distribution |

### Embedding Model

The project uses:

`sentence-transformers/all-MiniLM-L6-v2`

This model converts text into numerical vector representations so that semantically similar questions and documents can be retrieved.

---

## 3. Project Folder Structure

The Day_7 folder contains the S1 and S2 implementation.

```text
Day_7/
│
├── app/
│   ├── __init__.py
│   ├── chunking.py
│   ├── embed.py
│   ├── vectorstore.py
│   └── main.py
│
├── data/
│   ├── documents/
│   │   └── epfosathi_faqs.json
│   └── SOURCES.md
│
├── eval/
│   ├── __init__.py
│   ├── questions.json
│   ├── run_evaluation.py
│   └── search_results.md
│
├── scripts/
│   └── download_sources.py
│
├── tests/
│   ├── test_chunking.py
│   ├── test_embed.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

The structure above describes the main project components. Keep any additional existing project configuration and test files in the repository.

---

## 4. Document Sources and Ingestion

The project processes EPFOSathi document sources for semantic retrieval.

Supported document formats include:

- JSON
- PDF
- TXT
- Markdown (`.md`)

The current indexed FAQ dataset is:

`data/documents/epfosathi_faqs.json`

It contains 20 FAQ records extracted from EPFO FAQ material.

The records retain:

- FAQ question/title
- Answer
- Source URL
- Category
- Related forms, where available

### Document Provenance

Preserving the original document information is important for traceability.

Each chunk retains the following metadata:

| Metadata | Description |
|---|---|
| `source` | Original document URL or file path |
| `title` | Original FAQ question or document title |
| `page` | Original page number, when available |
| `document_id` | Identifier of the source document |
| `chunk_index` | Position of the chunk within its document |

**Important page metadata rule:**

The current FAQ records originate from a webpage and do not contain PDF page numbers. Therefore, their page metadata is stored as `null`.

For PDF documents, the actual 1-based PDF page number should be retained.

Page numbers must never be invented.

---

## 5. Windows PowerShell Setup

Open PowerShell inside the Day_7 folder.

### Step 1: Create a virtual environment

```powershell
py -3.12 -m venv .venv
```

### Step 2: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Step 3: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Step 4: Install project dependencies

```powershell
pip install -r requirements.txt
```

The first embedding execution may download the Sentence Transformer model from Hugging Face. Internet access is required for the initial download if the model is not already cached.

---

## 6. Document Chunking and Embedding

### Document Chunking

`app/chunking.py` is responsible for:

1. Loading configured source documents.
2. Extracting document text.
3. Splitting long documents into smaller chunks.
4. Applying chunk overlap to preserve contextual continuity.
5. Attaching source metadata to each chunk.

The documented default configuration is:

- Chunk size: 900 characters
- Chunk overlap: 150 characters

These settings can be configured using environment variables:

```powershell
$env:EPFOSATHI_CHUNK_SIZE = "900"
$env:EPFOSATHI_CHUNK_OVERLAP = "150"
```

### Embedding Generation

`app/embed.py` generates semantic embeddings using the Sentence Transformer model.

The generated vectors represent the semantic meaning of the document chunks and are used for similarity-based retrieval.

---

## 7. Persistent Chroma Vector Database

`app/vectorstore.py` manages the Chroma vector database.

The implementation stores:

- Chunk text
- Embeddings
- Document metadata
- Document identifiers

### Collection Name

`epfosathi_documents`

### Persistence

The vector database is stored locally in:

```text
chroma_db/
```

The persistent Chroma database allows indexed documents to remain available after restarting the API.

### Rebuild and Index the Collection

Run the following command from the project folder to rebuild the database:

```powershell
Remove-Item .\chroma_db -Recurse -Force
```

Only run the removal command when you intentionally want to recreate the database.

Then execute:

```powershell
python -c "from app.chunking import build_chunks; from app.vectorstore import index_chunks; chunks=build_chunks(); print('Chunks to index:',len(chunks)); print('Indexed count:',index_chunks(chunks))"
```

This operation:

1. Loads the configured documents.
2. Creates document chunks.
3. Generates embeddings.
4. Indexes chunks into Chroma.
5. Stores the indexed collection persistently.

The current verified execution produced:

```text
Chunks to index: 20
Indexed count: 20
```

---

## 8. Run the Semantic Search API

Start the FastAPI server from the Day_7 folder:

```powershell
uvicorn app.main:app --reload
```

The API runs locally at:

`http://127.0.0.1:8000`

### Available Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Checks API and collection health |
| `/search/semantic?q=` | GET | Performs semantic document retrieval |
| `/docs` | GET | Opens interactive API documentation |

### Health Check

Open:

`http://127.0.0.1:8000/health`

Or run:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/health"
```

Verified response:

```text
status collection          indexed_chunks
------ ----------          --------------
ok     epfosathi_documents             20
```

### Semantic Search Example

Search for:

`How can I transfer my PF account?`

PowerShell command:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/search/semantic?q=How%20can%20I%20transfer%20my%20PF%20account" | ConvertTo-Json -Depth 8
```

The endpoint returns ranked search results containing:

- Retrieved text
- Original title
- Source URL
- Page number, when available
- Document ID
- Chunk index
- Chroma distance
- Similarity score

### Example Response Structure

```json
{
  "query": "How can I transfer my PF account?",
  "count": 5,
  "results": [
    {
      "text": "Retrieved source text...",
      "title": "Original FAQ question",
      "source": "https://www.epfo.gov.in/faq-epfo/",
      "page": null,
      "document_id": "10",
      "chunk_index": 0,
      "distance": 0.36,
      "similarity": 0.64
    }
  ]
}
```

The example above illustrates the response structure; actual retrieved values depend on the indexed collection.

### Understanding Similarity and Distance

Chroma uses the configured cosine distance metric.

The project reports:

`similarity = 1 - distance`

Similarity is useful for ranking retrieved results. It is not a calibrated probability or guaranteed measure of answer correctness.

---

## 9. Ten-Question Semantic Search Evaluation

The evaluation questions are stored in:

`eval/questions.json`

The project uses 10 questions to evaluate semantic retrieval across EPFO-related topics.

### Run the Evaluation

First ensure that the Chroma collection has been indexed and is accessible.

Then run:

```powershell
python -m eval.run_evaluation
```

The evaluation process:

1. Loads the 10 evaluation questions.
2. Generates semantic embeddings for the questions.
3. Searches the persistent Chroma collection.
4. Retrieves ranked matching chunks.
5. Records the actual retrieved hits.
6. Saves the results in `eval/search_results.md`.

### Evaluation Report

Output file:

`eval/search_results.md`

The report contains:

- Evaluation execution timestamp
- Retrieval method
- Evaluation questions
- Ranked search results
- Original titles
- Source URLs
- Page metadata
- Chunk indices
- Similarity and distance information

### Verified Evaluation Execution

The current verified run produced:

```text
Evaluation complete:
eval/search_results.md

Executed 10 questions and recorded 50 hits.
```

This represents 10 evaluation questions with 5 retrieved results per question.

**Retrieval quality note:** Successful retrieval execution does not guarantee that every returned result is relevant. The current FAQ dataset contains 20 records and does not cover every topic in the evaluation questions. The results should therefore be reviewed manually, and additional relevant official EPFO material should be added to improve retrieval coverage.

---

## 10. Automated Tests

The project includes automated tests for its document processing, embedding, and API functionality.

Run the tests from the project folder:

```powershell
python -m pytest -q
```

### Verified Test Result

```text
.............
13 passed in 0.72s
```

All 13 tests passed in the recorded execution.

Tests provide automated verification of the implemented functionality. They should be considered alongside the real Chroma indexing and API checks.

---

## 11. Design Decisions

### Modular Architecture

Chunking, embedding generation, vector storage, and API functionality are separated into independent modules.

This makes the project easier to understand, maintain, and extend.

### Document Traceability

Each retrieved chunk retains its original source and title, along with page information when available.

This supports verification of retrieved information.

### Persistent Retrieval

ChromaDB uses local persistent storage so that the indexed collection remains available after API restarts.

### Semantic Retrieval

Sentence Transformer embeddings allow the system to retrieve documents based on semantic similarity rather than relying only on exact keyword matches.

### Reproducible Evaluation

The evaluation script executes a fixed set of 10 questions and records actual runtime search results.

### No Fabricated Metadata

Missing page numbers are represented as `null` rather than being artificially generated.

### Local-First Architecture

The retrieval system uses local Chroma storage and a locally running FastAPI service. An external hosted vector database is not required.

---

## 12. Git and Repository Guidelines

Before committing the Day_7 folder to GitHub, verify that:

- `.env` files containing actual credentials are excluded.
- Virtual environments are excluded.
- Python cache directories are excluded.
- Unnecessary temporary files are excluded.
- The evaluation report is included.
- The source FAQ dataset is included.
- The README accurately describes the implementation.

Recommended `.gitignore` entries:

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/

# Virtual environments
.venv/
venv/

# Environment variables and secrets
.env
.env.*
!.env.example

# Generated vector database
chroma_db/

# Temporary files
*.log
.DS_Store
Thumbs.db
```

The Chroma database can be recreated from the source documents using the indexing instructions in this README. Keep `eval/search_results.md` in the repository so the evaluation evidence is available.

---

## 13. Current Verified Execution Status

The following results were confirmed through actual terminal execution for this project:

| Verification | Result |
|---|---|
| FAQ records loaded | 20 |
| Document chunks created | 20 |
| Chunks indexed | 20 |
| Chroma collection | `epfosathi_documents` |
| Persistent database files | 5 |
| Evaluation questions executed | 10 |
| Search hits recorded | 50 |
| API health | OK |
| Semantic search endpoint | Working |
| Automated tests | 13 passed |

### Known Limitation

The current corpus contains 20 FAQ records. Some evaluation questions cover topics that are not sufficiently represented in this corpus, which can result in less relevant search results.

This is a corpus coverage and retrieval quality limitation, not evidence that the indexing or API execution failed.

Additional relevant official EPFO documents and FAQs should be incorporated to improve the retrieval results.

---

## 14. Completion Checklist

### S1 — Chunking, Embeddings and Evaluation

- [x] Create `app/chunking.py`.
- [x] Create `app/embed.py`.
- [x] Load EPFOSathi FAQ documents.
- [x] Generate document chunks.
- [x] Preserve source metadata.
- [x] Preserve title metadata.
- [x] Preserve page metadata when available.
- [x] Configure semantic embeddings.
- [x] Prepare 10 evaluation questions.
- [x] Execute semantic retrieval for all 10 questions.
- [x] Record 50 retrieved hits in `eval/search_results.md`.

### S2 — Persistent Chroma and API

- [x] Create `app/vectorstore.py`.
- [x] Generate and index document embeddings.
- [x] Store chunks in persistent Chroma.
- [x] Verify the `epfosathi_documents` collection.
- [x] Implement `GET /search/semantic?q=`.
- [x] Verify semantic search results.
- [x] Verify API health.
- [x] Confirm 20 indexed chunks.

### Testing

- [x] Run automated pytest tests.
- [x] Confirm all 13 tests pass.
- [x] Run the real semantic evaluation.
- [ ] Improve relevance for questions not adequately covered by the current corpus.

---

## 15. Final Summary

EPFOSathi S1 and S2 implement a document retrieval foundation using Python, Sentence Transformers, ChromaDB, and FastAPI.

The implementation provides:

1. Document ingestion and chunking.
2. Metadata preservation and document traceability.
3. Semantic embedding generation.
4. Persistent Chroma vector storage.
5. Semantic search through a FastAPI endpoint.
6. Ten-question retrieval evaluation.
7. Search result recording.
8. Automated test coverage.

The current implementation has been executed and technically verified with 20 indexed chunks, 10 evaluation questions, 50 recorded search hits, a working semantic search endpoint, and 13 passing tests.

**Project status:** S1 and S2 technical implementation verified. Retrieval relevance improvements remain an identified follow-up task.

---

**Project:** EPFOSathi  
**Module:** S1 — Document Chunking, Embeddings and Evaluation  
**Module:** S2 — Persistent Chroma Vector Store and Semantic Search API  
**Primary language:** Python  
**Vector database:** ChromaDB  
**API framework:** FastAPI