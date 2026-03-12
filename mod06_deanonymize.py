import pandas as pd


def load_data(anon_path, aux_path):
    # Load both datasets
    anon = pd.read_csv(anon_path)
    aux = pd.read_csv(aux_path)

    return anon, aux


def link_records(anon, aux):

    # create a matching key
    anon["key"] = list(zip(anon["age"], anon["gender"], anon["zip3"]))
    aux["key"] = list(zip(aux["age"], aux["gender"], aux["zip3"]))

    # count occurrences in auxiliary dataset
    key_counts = aux["key"].value_counts()

    # store unique matches
    unique_matches = {}

    for key, count in key_counts.items():
        if count == 1:
            name = aux[aux["key"] == key]["name"].iloc[0]
            unique_matches[key] = name

    # map predicted names
    anon["matched_name"] = anon["key"].map(unique_matches)
    return anon


def deanonymization_rate(matches, anon):

    total_records = len(anon)

    matched_records = matches["matched_name"].notna().sum()

    rate = matched_records / total_records

    return rate