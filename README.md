#  Similarity Scoring Model

Simple score mechanism to rank candidates to a job spot.
This model uses distance and similarity between the job category/position and the candidate interests.
It also considers the distace of the job location and the candidates residence as a weight factor.

## TL;DR:

Run the server:

```bash
docker build -t score .
docker run -p 3000:3000 score
```

Test it with the sample provided

```bash
curl -XPOST http://localhost:3000/score/invocations -d @sample.json
```

Outputs:

```json
[
    {
        "candidate_id": 987,
        "job_id": 654,
        "score": 0.9933071491,
        "model": "similarity",
        "version": "1.0.0"
    }
]
```
The `score` value is the percentage of similarity between the candidate and the job weighted with the distance.

## Request details

The request spects a json body with the following format:

```json
[
    {
        "job_id": 654,
        "job_category": 1,
        "job_position": 3,
        "job_education": 1,
        "candidate_id": 987,
        "candidate_interests_1_category": 1,
        "candidate_interests_1_position": 3,
        "candidate_interests_1_experience": 6,
        "candidate_interests_2_category": 17,
        "candidate_interests_2_position": 46,
        "candidate_interests_2_experience": 1,
        "candidate_interests_3_category": 59,
        "candidate_interests_3_position": 60,
        "candidate_interests_3_experience": 1,
        "candidate_education": 1,
        "match_distance": 12
    }
]
```

Those fields are used to identify the candidate and job (ids), the similarity between them using the category and positions and the education correlation index.

`job_education` and `candidate_education` should be represented by the following map:

```
any                  1
none                 1
primary_initial      2
primary              3
secondary_incomplete 4
secondary_complete   5
higher_incomplete    6
higher_complete      7
```

`match_distance` is the distance between the work place and the candidates residence.

Available category/positions similarities:

```csv
category_id,position_id,position_title
1,2,Call center operator
1,3,Call center operator 2
1,7,Call center operator 3
1,87,Call center operator 4
1,88,Call center operator 5
4,5,Waiter
4,6,Waiter 2
4,10,Waiter 3
4,11,Waiter 4
4,12,Waiter 5
13,19,Salesperson
13,20,Salesperson 2
13,21,Salesperson 3
13,22,Salesperson 4
13,23,Salesperson 5
13,85,Salesperson 6
13,86,Salesperson 7
```
