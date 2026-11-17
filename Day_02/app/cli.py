"""Command-line interface for the EPFO FAQ project."""
import argparse
from pprint import pprint

from app.records import load_records, search, count_by, get_by_id

def main():
    records = load_records()
    parser = argparse.ArgumentParser(description="EPFO FAQ Management")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="Print all FAQ records")

    search_parser = commands.add_parser("search", help="Search questions and answers")
    search_parser.add_argument("keyword")

    count_parser = commands.add_parser("count", help="Count records by field")
    count_parser.add_argument("--by", default="category",
                              help="Field to count (default: category)")

    get_parser = commands.add_parser("get", help="Get one FAQ by number")
    get_parser.add_argument("faq_number", type=int)

    args = parser.parse_args()

    if args.command == "list":
        for record in records:
            print("-" * 72)
            pprint(record, sort_dicts=False)
        print(f"\nTotal records: {len(records)}")

    elif args.command == "search":
        results = search(records, args.keyword)
        for record in results:
            print(f'{record["faq_number"]}: {record["question"]}')
        print(f"Matches: {len(results)}")

    elif args.command == "count":
        for value, total in count_by(records, args.by).items():
            print(f"{value}: {total}")

    elif args.command == "get":
        record = get_by_id(records, args.faq_number)
        if record is None:
            print("FAQ not found.")
        else:
            pprint(record, sort_dicts=False)

if __name__ == "__main__":
    main()
