# src/download_table_auto.py
import os
import time
import requests
import zipfile
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www-genesis.destatis.de/genesisWS/rest/2020/data/tablefile"
USERNAME = os.getenv("GENESIS_USERNAME")
PASSWORD = os.getenv("GENESIS_PASSWORD")

def download_and_extract_table_job(table_id: str, year: str, dest_folder="data"):
    os.makedirs(dest_folder, exist_ok=True)

    # Schritt 1: Job starten
    job_url = f"{BASE_URL}/tablefile?job=true"
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "name": table_id,
        "timeslices": year,
        "type": "csv",
        "language": "de"
    }

    print(f"🚀 Starte Job für {table_id} ({year})")
    response = requests.post(job_url, json=payload)  # ← richtiges Format

    if response.status_code != 200:
        raise Exception(f"❌ Job konnte nicht gestartet werden: {response.text}")

    job_id = response.text.strip()
    print(f"🕒 Job gestartet: {job_id}")

    # Schritt 2: Polling auf Status
    status_url = f"{BASE_URL}/statusfile?job={job_id}"
    for i in range(30):
        print(f"⏳ Warte auf Fertigstellung... ({i+1}/30)")
        time.sleep(5)
        status_resp = requests.get(status_url)
        if status_resp.status_code != 200:
            continue
        if "ZIP" in status_resp.text.upper():
            break
    else:
        raise Exception("❌ Zeitüberschreitung beim Warten auf Fertigstellung")

    # Schritt 3: Datei abrufen
    file_url = f"{BASE_URL}/resultfile?job={job_id}"
    result = requests.get(file_url)
    if result.status_code != 200:
        raise Exception(f"❌ Fehler beim Ergebnis-Download: {result.text}")

    zip_path = os.path.join(dest_folder, f"{table_id}_{year}_job.zip")
    with open(zip_path, "wb") as f:
        f.write(result.content)

    # Schritt 4: Entpacken
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
        csv_files = [f for f in zip_ref.namelist() if f.endswith(".csv")]

    if not csv_files:
        raise Exception("❌ Keine CSV-Datei im Ergebnis-ZIP gefunden.")

    csv_path = os.path.join(dest_folder, csv_files[0])
    print(f"✅ CSV extrahiert: {csv_path}")
    return csv_path
