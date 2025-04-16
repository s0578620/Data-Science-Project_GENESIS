# src/merge_cleaned.py

import os
import pandas as pd

def merge_cleaned_files(file1: str, file2: str, merged_name: str, out_folder="data/merged") -> pd.DataFrame:
    os.makedirs(out_folder, exist_ok=True)

    print(f"🔄 Lade Dateien: {file1}, {file2}")
    df1 = pd.read_csv(file1, sep=";")
    df2 = pd.read_csv(file2, sep=";")

    print("🔗 Merging on ['Jahr', 'Kurzzeichen', 'Wirtschaftszweige']")
    merged_df = pd.merge(df1, df2, on=["Jahr", "Kurzzeichen", "Wirtschaftszweige"], how="outer")

    output_path = os.path.join(out_folder, merged_name)
    merged_df.to_csv(output_path, index=False, sep=";")
    print(f"✅ Gespeichert unter: {output_path}")

    return merged_df
