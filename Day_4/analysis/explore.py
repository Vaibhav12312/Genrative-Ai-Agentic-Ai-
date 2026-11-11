
import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "records.json"


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    df = pd.DataFrame(records)

    print("\n========== EPFOSathi DATA ANALYSIS ==========\n")

    # FACT 1
    print("FACT 1: Total FAQ records")
    print(f"Total records: {len(df)}")

    # FACT 2
    print("\nFACT 2: Records by category")
    print(df["category"].value_counts().to_string())

    # FACT 3
    print("\nFACT 3: Longest FAQ answer")
    longest_index = df["answer"].str.len().idxmax()
    longest_faq = df.loc[longest_index]

    print(f"FAQ Number: {longest_faq['faq_number']}")
    print(f"Category: {longest_faq['category']}")
    print(f"Answer length: {len(longest_faq['answer'])} characters")

    print("\n=============================================\n")


if __name__ == "__main__":
    main()
