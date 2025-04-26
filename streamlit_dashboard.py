import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from genesis_preprocessing import clean_genesis_dataframe

st.set_page_config(page_title="Branchen-Cluster Dashboard", layout="wide")
st.title("Branchen-Cluster Analyse \u00fcber mehrere Jahre")

# Helper Functions
def cluster_and_pca(df, features, k):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])

    kmeans = KMeans(n_clusters=k, random_state=42)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)
    df["PCA1"] = pca_result[:, 0]
    df["PCA2"] = pca_result[:, 1]

    return df

def generate_cluster_labels(df, feature_sort=None):
    if feature_sort is None:
        feature_sort = "Umsatz_log" if "Umsatz_log" in df.columns else "Umsatz"

    cluster_means = df.groupby("Cluster")[[feature_sort]].mean().sort_values(feature_sort)
    labels = {}
    for idx, cluster in enumerate(cluster_means.index):
        if idx == 0:
            labels[cluster] = "Kleinbetriebe"
        elif idx == 1:
            labels[cluster] = "Mittelstand"
        else:
            labels[cluster] = f"Großunternehmen #{idx-1}"
    return labels


uploaded_files = st.file_uploader("W\u00e4hle eine oder mehrere CSV-Dateien (GENESIS-Format)", type="csv", accept_multiple_files=True)

if uploaded_files:
    df_list = []
    for file in uploaded_files:
        df = pd.read_csv(file, sep=";")
        parts = file.name.split("_")
        year = parts[2] if len(parts) > 2 else "Unbekannt"
        df["Jahr"] = year
        df_list.append(df)

    df_all = pd.concat(df_list, ignore_index=True)

    # Sidebar
    st.sidebar.header("Einstellungen")

    raw_features = st.sidebar.multiselect(
        "Numerische Spalten zur Analyse:",
        options=df_all.columns.tolist(),
        default=["Tätige Personen", "Umsatz"]
    )

    log_transform_umsatz = st.sidebar.checkbox("Umsatz log-transformieren?", value=True)

    jahr_auswahl = st.sidebar.multiselect(
        "Jahre auswählen:",
        options=sorted(df_all["Jahr"].unique()),
        default=sorted(df_all["Jahr"].unique())
    )

    k = st.sidebar.slider("Anzahl Cluster (k)", min_value=2, max_value=10, value=3)

    # Filtering
    df_filtered = df_all[df_all["Jahr"].isin(jahr_auswahl)]
    df_filtered = clean_genesis_dataframe(df_filtered, raw_features)

    # Optional: Log-Transformation Umsatz
    if "Umsatz" in raw_features and log_transform_umsatz:
        df_filtered["Umsatz_log"] = np.log1p(df_filtered["Umsatz"])
        features = [col if col != "Umsatz" else "Umsatz_log" for col in raw_features]
    else:
        features = raw_features

    df_clean = df_filtered.dropna(subset=features).copy()

    # Cluster und PCA anwenden
    df_clustered = cluster_and_pca(df_clean, features, k)
    cluster_labels = generate_cluster_labels(df_clustered)
    df_clustered["Cluster_Name"] = df_clustered["Cluster"].map(cluster_labels)

    #Visualisierungen
    st.subheader("PCA 2D-Visualisierung der Cluster")
    fig = px.scatter(
        df_clustered, x="PCA1", y="PCA2", color="Cluster_Name",
        hover_data=["Wirtschaftszweige"] if "Wirtschaftszweige" in df_clustered.columns else features,
        title="Cluster basierend auf: " + ", ".join(features),
        animation_frame="Jahr" if df_clustered["Jahr"].nunique() > 1 else None
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Durchschnittswerte je Cluster und Jahr")
    avg_table = df_clustered.groupby(["Jahr", "Cluster_Name"])[features].mean().round(2)
    st.dataframe(avg_table)


    if "Jahr" in df_clustered.columns:
        st.subheader("Zeitliche Entwicklung eines Merkmals")
        feature_to_plot = st.selectbox("Wähle ein Merkmal für die Zeitreihe:", features)

        zeit = df_clustered.groupby(["Jahr", "Cluster_Name"])[feature_to_plot].sum().reset_index()
        fig_line = px.line(
            zeit, x="Jahr", y=feature_to_plot, color="Cluster_Name",
            markers=True,
            title=f"Entwicklung von {feature_to_plot} über die Jahre"
        )

        st.plotly_chart(fig_line, use_container_width=True)

    #CSV Export
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        "Exportiere Cluster-Ergebnisse",
        df_clustered.to_csv(index=False, sep=";"),
        file_name="cluster_ergebnisse_mehrere_jahre.csv",
        mime="text/csv"
    )
