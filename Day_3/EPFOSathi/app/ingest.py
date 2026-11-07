
import json
import logging
import runpy
from pathlib import Path

from app.models import Record

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "sample_records.py"
OUTPUT_FILE = PROJECT_ROOT / "data" / "records.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def ingest():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {RAW_FILE}")

    source_data = runpy.run_path(str(RAW_FILE))
    raw_records = source_data.get("sample_records")

    if not isinstance(raw_records, list):
        raise ValueError("sample_records must be a list")

    clean_records = []
    bad_records = 0

    for row_number, row in enumerate(raw_records, start=1):
        try:
            if not isinstance(row, dict):
                raise ValueError("Record must be a dictionary")

            related_form = row.get("related_form")

            if isinstance(related_form, list):
                related_form = ", ".join(
                    str(item).strip()
                    for item in related_form
                    if str(item).strip()
                ) or None
            elif related_form is not None:
                related_form = str(related_form).strip() or None

            record = Record(
                faq_number=str(row["faq_number"]),
                category=str(row["category"]),
                question=str(row["question"]),
                answer=str(row["answer"]),
                related_form=related_form,
                source_url=str(
                    row.get("source_url")
                    or "Not provided in original Day 2 dataset"
                ),
            )

            clean_records.append(record.to_dict())

        except (KeyError, TypeError, ValueError, AttributeError) as error:
            bad_records += 1
            logging.warning(
                "Skipping bad row %s: %s",
                row_number,
                error
            )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(clean_records, file, indent=4, ensure_ascii=False)

    logging.info("Total input records: %s", len(raw_records))
    logging.info("Successfully processed: %s", len(clean_records))
    logging.info("Bad records skipped: %s", bad_records)
    logging.info("Output saved to: %s", OUTPUT_FILE)

    return clean_records


if __name__ == "__main__":
    ingest()
