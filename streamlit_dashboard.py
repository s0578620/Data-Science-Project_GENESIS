# streamlit_dashboard.py
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from genesis_preprocessing import clean_genesis_dataframe

st.set_page_config(page_title="Branchen-Cluster Dashboard", layout="wide")
st.title("📊 Branchen-Cluster Analyse")

# 📁 Datei-Auswahl
uploaded_file = st.file_uploader("Wähle eine CSV-Datei aus (GENESIS-Format)", type="csv")

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file, sep=";")

    # 🧼 Spaltenauswahl
    st.sidebar.header("🔧 Einstellungen")
    raw_features = st.sidebar.multiselect(
        "Numerische Spalten zur Analyse:",
        options=df_raw.columns.tolist(),
        default=["Tätige Personen", "Umsatz"]
    )

    jahr_col = st.sidebar.selectbox("Jahr-Spalte (optional):", ["None"] + list(df_raw.columns), index=1)

    # 💡 Daten bereinigen
    df = clean_genesis_dataframe(df_raw, raw_features)
    if "Umsatz" in raw_features:
        df["Umsatz_log"] = np.log1p(df["Umsatz"])
        features = [col if col != "Umsatz" else "Umsatz_log" for col in raw_features]
    else:
        features = raw_features

    df_clean = df.dropna(subset=features).copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean[features])

    # 🔢 Cluster-Anzahl
    k = st.sidebar.slider("Anzahl Cluster (k)", min_value=2, max_value=10, value=3)
    kmeans = KMeans(n_clusters=k, random_state=42)
    df_clean["Cluster"] = kmeans.fit_predict(X_scaled)

    # 🎨 PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)
    df_clean["PCA1"] = pca_result[:, 0]
    df_clean["PCA2"] = pca_result[:, 1]

    # 📊 Cluster-Plot
    st.subheader("📍 PCA 2D-Visualisierung der Cluster")
    fig = px.scatter(
        df_clean, x="PCA1", y="PCA2", color=df_clean["Cluster"].astype(str),
        hover_data=["Wirtschaftszweige"] if "Wirtschaftszweige" in df_clean.columns else features,
        title="Cluster basierend auf: " + ", ".join(features)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📋 Kennzahlen pro Cluster
    st.subheader("📑 Durchschnittswerte je Cluster")
    st.dataframe(df_clean.groupby("Cluster")[features].mean().round(2))

    # 📈 Zeitreihe (falls vorhanden)
    if jahr_col != "None" and jahr_col in df_clean.columns:
        df_clean[jahr_col] = pd.to_numeric(df_clean[jahr_col], errors="coerce").astype("Int64")
        st.subheader("📈 Zeitliche Entwicklung je Cluster")
        zeit = df_clean.groupby([jahr_col, "Cluster"])[features[0]].sum().reset_index()
        fig = px.line(
            zeit, x=jahr_col, y=features[0], color="Cluster",
            title=f"Entwicklung von {features[0]} über Zeit"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 💾 CSV Export
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        "📥 Exportiere Cluster-Zuordnung", df_clean.to_csv(index=False, sep=";"),
        file_name="cluster_ergebnis.csv",
        mime="text/csv"
    )
