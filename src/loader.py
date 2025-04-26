# src/loader.py
import os
import pandas as pd

def load_genesis_csv(csv_path: str, zip_name: str, save_cleaned: bool = True) -> pd.DataFrame:
    encodings_to_try = ["utf-8", "utf-8-sig", "latin1"]

    for enc in encodings_to_try:
        try:
            print(f"📎 Versuche Encoding: {enc}")
            df = pd.read_csv(csv_path, sep=";", encoding=enc, header=6, skiprows=[7])
            print("📋 Geladene Spaltennamen:")
            print(df.columns.tolist())
            print(f"✅ Erfolgreich geladen mit Encoding: {enc}")

            df = df[:-3]
            print(f"ℹ️ DataFrame nach Kürzen: {df.shape}")

            df = df.rename(columns={
                "Unnamed: 0": "Jahr",
                "Unnamed: 1": "Kurzzeichen",
                "Unnamed: 2": "Wirtschaftszweige"
            })

            if save_cleaned:
                cleaned_dir = os.path.join("data", "cleaned")
                os.makedirs(cleaned_dir, exist_ok=True)

                zip_basename = os.path.splitext(os.path.basename(zip_name))[0]

                jahr_col = None
                for col in df.columns:
                    if "jahr" in col.lower():
                        jahr_col = col
                        break

                if not jahr_col:
                    raise Exception("❌ Keine 'Jahr'-Spalte gefunden.")

                first_year = str(df[jahr_col].iloc[0])
                print(f"🕵️ Jahr-Spalte erkannt als: '{jahr_col}', erster Wert: {first_year}")

                cleaned_filename = f"{zip_basename}_{first_year}_cleaned.csv"
                cleaned_path = os.path.join(cleaned_dir, cleaned_filename)

                print(f"💾 Speichere bereinigte Datei unter: {cleaned_path}")
                df.to_csv(cleaned_path, index=False, sep=";")
                print("✅ Bereinigte CSV gespeichert!")

            return df

        except Exception as e:
            print(f"⚠️ Fehler mit Encoding '{enc}': {e}")

    print("❌ Fehler: Keine passende Kodierung gefunden.")
    return None
