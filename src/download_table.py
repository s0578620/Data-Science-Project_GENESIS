# src/download_table.py
import os
import requests
import zipfile
import io
from dotenv import load_dotenv

def download_and_extract_table(table_id: str, year: str, dest_folder="data"):
    load_dotenv()

    base_url = "https://www-genesis.destatis.de/genesisWS/rest/2020/data/tablefile"
    params = {
        "username": os.getenv("GENESIS_USERNAME"),
        "password": os.getenv("GENESIS_PASSWORD"),
        "name": table_id,
        "timeslices": year,
        "type": "csv",
        "language": "de"
    }

    os.makedirs(dest_folder, exist_ok=True)

    print(f"🌐 Anfrage an GENESIS-API: {table_id} für Jahr {year}")
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"❌ Download fehlgeschlagen: {response.status_code}, {response.text}")

    file_bytes = io.BytesIO(response.content)

    # 🗜️ ZIP-Check
    if zipfile.is_zipfile(file_bytes):
        zip_path = os.path.join(dest_folder, f"{table_id}.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
            csv_files = [f for f in zip_ref.namelist() if f.endswith(".csv")]

        if not csv_files:
            raise Exception("❌ Keine CSV-Datei im ZIP gefunden.")

        return os.path.join(dest_folder, csv_files[0])

    # 📄 Direkte CSV-Prüfung
    decoded_text = response.content.decode("utf-8", errors="ignore")
    if decoded_text.strip().startswith("﻿") or ";" in decoded_text:
        csv_path = os.path.join(dest_folder, f"{table_id}_{year}_direct.csv")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(decoded_text)
        return csv_path

    # ❗ Unerwarteter Inhalt: Ausgabe zur Analyse
    print("🪵 Serverantwort-Vorschau (erste 500 Zeichen):")
    print(decoded_text[:500])
    raise Exception("❌ Unerwartetes Dateiformat. Kein ZIP und keine CSV erkannt.")