
import logging
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

DOCUMENTS = [
    {
        "filename": "epfo_annual_report_2024_25.pdf",
        "url": "https://pmvbry-cdn.epfindia.gov.in/wp-content/uploads/2025/08/Annual-Report-2024-25.pdf",
    },
    {
        "filename": "epfo_annual_report_2023_24.pdf",
        "url": "https://pmvbry-cdn.epfindia.gov.in/wp-content/uploads/2025/08/71.pdf",
    },
    {
        "filename": "epfo_annual_report_2014_15.pdf",
        "url": "https://pmvbry-cdn.epfindia.gov.in/wp-content/uploads/2025/08/61.pdf",
    },
]

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 EPFOSathi-Data-Research/1.0"
}


def download_document(document):
    filename = document["filename"]
    url = document["url"]

    output_path = RAW_DIR / filename
    temp_path = RAW_DIR / (filename + ".part")

    try:
        logging.info("Downloading: %s", filename)

        with requests.get(
            url,
            headers=HEADERS,
            timeout=(15, 90),
            stream=True
        ) as response:

            response.raise_for_status()

            with open(temp_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)

        with open(temp_path, "rb") as file:
            signature = file.read(5)

        if signature != b"%PDF-":
            raise ValueError("Downloaded file is not a genuine PDF")

        temp_path.replace(output_path)

        logging.info(
            "SUCCESS: %s (%s bytes)",
            filename,
            output_path.stat().st_size
        )
        return True

    except (requests.RequestException, OSError, ValueError) as error:
        logging.error("FAILED: %s - %s", filename, error)

        if temp_path.exists():
            temp_path.unlink()

        return False


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    successful = 0

    for document in DOCUMENTS:
        if download_document(document):
            successful += 1

    logging.info("Total documents: %s", len(DOCUMENTS))
    logging.info("Successfully downloaded: %s", successful)
    logging.info("Failed downloads: %s", len(DOCUMENTS) - successful)
    logging.info("Raw data folder: %s", RAW_DIR)


if __name__ == "__main__":
    main()
