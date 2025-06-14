# genesis_preprocessing.py
import pandas as pd


def clean_genesis_dataframe(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    """
    Bereinigt typische Platzhalter aus GENESIS-Daten und konvertiert Features zu float.

    Args:
        df: Ursprünglicher DataFrame mit rohen Daten.
        features: Liste der numerischen Spalten, die bereinigt werden sollen.

    Returns:
        Bereinigter DataFrame mit NaNs und floats in den Features.
    """
    platzhalter = [".", "-", "…", "k.A.", "k. A.", "na", "n.a.", ""]

    df = df.copy()
    df.replace(platzhalter, pd.NA, inplace=True)

    for col in features:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            print(f"⚠️ Spalte '{col}' nicht gefunden!")

    return df

if __name__ == "__main__":
    raw_df = pd.read_csv("data/merged/48112-0002_48112-0004_2022_merged.csv", sep=";")

    features = ["Tätige Personen", "Umsatz"]
    clean_df = clean_genesis_dataframe(raw_df, features)

    print(clean_df[features].dtypes)
    print(clean_df[features].isna().sum())
