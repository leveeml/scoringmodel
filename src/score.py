"""
Similarity Scorer
=================

Heuristic-based model which calculates 3 scores based on Candidate-Job relations upon:

1) `education`
2) distance between Job and Candidate (`match_distance`)
3) similarity between Candidate interests (`category`, `position`, `experience`) and required Job
    (`category` and `position`)

weighted by a `betas` array.

Furthermore, let:
    - `factor` 5 / sum(betas)
    - <x, y> be the inner product of `x` and `y` d-dimensional vectors
    - logistic(α) = 1 / (1 + exp(α)) , the canonical math function

Then, the final score is defined to be
    final_score := logistic(-factor * <scores, betas>)
"""
import numpy as np

# "score_similarity", "score_education", "score_distance"
BETAS = [1, 1, 3]
MIN_VAL = -1
MAX_VAL = +1
    
def calculate_scores(X_):
    similarities = X_.filter(regex="sim_[0-2]").values
    experiences = X_.filter(regex="[0-2]_experience").values

    similarities_notnan = np.ma.MaskedArray(similarities, mask=np.isnan(similarities))
    experiences_notnan = np.ma.MaskedArray(experiences, mask=np.isnan(experiences))

    X_["avg_similarities"] = np.ma.average(similarities_notnan, axis=1)
    X_["avg_experiences_similarities"] = np.ma.average(experiences_notnan, axis=1,
                                                        weights=similarities_notnan)

    X_["score_similarity"] = X_.avg_experiences_similarities * X_.avg_similarities
    X_["score_education"] = X_.job_education / X_.candidate_education
    X_["score_distance"] = 1 / X_.match_distance

    cols_scores = list(X_.filter(like="score_"))
    for c in cols_scores:
        col_min, col_max = X_[c].min(), X_[c].max()

        # Min-Max Scaling
        X_[f"{c}_norm"] = (
            1.
            if col_max == col_min
            else ((MAX_VAL - MIN_VAL) / (col_max - col_min)) * (X_[c] - col_max) + MAX_VAL
        )

    # appending '_norm' prefix
    cols_scores_norm = list(map(lambda x: f"{x}_norm", cols_scores))

    betas_v = np.array(BETAS).reshape(3, 1)  # vertical Betas array
    factor = 5 / betas_v.sum()

    X_['score'] = 1 / (1 + np.exp(-factor * X_[cols_scores_norm].values.dot(betas_v)))

    return X_
