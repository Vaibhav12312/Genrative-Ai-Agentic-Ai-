from app.database import connect
from app.schemas import RecordCreate


def create_record(record: RecordCreate) -> dict:
    with connect() as db:
        if record.legacy_id:
            db.execute(
                "INSERT OR IGNORE INTO records (title, content, category, legacy_id) "
                "VALUES (?, ?, ?, ?)",
                (record.title, record.content, record.category, record.legacy_id),
            )
            row = db.execute(
                "SELECT * FROM records WHERE legacy_id = ?", (record.legacy_id,)
            ).fetchone()
        else:
            cursor = db.execute(
                "INSERT INTO records (title, content, category) VALUES (?, ?, ?)",
                (record.title, record.content, record.category),
            )
            row = db.execute(
                "SELECT * FROM records WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        db.commit()
    return dict(row)


def list_records(limit: int = 100, offset: int = 0) -> list[dict]:
    with connect() as db:
        rows = db.execute(
            "SELECT * FROM records ORDER BY id ASC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    return [dict(row) for row in rows]


def get_record(record_id: str) -> dict | None:
    with connect() as db:
        if record_id.isdigit():
            row = db.execute(
                "SELECT * FROM records WHERE id = ? OR legacy_id = ?",
                (int(record_id), record_id),
            ).fetchone()
        else:
            row = db.execute(
                "SELECT * FROM records WHERE legacy_id = ?", (record_id,)
            ).fetchone()
    return dict(row) if row else None



def search_records(query: str, limit: int = 10) -> list[dict]:
    """Return records ranked by title, category, and content relevance."""
    stop_words = {
        "a", "an", "and", "are", "can", "do", "for", "how", "i", "in",
        "is", "it", "my", "of", "the", "to", "what", "when", "where",
        "which", "with", "epf", "epfo", "pf", "account", "accounts",
        "personal", "balance", "balances", "member", "members",
    }

    terms = [
        word.strip(".,!?;:()[]{}").lower()
        for word in query.split()
    ]
    terms = [
        word for word in terms
        if len(word) > 2 and word not in stop_words
    ]

    if not terms:
        return []

    with connect() as db:
        rows = db.execute("SELECT * FROM records").fetchall()

    title_matches = []
    content_matches = []

    for row in rows:
        record = dict(row)
        title = record["title"].lower()
        category = record["category"].lower()
        content = record["content"].lower()

        title_category_score = (
            sum(4 for term in terms if term in title)
            + sum(3 for term in terms if term in category)
        )
        content_score = sum(1 for term in terms if term in content)

        if title_category_score > 0:
            title_matches.append(
                (title_category_score + content_score, record)
            )
        elif content_score > 0:
            content_matches.append((content_score, record))

    matches = title_matches if title_matches else content_matches
    matches.sort(key=lambda item: (-item[0], item[1]["id"]))

    return [record for _, record in matches[:limit]]
