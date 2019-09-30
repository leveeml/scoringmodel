"""
Similarities data load and preparation functions.
"""
import pandas as pd


SIMILARITY_COLUMNS = ["category_id_a", "position_id_a", "category_id_b", "position_id_b", "lemma_similarity"]


def load_similarity_data():
    """
    Load similarities data and prepares for usage.

    :return: pd.DataFrame the similarities dataframe.
    """
    from src.constants import PROJECT_PATH

    return (
        pd
        .read_csv(PROJECT_PATH / "resources/similarities_lemma.csv.gz", usecols=SIMILARITY_COLUMNS)
        .rename(columns={"lemma_similarity": "val"})
        .fillna(0)
        .set_index(SIMILARITY_COLUMNS[:-1])
    )


def get_similarities(df, sims_df):
    from src.constants import DEFAULT_CANDIDATE_INTERESTS_LENGTH

    df_columns = list(df)

    for i in range(DEFAULT_CANDIDATE_INTERESTS_LENGTH):
        check_cols = [f"candidate_interests_{i}_{c}" for c in ["category", "position", "experience"]]
        sim_i = f"sim_{i}"

        if not all([c in df_columns for c in check_cols]):
            for c in check_cols + [sim_i]:
                df[c] = pd.np.nan

            continue

        df = df.merge(
            sims_df, how="left",
            right_index=True,
            left_on=[
                f"candidate_interests_{i}_category", f"candidate_interests_{i}_position",
                "job_category", "job_position"
            ]
        ).rename(columns={"val": sim_i})

    return df
