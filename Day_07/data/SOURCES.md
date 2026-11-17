# Official EPFO source documents to add to this corpus

The source-code package did not include the `Day_4/data/records.json` corpus
referenced by the loader. No FAQ answers or retrieval hits have been fabricated.

To make the 10-question evaluation meaningful, place downloaded official EPFO
PDFs in this directory. The following EPFO-hosted references were identified
for this checkpoint; check each document's date and current applicability
before using its content to advise a member:

1. **UAN Member FAQ**  
   https://epfindia.gov.in/site_docs/PDFs/UAN_PDFs/UAN_ForMembers/FAQ-Member-Ver1.1.pdf
2. **Instructions for processing online claims (Form 19, Form 10C and Form 31)**  
   https://www.epfindia.gov.in/site_docs/PDFs/Circulars/Y2017-2018/Manual_FilingOnlineClaim_293.pdf
3. **Online claim eligibility and submission flow**  
   https://www.epfindia.gov.in/site_docs/PDFs/MiscPDFs/ocs_eligibiltiyCheck_050517_1019.pdf
4. **Important guidelines for EPF members / online transfer claim**  
   https://www.epfindia.gov.in/site_docs/PDFs/OTCP_PDFs/ImportantGuidelinesformember.pdf

Save the PDFs here using descriptive filenames, then rebuild the Chroma index
and run the ten-question evaluation. PDF page numbers are extracted as 1-based
page metadata. Keep the original official source URL in this manifest or in a
JSON record if you later ingest the same material through JSON.

The references above are official EPFO-hosted documents, but some are older
circulars/guides. They are useful retrieval corpus material, not proof that
all instructions remain current in 2026.


## Included FAQ corpus

`data/documents/epfosathi_faqs.json` contains 20 FAQ records extracted from the
EPFO FAQ material supplied with the project. Each record preserves its FAQ
question as the title, answer text, category, related forms, and the supplied
source URL (`https://www.epfo.gov.in/faq-epfo/`). The supplied material did not
include PDF page numbers, so `page` is explicitly `null`; no page numbers have
been invented. Check the current applicability of these FAQ answers before
using them as member guidance.
