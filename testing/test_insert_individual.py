import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.populate.populate_db import insert_individual_results

df = pd.DataFrame([
    # Students from the same school
    {
        "student_name": "Alice Smith",
        "school_name": "Westview High",
        "event_name": "Mathematics",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "code": "5A-03",
        "placement": 1,
        "score": 240.0,
        "tiebreaker": None,
        "objective_score": 90.0,
        "essay_score": None,
        "biology_score": None,
        "chemistry_score": None,
        "physics_score": None,
        "points": 15,
        "advancement_status": "Region"
    },
    {
        "student_name": "Bob Johnson",
        "school_name": "Westview High",
        "event_name": "Mathematics",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "code": "5A-03",
        "placement": 2,
        "score": 230.0,
        "tiebreaker": 5,
        "objective_score": 85.0,
        "essay_score": None,
        "biology_score": None,
        "chemistry_score": None,
        "physics_score": None,
        "points": 12,
        "advancement_status": "Region"
    },

    # Duplicate student name, different schools
    {
        "student_name": "Alice Smith",
        "school_name": "Eastview High",  # Different school
        "event_name": "Mathematics",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "code": "5A-03",
        "placement": 3,
        "score": 220.0,
        "tiebreaker": None,
        "objective_score": 80.0,
        "essay_score": None,
        "biology_score": None,
        "chemistry_score": None,
        "physics_score": None,
        "points": 10,
        "advancement_status": "Alternate"
    },

    # Missing scores, blank advancement
    {
        "student_name": "Charlie Young",
        "school_name": "North Ridge HS",
        "event_name": "Mathematics",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "code": "5A-03",
        "placement": 4,
        "score": None,
        "tiebreaker": None,
        "objective_score": None,
        "essay_score": None,
        "biology_score": None,
        "chemistry_score": None,
        "physics_score": None,
        "points": 8,
        "advancement_status": ""
    },

    # Tie on placement
    {
        "student_name": "Dana Lee",
        "school_name": "North Ridge HS",
        "event_name": "Mathematics",
        "year": 2025,
        "level_name": "district",
        "level_input": 3,
        "conference": 5,
        "code": "5A-03",
        "placement": 4,  # Same placement as Charlie
        "score": 210.0,
        "tiebreaker": 6,
        "objective_score": 75.0,
        "essay_score": None,
        "biology_score": None,
        "chemistry_score": None,
        "physics_score": None,
        "points": 8,
        "advancement_status": ""
    }
])

insert_individual_results(df)
print("Test insert_individual_results passed.")
