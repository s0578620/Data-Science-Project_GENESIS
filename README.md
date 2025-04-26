# 📊 GENESIS Daten Download & Verarbeitung

Dieses Projekt lädt Daten aus der **GENESIS-Online Datenbank** der **Destatis** herunter, extrahiert und verarbeitet CSV-Dateien und führt bereinigte Datensätze zusammen.

---

## 📦 Inhalte
- `download_table_auto.py`: Automatischer Download von Tabellen über die GENESIS-API.
- `loader.py`: Laden und Bereinigen der heruntergeladenen CSV-Dateien.
- `merge_cleaned.py`: Zusammenführen von zwei bereinigten CSV-Dateien.

Tabellen:
- **0001** & **0002**: Personal- und Umsatzdaten
- **0003** & **0004**: Einkaufs- und Investitionsdaten

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

## ▶️ Start

### Einzelner Download
Direkter Download einer Tabelle und Extraktion:

```bash
  python -c "from src.download_table_auto import download_and_extract_table_auto; download_and_extract_table_auto('48112-0001', '2022')"
```

### Weitere Startoptionen
Beispiele für den Download:

```bash
  python src/download_table_auto.py --table_id 48112-0002 --year 2022
  python src/download_table_auto.py --table_id 48112-0003 --year 2022
  python src/download_table_auto.py --table_id 48112-0004 --year 2022
```

(Bei Bedarf kannst du ein kleines CLI-Skript ergänzen, um `download_table_auto.py` direkt ausführbar zu machen.)

---

## 🛠️ Daten Bereinigen

Nach dem Download kannst du die CSV-Dateien bereinigen:

```bash
  python -c "from src.loader import load_genesis_csv; load_genesis_csv('data/48112-0001_2022.csv', '48112-0001_2022.zip')"
```

Wiederhole dies für jede heruntergeladene Tabelle.

---

## 🔗 Daten Zusammenführen

Um zwei bereinigte CSVs zu kombinieren:

```bash
  python -c "from src.merge_cleaned import merge_cleaned_files; merge_cleaned_files('data/cleaned/48112-0001_2022_cleaned.csv', 'data/cleaned/48112-0003_2022_cleaned.csv')"
```

oder

```bash
  python -c "from src.merge_cleaned import merge_cleaned_files; merge_cleaned_files('data/cleaned/48112-0002_2022_cleaned.csv', 'data/cleaned/48112-0004_2022_cleaned.csv')"
```

---

## 📚 Hinweise

- `0001` und `0003` sollten kombiniert werden (Personal- und Einkaufsdaten).
- `0002` und `0004` sollten kombiniert werden (Umsatz- und Investitionsdaten).

---

## ❓ Fehlermeldungen

- **"❌ Download fehlgeschlagen"**: Prüfe API-Zugangsdaten.
- **"❌ Keine CSV-Datei im ZIP gefunden"**: Eventuell ist die Tabelle leer oder Download fehlgeschlagen.
- **"❌ Keine passende Kodierung gefunden"**: Datei könnte beschädigt oder nicht im erwarteten Format sein.

