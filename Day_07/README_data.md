# Source documents

This folder contains the bundled `epfosathi_faqs.json` corpus (20 FAQ records)
and is the default input directory for the S1/S2 pipeline.

You may add further actual EPFOSathi source documents here (`.pdf`, `.txt`,
`.md` or `.json`). The loader also reads `../Day_4/data/records.json` when it
exists.

For PDF documents, page numbers are extracted from the PDF and retained as
1-based page metadata. The bundled FAQ records have no source page numbers;
their `page` value is intentionally `null`. The original source URL, question
(title), answer and related form metadata are retained. Do not invent page
numbers or retrieval results.
