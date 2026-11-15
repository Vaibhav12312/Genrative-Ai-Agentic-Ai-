"""Document loading and provenance-preserving text chunking."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable

from pypdf import PdfReader

PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_FAQ_FILE = PROJECT_DIR.parent / "Day_4" / "data" / "records.json"
DOCUMENT_DIR = PROJECT_DIR / "data" / "documents"
SUPPORTED_SUFFIXES = {".pdf", ".txt", ".md", ".json"}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def _faq_record_to_text(record: dict[str, Any]) -> tuple[str, str, str]:
    question = _clean(record.get("question") or record.get("title"))
    answer = _clean(record.get("answer") or record.get("content") or record.get("text"))
    title = question or _clean(record.get("title")) or f"EPFO FAQ {record.get('faq_number', '')}".strip()
    parts = []
    if question:
        parts.append(f"Question: {question}")
    if answer:
        parts.append(f"Answer: {answer}")
    forms = record.get("related_form")
    if forms:
        parts.append(f"Related forms: {_clean(forms)}")
    return "\n".join(parts), title, _clean(record.get("source_url") or record.get("source"))


def _load_json(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(payload, dict):
        for key in ("records", "faqs", "documents", "items"):
            if isinstance(payload.get(key), list):
                payload = payload[key]
                break
        else:
            payload = [payload]
    if not isinstance(payload, list):
        raise ValueError(f"Unsupported JSON structure in {path}")
    docs = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            continue
        text, title, source = _faq_record_to_text(item)
        if not text:
            text = _clean(item)
        if not title:
            title = path.stem
        docs.append({
            "text": text,
            "title": title,
            "source": source or str(path.resolve()),
            "page": item.get("page"),
            "document_id": str(item.get("faq_number") or item.get("id") or f"{path.stem}-{index}"),
        })
    return docs


def load_documents(input_paths: Iterable[str | Path] | None = None) -> list[dict[str, Any]]:
    """Load supported sources while retaining title/source/page provenance."""
    paths: list[Path] = []
    if input_paths is None:
        env_value = os.getenv("EPFOSATHI_INPUTS", "")
        if env_value:
            paths.extend(Path(p.strip()).expanduser() for p in env_value.split(os.pathsep) if p.strip())
        else:
            if DEFAULT_FAQ_FILE.exists():
                paths.append(DEFAULT_FAQ_FILE)
            if DOCUMENT_DIR.exists():
                paths.append(DOCUMENT_DIR)
    else:
        paths.extend(Path(p).expanduser() for p in input_paths)

    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(p for p in sorted(path.rglob("*")) if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES)
        elif path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            files.append(path)
        elif path.exists():
            raise ValueError(f"Unsupported source file type: {path}")
    if not files:
        raise FileNotFoundError(
            "No EPFOSathi input documents found. Put files in data/documents/ "
            "or set EPFOSATHI_INPUTS. Expected PDF, TXT, MD or JSON."
        )

    documents: list[dict[str, Any]] = []
    for path in files:
        suffix = path.suffix.lower()
        if suffix == ".json":
            documents.extend(_load_json(path))
        elif suffix == ".pdf":
            reader = PdfReader(str(path))
            pdf_title = (reader.metadata.title if reader.metadata else None) or path.stem
            for page_number, page in enumerate(reader.pages, start=1):
                page_text = (page.extract_text() or "").strip()
                if page_text:
                    documents.append({
                        "text": page_text,
                        "title": pdf_title,
                        "source": str(path.resolve()),
                        "page": page_number,
                        "document_id": f"{path.name}-page-{page_number}",
                    })
        else:
            content = path.read_text(encoding="utf-8-sig", errors="replace").strip()
            if content:
                documents.append({
                    "text": content,
                    "title": path.stem,
                    "source": str(path.resolve()),
                    "page": None,
                    "document_id": path.name,
                })
    return documents


def chunk_documents(
    documents: Iterable[dict[str, Any]],
    chunk_size: int = 900,
    overlap: int = 150,
) -> list[dict[str, Any]]:
    """Split text into chunks and copy source/title/page metadata to every chunk."""
    if chunk_size < 100:
        raise ValueError("chunk_size must be at least 100 characters")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    chunks: list[dict[str, Any]] = []
    step = chunk_size - overlap
    for doc_index, doc in enumerate(documents):
        text = _clean(doc.get("text"))
        if not text:
            continue
        start = 0
        chunk_index = 0
        while start < len(text):
            piece = text[start:start + chunk_size].strip()
            if piece:
                metadata = {
                    "title": _clean(doc.get("title")) or "Untitled document",
                    "source": _clean(doc.get("source")) or "unknown",
                    "page": doc.get("page"),
                    "document_id": _clean(doc.get("document_id")) or f"document-{doc_index + 1}",
                    "chunk_index": chunk_index,
                }
                digest = hashlib.sha256(
                    f"{metadata['source']}|{metadata['page']}|{chunk_index}|{piece}".encode("utf-8")
                ).hexdigest()[:24]
                chunks.append({"id": digest, "text": piece, **metadata})
                chunk_index += 1
            if start + chunk_size >= len(text):
                break
            start += step
    return chunks


def build_chunks(input_paths: Iterable[str | Path] | None = None) -> list[dict[str, Any]]:
    size = int(os.getenv("EPFOSATHI_CHUNK_SIZE", "900"))
    overlap = int(os.getenv("EPFOSATHI_CHUNK_OVERLAP", "150"))
    return chunk_documents(load_documents(input_paths), chunk_size=size, overlap=overlap)
