![Python Version](https://img.shields.io/badge/python-3.12.3+-blue)
# 📊 GENESIS Daten Download & Verarbeitung
___
Dieses Projekt automatisiert den **Download**, die **Verarbeitung** und **Analyse** von Daten aus der **GENESIS-Online Datenbank** des **Statistischen Bundesamts (Destatis)**.
___
## 📦 Projektübersicht


### 📁 Python-Skripte
| Datei                      | Beschreibung                                       |
|---------------------------|----------------------------------------------------|
| `download_table_auto.py`  | Automatischer Tabellen-Download per GENESIS-API   |
| `loader.py`               | Laden & Bereinigen von CSV-Dateien                |
| `merge_cleaned.py`        | Zusammenführen bereinigter Datensätze             |
| `streamlit_dashboard.py`  | Interaktive Cluster-Analyse (Streamlit-UI)        |

### 🧾 Tabellenstruktur

- `0001`, `0002`: Personal & Umsatz  
- `0003`, `0004`: Einkaufs- & Investitionsdaten

🔗 **Kombinationen**:
- `0001` + `0003` → Personal & Einkauf  
- `0002` + `0004` → Umsatz & Investitionen
---
## ⚙️ Setup

1. Virtuelle Umgebung erstellen:
   ```bash
   python -m venv .venv
   ```

2. Virtuelle Umgebung aktivieren:
   - Windows CMD:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. Erstelle eine `.env` Datei im Hauptverzeichnis:
   ```env
   GENESIS_USERNAME=dein_benutzername
   GENESIS_PASSWORD=dein_passwort
   ```
---
## ▶️ Daten herunterladen (Example)

### Einzelner Download
🔹 Einzeltabelle herunterladen & extrahieren

```bash
  python -c "from src.download_table_auto import download_and_extract_table_auto; download_and_extract_table_auto('48112-0001', '2022')"
```

### Weitere Startoptionen
🔹 Weitere Beispiele:

```bash
  python src/download_table_auto.py --table_id 48112-0002 --year 2022
  python src/download_table_auto.py --table_id 48112-0003 --year 2022
  python src/download_table_auto.py --table_id 48112-0004 --year 2022
```
---

## 📊 Analyse starten
▶️ Streamlit Dashboard (lokal)
```bash
  streamlit run .\streamlit_dashboard.py
```


## 🐳 Docker
Build & Run
```bash
  docker-compose up --build
```
Run
```bash
  docker-compose up
```
Stop
```bash
  docker-compose down
```

## ❓ Fehlermeldungen
| Meldung | Ursache & Lösung |
|--------|------------------|
| ❌ `Download fehlgeschlagen` | API-Login prüfen (`.env` korrekt?) |
| ❌ `Keine CSV im ZIP gefunden` | Tabelle ist leer oder Download fehlerhaft |
| ❌ `Kodierung nicht lesbar` | Datei defekt oder Format inkompatibel |
