"""Reusable data access and search operations for EPFO FAQ records."""
from data.sample_records import sample_records

def load_records():
    """Return a copy of all FAQ records."""
    return [record.copy() for record in sample_records]

def search(records, keyword):
    """Case-insensitive search in FAQ questions and answers."""
    keyword = keyword.casefold().strip()
    if not keyword:
        return []
    return [
        record for record in records
        if keyword in record["question"].casefold()
        or keyword in record["answer"].casefold()
    ]

def count_by(records, field):
    """Count values for a field; list-valued fields count each item."""
    counts = {}
    for record in records:
        value = record.get(field)
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        for item in values:
            counts[item] = counts.get(item, 0) + 1
    return counts

def get_by_id(records, faq_number):
    """Return one record by FAQ number, or None when absent."""
    for record in records:
        if record.get("faq_number") == faq_number:
            return record
    return None
