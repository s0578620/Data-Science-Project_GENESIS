python -m venv venv
source venv/bin/activate  # oder venv\Scripts\activate (Windows)
pip install -r requirements.txt


0001 & 0002: Personal- und Umsatzdaten
0003 & 0004: Einkaufs- und Investitionsdaten


Combine Data?
    1 and 3
    2 and 4


# ⚙️ Setup
1. Create a virtual environmen
```bash
  python -m venv .venv
```
2. Activate the virtual environment (Windows CMD)
```bash
  source .venv/bin/activate
```
3. Install dependencies
```bash
  pip install -r requirements.txt
```

# Start
1. Install dependencies
```bash
  python -c "from src.download_table import download_and_extract_table; download_and_extract_table('48112-0001', '2022')"
```
```start options:
Examples:
python src/download_table.py --table_id 48112-0002 --year 2022
python src/download_table.py --table_id 48112-0003 --year 2022
python src/download_table.py --table_id 48112-0004 --year 2022
