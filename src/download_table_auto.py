# src/download_table_auto.py
import os
import time
import requests
import zipfile
import io
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www-genesis.destatis.de/genesisWS/rest/2020/data"
USERNAME = os.getenv("GENESIS_USERNAME")
PASSWORD = os.getenv("GENESIS_PASSWORD")


def download_and_extract_table(table_id: str, year: str, dest_folder="data"):
    url = f"{BASE_URL}/tablefile"
    params = {
        "username": USERNAME,
        "password": PASSWORD,
        "name": table_id,
        "startyear": year,
        "endyear": year,
        "type": "csv",
        "language": "de"
    }

    os.makedirs(dest_folder, exist_ok=True)
    print(f"🌐 Anfrage an GENESIS-API: {table_id} für Jahr {year}")
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"❌ Download fehlgeschlagen: {response.status_code}, {response.text}")

    file_bytes = io.BytesIO(response.content)

    if zipfile.is_zipfile(file_bytes):
        zip_path = os.path.join(dest_folder, f"{table_id}_{year}.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
            csv_files = [f for f in zip_ref.namelist() if f.endswith(".csv")]
        if not csv_files:
            raise Exception("❌ Keine CSV-Datei im ZIP gefunden.")
        return os.path.join(dest_folder, csv_files[0])

    decoded = response.content.decode("utf-8", errors="ignore")
    if decoded.strip().startswith("﻿") or ";" in decoded:
        csv_path = os.path.join(dest_folder, f"{table_id}_{year}_direct.csv")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(decoded)
        return csv_path

    print("🪵 Serverantwort-Vorschau (erste 500 Zeichen):")
    print(decoded[:500])
    raise Exception("❌ Unerwartetes Dateiformat. Kein ZIP und keine CSV erkannt.")

def download_and_extract_table_job(table_id: str, year: str, dest_folder="data"):
    os.makedirs(dest_folder, exist_ok=True)
    job_url = f"{BASE_URL}/tablefile?job=true"
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "name": table_id,
        "startyear": year,
        "endyear": year,
        "type": "csv",
        "language": "de"
    }

    print(f"🚀 Starte Job für {table_id} ({year})")

    response = requests.post(job_url, data=payload)

    if response.status_code != 200:
        raise Exception(f"❌ Job konnte nicht gestartet werden: {response.text}")

    job_id = response.text.strip()
    print(f"🕒 Job gestartet: {job_id}")

    status_url = f"{BASE_URL}/statusfile?job={job_id}"
    for i in range(30):
        print(f"⏳ Warte auf Fertigstellung... ({i+1}/30)")
        time.sleep(5)
        status_resp = requests.get(status_url)
        if status_resp.status_code == 200 and "ZIP" in status_resp.text.upper():
            break
    else:
        raise Exception("❌ Zeitüberschreitung beim Warten auf Fertigstellung")

    file_url = f"{BASE_URL}/resultfile?job={job_id}"
    result = requests.get(file_url)
    if result.status_code != 200:
        raise Exception(f"❌ Fehler beim Ergebnis-Download: {result.text}")

    zip_path = os.path.join(dest_folder, f"{table_id}_{year}_job.zip")
    with open(zip_path, "wb") as f:
        f.write(result.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
        csv_files = [f for f in zip_ref.namelist() if f.endswith(".csv")]

    if not csv_files:
        raise Exception("❌ Keine CSV-Datei im Ergebnis-ZIP gefunden.")

    csv_path = os.path.join(dest_folder, csv_files[0])
    print(f"✅ CSV extrahiert: {csv_path}")
    return csv_path

def download_and_extract_table_auto(table_id: str, year: str, dest_folder="data"):
    try:
        print("⚡ Versuche Direkt-Download...")
        return download_and_extract_table(table_id, year, dest_folder)
    except Exception as e:
        if "zu gross" in str(e).lower() or "unerwartetes" in str(e).lower():
            print("↪️ Fallback: Job-Modus...")
            return download_and_extract_table_job(table_id, year, dest_folder)
        raise
