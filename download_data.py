# download_data.py

import argparse
from src.download_table_auto import download_and_extract_table_auto
from src.loader import load_genesis_csv

def download_and_clean_all():
    codes = ["48112-0001", "48112-0002", "48112-0003", "48112-0004"]
    years = ["2018", "2019", "2020", "2021", "2022"]

    for code in codes:
        for year in years:
            print(f"📥 Lade {code} für Jahr {year} ...")
            path = download_and_extract_table_auto(code, year, dest_folder="data/raw")
            if path:
                df = load_genesis_csv(path, zip_name=code)  # ✅ Nur Code, nicht Code+Jahr
                if df is not None:
                    print(f"✅ Erfolgreich bereinigt: {code} ({year})")
                else:
                    print(f"⚠️ Fehler beim Bereinigen: {code} ({year})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-all", action="store_true")
    args = parser.parse_args()

    if args.run_all:
        download_and_clean_all()
