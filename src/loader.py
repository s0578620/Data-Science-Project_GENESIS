# src/loader.py

import pandas as pd

def load_genesis_csv(csv_path: str, zip_name: str = None, save_cleaned: bool = True) -> pd.DataFrame:

    import os
    import pandas as pd

    encodings_to_try = ["utf-8", "utf-8-sig", "latin1"]

    for enc in encodings_to_try:
        try:
            print(f"📎 Versuche Encoding: {enc}")
            df = pd.read_csv(csv_path, sep=";", encoding=enc, header=6, skiprows=[7])
            print("📋 Geladene Spaltennamen:")
            print(df.columns.tolist())
            print(f"✅ Erfolgreich geladen mit Encoding: {enc}")

            # Letzte 3 Zeilen entfernen
            df = df[:-3]
            print(f"ℹ️ DataFrame nach Kürzen: {df.shape}")

            # Spalten explizit umbenennen (wenn vorhanden)
            df = df.rename(columns={
                "Unnamed: 0": "Jahr",
                "Unnamed: 1": "Kurzzeichen",
                "Unnamed: 2": "Wirtschaftszweige"
            })

            if save_cleaned:
                cleaned_dir = os.path.join("data", "cleaned")
                os.makedirs(cleaned_dir, exist_ok=True)

                # Nutze zip_name statt CSV-Filename
                if zip_name is None:
                    zip_basename = os.path.splitext(os.path.basename(csv_path))[0]
                else:
                    zip_basename = os.path.splitext(os.path.basename(zip_name))[0]

                cleaned_filename = f"{zip_basename}_cleaned.csv"
                cleaned_path = os.path.join(cleaned_dir, cleaned_filename)

                print(f"💾 Speichere bereinigte Datei unter: {cleaned_path}")
                df.to_csv(cleaned_path, index=False, sep=";")

                print(f"✅ Bereinigte CSV gespeichert!")

            return df
        except Exception as e:
            print(f"⚠️ Fehler mit Encoding '{enc}': {e}")

    print("❌ Fehler: Keine passende Kodierung gefunden.")
    return None