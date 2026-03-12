import pandas as pd


def load_data(anon_path, aux_path):

    anon = pd.read_csv(anon_path)
    aux = pd.read_csv(aux_path)
    return anon, aux


def link_records(anon, aux):

    #create a matching key
    anon["key"] = list(zip(anon["age"], anon["gender"], anon["zip3"]))
    aux["key"] = list(zip(aux["age"], aux["gender"], aux["zip3"]))

    #merge datasets on key
    merged = pd.merge(anon, aux[["key", "name"]], on="key", how="left")

    key_counts = merged["key"].value_counts()

    unique_keys = key_counts[key_counts == 1].index

    merged["matched_name"] = merged.apply(
        lambda row: row["name"] if row["key"] in unique_keys else pd.NA, axis=1
    )

    #drop helper columns
    merged = merged.drop(columns=["key", "name"])

    return merged


def deanonymization_rate(matches, anon):

    total_records = len(anon)
    matched_records = matches["matched_name"].notna().sum()
    rate = matched_records / total_records
    return rate