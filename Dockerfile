# Verwende explizit Python 3.12.3 als Basis
FROM python:3.12.3-slim

# Arbeitsverzeichnis
WORKDIR /app

# Systempakete installieren (z. B. für Pandas, Scikit-learn etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Anforderungen installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . .

# Port für Streamlit
EXPOSE 8501

# Startbefehl
CMD ["streamlit", "run", "streamlit_dashboard.py", "--server.port=8501", "--server.enableCORS=false"]
