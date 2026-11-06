"""Simple S1 entry point."""
from app.records import load_records, search, count_by

if __name__ == "__main__":
    records = load_records()
    for record in records:
        print(record)
    print("\nSearch results for 'withdrawal':")
    for record in search(records, "withdrawal"):
        print(record["faq_number"], record["question"])
    print("\nCounts by category:")
    print(count_by(records, "category"))
