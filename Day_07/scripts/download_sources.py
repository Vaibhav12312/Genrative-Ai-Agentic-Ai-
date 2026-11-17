"""Download the official EPFO PDFs listed in data/SOURCES.md into data/documents/.

Run from the Day_5 folder (needs internet):
    python scripts/download_sources.py
Uses only the standard library. Files that already exist are skipped.
"""
from pathlib import Path
from urllib.request import Request, urlopen

TARGET = Path(__file__).resolve().parents[1] / "data" / "documents"

SOURCES = {
    "UAN_Member_FAQ.pdf":
        "https://epfindia.gov.in/site_docs/PDFs/UAN_PDFs/UAN_ForMembers/FAQ-Member-Ver1.1.pdf",
    "Online_Claim_Filing_Manual_Form19_10C_31.pdf":
        "https://www.epfindia.gov.in/site_docs/PDFs/Circulars/Y2017-2018/Manual_FilingOnlineClaim_293.pdf",
    "Online_Claim_Eligibility_Check.pdf":
        "https://www.epfindia.gov.in/site_docs/PDFs/MiscPDFs/ocs_eligibiltiyCheck_050517_1019.pdf",
    "Important_Guidelines_For_Members_OTCP.pdf":
        "https://www.epfindia.gov.in/site_docs/PDFs/OTCP_PDFs/ImportantGuidelinesformember.pdf",
}


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        dest = TARGET / name
        if dest.exists():
            print(f"skip (exists): {name}")
            continue
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=60) as resp:
                data = resp.read()
            if not data.startswith(b"%PDF"):
                print(f"FAILED (not a PDF): {name}")
                continue
            dest.write_bytes(data)
            print(f"downloaded: {name} ({len(data) // 1024} KB)")
        except Exception as exc:
            print(f"FAILED: {name} -> {exc}")


if __name__ == "__main__":
    main()
