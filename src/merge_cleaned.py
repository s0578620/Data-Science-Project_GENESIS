# src/merge_cleaned.py

import os
import pandas as pd

def merge_cleaned_files(file1: str, file2: str, out_folder="data/merged") -> pd.DataFrame:
    os.makedirs(out_folder, exist_ok=True)

    print(f"🔄 Lade Dateien: {file1}, {file2}")
    df1 = pd.read_csv(file1, sep=";")
    df2 = pd.read_csv(file2, sep=";")

    print("🔗 Merging on ['Jahr', 'Kurzzeichen', 'Wirtschaftszweige']")
    merged_df = pd.merge(df1, df2, on=["Jahr", "Kurzzeichen", "Wirtschaftszweige"], how="outer")

    if "Jahr" not in merged_df.columns:
        raise Exception("❌ 'Jahr'-Spalte fehlt im Merge.")

    jahr_series = merged_df["Jahr"].dropna().astype(str)
    if jahr_series.empty:
        raise Exception("❌ Keine gültigen Jahr-Werte gefunden.")

    most_common_year = jahr_series.mode().iloc[0]
    print(f"🕵️ Dominantes Jahr im Merge: {most_common_year}")

    if "Wirtschaftszweige" in merged_df.columns:
        merged_df = merged_df[merged_df["Wirtschaftszweige"] != "Insgesamt"]

    base1 = os.path.basename(file1).split("_")[0]
    base2 = os.path.basename(file2).split("_")[0]
    combined_id = f"{base1}_{base2}"

    merged_filename = f"{combined_id}_{most_common_year}_merged.csv"
    output_path = os.path.join(out_folder, merged_filename)

    merged_df.to_csv(output_path, index=False, sep=";")
    print(f"✅ Gespeichert unter: {output_path}")

    return merged_df


