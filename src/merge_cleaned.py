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

    # Jahr extrahieren – wir nehmen das häufigste Jahr als Referenz
    if "Jahr" not in merged_df.columns:
        raise Exception("❌ 'Jahr'-Spalte fehlt im Merge.")

    jahr_series = merged_df["Jahr"].dropna().astype(str)
    if jahr_series.empty:
        raise Exception("❌ Keine gültigen Jahr-Werte gefunden.")

    most_common_year = jahr_series.mode().iloc[0]
    print(f"🕵️ Dominantes Jahr im Merge: {most_common_year}")

    merged_base = os.path.splitext(merged_name)[0]
    merged_filename = f"{merged_base}_{most_common_year}.csv"
    output_path = os.path.join(out_folder, merged_filename)

    merged_df.to_csv(output_path, index=False, sep=";")
    print(f"✅ Gespeichert unter: {output_path}")

    return merged_df

