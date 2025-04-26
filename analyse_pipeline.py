# analyse_pipeline.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
import numpy as np
from genesis_preprocessing import clean_genesis_dataframe

# 📄 CSV laden
file_path = ".zmp/merged/48112-0001_48112-0003_2018_merged.csv"
features = ["Tätige Personen", "Umsatz_log"]  # Log-transformierte Version verwenden

print("📥 Lade Datei:", file_path)
df_raw = pd.read_csv(file_path, sep=";")

# ✅ Jahr als Integer setzen, falls vorhanden
if "Jahr" in df_raw.columns:
    df_raw["Jahr"] = pd.to_numeric(df_raw["Jahr"], errors="coerce").astype("Int64")

# 🧹 Clean up
raw_features = ["Tätige Personen", "Umsatz"]
df = clean_genesis_dataframe(df_raw, raw_features)

# 🧮 Log-Transformation von "Umsatz"
df["Umsatz_log"] = np.log1p(df["Umsatz"])

# 🧼 Vorbereitung
print("🧹 Entferne fehlende Werte für:", features)
df_clean = df.dropna(subset=features).copy()
X = df_clean[features]
X_scaled = StandardScaler().fit_transform(X)

# 🔢 K-Means Clustering
print("🔢 Berechne Cluster mit KMeans...")
kmeans = KMeans(n_clusters=3, random_state=42)
df_clean["Cluster"] = kmeans.fit_predict(X_scaled)

# 🎨 PCA für 2D Visualisierung
print("🎨 Berechne PCA-Komponenten...")
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)
df_clean["PCA1"] = components[:, 0]
df_clean["PCA2"] = components[:, 1]

# 📊 Interaktiver Plot
print("📊 Erzeuge Cluster-Plot...")
fig = px.scatter(
    df_clean, x="PCA1", y="PCA2",
    color=df_clean["Cluster"].astype(str),
    hover_data=["Wirtschaftszweige"] + features,
    title="Branchen-Cluster basierend auf: " + ", ".join(features)
)
fig.show()

# 🧮 Mittelwerte je Cluster
print("\n📋 Mittelwerte pro Cluster:")
print(df_clean.groupby("Cluster")[features].mean())

# 📈 Zeitreihenplot je Cluster (falls 'Jahr' vorhanden)
if "Jahr" in df_clean.columns:
    print("\n📈 Erzeuge Zeitreihe nach Cluster...")
    zeit_cluster = df_clean.groupby(["Jahr", "Cluster"])[features[0]].sum().reset_index()
    fig = px.line(
        zeit_cluster, x="Jahr", y=features[0], color="Cluster",
        title=f"Zeitliche Entwicklung je Cluster ({features[0]})"
    )
    fig.show()

# 📐 Elbow-Methode zur Clusteranzahl-Bestimmung:
print("\n📐 Elbow-Methode zur Clusteranzahl-Bestimmung:")
inertia = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42).fit(X_scaled)
    inertia.append(km.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(k_range, inertia, marker="o")
plt.title("Elbow-Methode zur Bestimmung der optimalen Clusteranzahl")
plt.xlabel("Anzahl Cluster (k)")
plt.ylabel("Inertia")
plt.grid(True)
plt.show()
