import pandas as pd


def link_records(anon_file, aux_file):

    # load datasets
    anon_df = pd.read_csv(anon_file)
    aux_df = pd.read_csv(aux_file)

    # create a matching key
    anon_df["key"] = list(zip(anon_df["age"], anon_df["zip3"], anon_df["gender"]))
    aux_df["key"] = list(zip(aux_df["age"], aux_df["zip3"], aux_df["gender"]))

    # count occurrences of each key in auxiliary data
    key_counts = aux_df["key"].value_counts()

    # store matches that appear exactly once
    unique_matches = {}

    for key, count in key_counts.items():
        if count == 1:
            name = aux_df[aux_df["key"] == key]["name"].iloc[0]
            unique_matches[key] = name

    # map matches back to anonymized dataset
    anon_df["predicted_name"] = anon_df["key"].map(unique_matches)

    return anon_df


def calculate_success_rate(linked_df):


    total_records = len(linked_df)

    matched_records = linked_df["predicted_name"].notna().sum()

    success_rate = matched_records / total_records

    return success_rate


def main():

    anon_file = "anonymized.csv"
    aux_file = "auxiliary.csv"

    linked_df = link_records(anon_file, aux_file)

    success_rate = calculate_success_rate(linked_df)

    print("Deanonymization Success Rate:", success_rate)

    # optional: save results
    linked_df.to_csv("linked_results.csv", index=False)


if __name__ == "__main__":
    main()