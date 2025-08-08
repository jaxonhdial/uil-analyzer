from backend.query.query_db import get_contest_results
import pandas as pd

def process_results_df(df, is_team=False):
    if df is None or df.empty:
        return df

    if is_team:
        rename_map = {
            "placement": "Place",
            "school_name": "School",
            "student_1": "Entry 1",
            "student_2": "Entry 2",
            "student_3": "Entry 3",
            "student_4": "Entry 4",
            "programming_score": "Programming",
            "score": "Total", 
            "points": "Points",
            "advancement_status": "Advance?",
        }
        column_order = [
            "Place", "School", "Entry 1", "Entry 2", "Entry 3", "Entry 4",
            "Programming", "Total", "Points", "Advance?"
        ]
    else:
        rename_map = {
            "placement": "Place",
            "school_name": "School",
            "student_name": "Entry",
            "code": "Code",
            "objective_score": "Objective",
            "essay_score": "Essay",
            "biology_score": "Biology",
            "chemistry_score": "Chemistry",
            "physics_score": "Physics",
            "score": "Score",
            "tiebreaker": "Tiebreaker",
            "points": "Points",
            "advancement_status": "Advance?",
        }
        column_order = [
            "Place", "School", "Entry", "Code", "Objective", "Essay",
            "Biology", "Chemistry", "Physics", "Score", "Tiebreaker", "Points", "Advance?"
        ]

    df = df.rename(columns=rename_map)
    present_cols = [col for col in column_order if col in df.columns]

    # Replace NaN in Points with an empty string
    if 'Points' in df.columns:
        df['Points'] = df['Points'].apply(lambda x: '' if pd.isna(x) or x == 0 else x)

    return df[present_cols], present_cols


def format_archives_results(year, conference, event_name, level, level_input, is_team=False):
    df = get_contest_results(year, conference, event_name, level, level_input, is_team)
    if df is None or df.empty:
        return df, []
    
    return process_results_df(df, is_team)
