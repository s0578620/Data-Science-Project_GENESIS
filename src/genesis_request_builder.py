# src/genesis_request_builder.py

import os
import time
import re
import requests
import zipfile
from dotenv import load_dotenv

load_dotenv()

TABLEFILE_URL = "https://www-genesis.destatis.de/genesisWS/rest/2020/data/tablefile"
RESULTFILE_URL = "https://www-genesis.destatis.de/genesisWS/rest/2020/data/resultfile"

def start_job_and_get_resultname(table_id, years, file_format="csv"):
    params = {
        "username": os.getenv("GENESIS_USERNAME"),
        "password": os.getenv("GENESIS_PASSWORD"),
        "name": table_id,
        "timeslices": years,
        "format": file_format,
        "language": "de",
        "job": "true",
        "compress": "false",
        "area": "all"
    }

    print(f"📡 Starte Hintergrund-Job für Tabelle {table_id}...")
    response = requests.get(TABLEFILE_URL, params=params)
    if response.status_code != 200:
        print("❌ Fehler beim Jobstart:", response.status_code)
        print(response.text)
        return None

    response_json = response.json()
    status_text = response_json.get("Status", {}).get("Content", "")
    print(f"📥 Server-Antwort: {status_text}")

    # Ergebnisname per Regex extrahieren
    match = re.search(rf"({table_id}_[\d]+)", status_text)
    if match:
        resultname = match.group(1)
        print(f"📦 Ergebnisname erkannt: {resultname}")
        return resultname

    print("❌ Kein Ergebnisname erkannt.")
    return None


from tqdm import tqdm

def wait_and_download_result(resultname, file_format, filename, max_wait=3000, interval=30):
    params = {
        "username": os.getenv("GENESIS_USERNAME"),
        "password": os.getenv("GENESIS_PASSWORD"),
        "name": resultname,
        "format": file_format,
        "area": "all",
        "language": "de"
    }

    print(f"⏳ Warte auf Verfügbarkeit von: {resultname}")
    attempts = max_wait // interval

    with tqdm(total=attempts, desc="🔄 Wartezeit", bar_format="{l_bar}{bar} ⏱️ {remaining}") as pbar:
        for i in range(attempts):
            time.sleep(interval)
            elapsed = (i + 1) * interval
            mins, secs = divmod(elapsed, 60)
            time_string = f"{mins:02}:{secs:02}"
            tqdm.write(f"⌛ {time_string} Minuten vergangen – prüfe erneut...")

            response = requests.get(RESULTFILE_URL, params=params)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")

                try:
                    possible_error = response.json()
                    if "Status" in possible_error and possible_error["Status"].get("Code") == 104:
                        tqdm.write("⚠️ Noch nicht fertig (Code 104 im JSON bei HTTP 200) – warte weiter...")
                        pbar.update(1)
                        continue
                    else:
                        tqdm.write("⚠️ JSON-Antwort erkannt – kein gültiger Download")
                        pbar.update(1)
                        continue
                except ValueError:
                    # Kein JSON = gültige Datei ✅
                    pass

                tqdm.write("✅ Ergebnis verfügbar – lade herunter...")

                if "zip" in content_type:
                    filename = filename if filename.endswith(".zip") else filename + ".zip"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"✅ ZIP-Datei gespeichert als: {filename}")

                    with zipfile.ZipFile(filename, 'r') as zip_ref:
                        zip_ref.extractall("daten_output")
                    print("📂 Entpackt in 'daten_output'")
                else:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"✅ Datei gespeichert als: {filename}")
                return

            try:
                error_json = response.json()
                status_code = error_json.get("Status", {}).get("Code", None)
                if status_code == 104:
                    tqdm.write(f"🔄 Noch nicht fertig (Server-Code 104)")
                else:
                    tqdm.write(f"⚠️ Serverfehler: {status_code} → {error_json}")
            except Exception:
                tqdm.write("⚠️ Unerwartete Antwort – kein JSON")

            pbar.update(1)

    raise TimeoutError(f"❌ Zeitüberschreitung: Ergebnis '{resultname}' nicht innerhalb von {max_wait // 60} Minuten verfügbar.")

if __name__ == "__main__":
    #table_id = input("🧾 Tabellen-ID (z. B. 48112-0004): ").strip()
    table_id = "48112-0003"
    #year = input("📅 Jahr(e) (z. B. 2018): ").strip()
    year = "2018"
    #file_format = input("📂 Format (csv, xlsx) [csv]: ").strip() or "csv"
    file_format = "csv"
    filename = input("💾 Dateiname [genesis_download.csv]: ").strip() or "genesis_download.csv"

    resultname = start_job_and_get_resultname(table_id, year, file_format)
    if resultname:
        wait_and_download_result(resultname, file_format, filename)
