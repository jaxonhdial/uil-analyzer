import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.populate.populate_db import insert_team_results

team_test_df = pd.DataFrame([
    {
        "school_name": "Westview High",
        "event_name": "Computer Science",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "placement": 1,
        "student_1_name": "Alice Smith",
        "student_2_name": "Bob Johnson",
        "student_3_name": "Charlie Young",
        "student_4_name": None,
        "score": 450.5,
        "programming_score": 400.0,
        "points": 20,
        "advancement_status": "Region"
    },
    {
        "school_name": "Eastview High",
        "event_name": "Computer Science",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "placement": 2,
        "student_1_name": "Dana Lee",
        "student_2_name": None,
        "student_3_name": None,
        "student_4_name": None,
        "score": 420.0,
        "programming_score": 390.0,
        "points": 15,
        "advancement_status": "Alternate"
    },
    {
        "school_name": "Westview High",
        "event_name": "Mathematics",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "placement": 3,
        "student_1_name": "Eve Torres",
        "student_2_name": "Frank Wright",
        "student_3_name": None,
        "student_4_name": None,
        "score": None,
        "programming_score": None,
        "points": 10,
        "advancement_status": ""
    }
])

insert_team_results(team_test_df)
print("Team results test data inserted successfully")
