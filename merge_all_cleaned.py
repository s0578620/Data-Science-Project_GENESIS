# merge_all_cleaned.py
from src.merge_cleaned import merge_cleaned_files
import os

codes_pairs = [
    ("48112-0001", "48112-0003"),
    ("48112-0002", "48112-0004")
]
years = ["2018", "2019", "2020", "2021", "2022"]

def main():
    for code1, code2 in codes_pairs:
        for year in years:
            file1 = f"data/cleaned/{code1}_{year}_cleaned.csv"
            file2 = f"data/cleaned/{code2}_{year}_cleaned.csv"

            if not (os.path.exists(file1) and os.path.exists(file2)):
                print(f"⚠️  Dateien nicht gefunden: {file1} oder {file2}")
                continue

            print(f"🔄 Merge {file1} und {file2} ...")
            merged_df = merge_cleaned_files(file1, file2, out_folder="data/merged")

            print("✅ Vorschau der ersten Zeilen:")
            print(merged_df.head(3))
            print("-" * 40)

if __name__ == "__main__":
    main()
