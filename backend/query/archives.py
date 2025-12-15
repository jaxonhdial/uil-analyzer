from backend.query.query_db import get_contest_results
import pandas as pd

def is_empty_value(x):
    if pd.isna(x):
        return True
    if isinstance(x, str):
        normalized = x.replace('\xa0', ' ').strip()
        return normalized == ''
    if isinstance(x, (int, float)):
        return x == 0
    return False

def process_results_df(df, is_team=False):
    if df is None or df.empty:
        return df, []

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

    # Replace NaN or 0 in Points and Essay with empty string
    if 'Points' in df.columns:
        df['Points'] = df['Points'].apply(lambda x: '' if pd.isna(x) or x == 0 else x)
    if 'Essay' in df.columns:
        df['Essay'] = df['Essay'].apply(lambda x: '' if pd.isna(x) or x == 0 else x)

    # Drop columns that are entirely empty or empty strings
    for col in present_cols[:]:
        if col in df.columns:
            if df[col].apply(is_empty_value).all():
                df.drop(columns=[col], inplace=True)
                present_cols.remove(col)

    # Now drop rows where all numeric/score columns are zero or empty
    # Define columns to check for zeros: exclude Place, School, Entry, Code, Advance? columns
    non_numeric_cols = {"Place", "School", "Entry", "Code", "Advance?", "Entry 1", "Entry 2", "Entry 3", "Entry 4"}
    cols_to_check = [col for col in present_cols if col not in non_numeric_cols]

    if cols_to_check:
        def row_is_all_zero_or_empty(row):
            # Treat empty strings or NaN as zero for numeric columns
            return all(
                (pd.isna(val) or val == '' or val == 0 or (isinstance(val, str) and val.strip() == ''))
                for val in row[cols_to_check]
            )

        df = df.loc[~df.apply(row_is_all_zero_or_empty, axis=1)]

    return df[present_cols], present_cols

def format_archives_results(year, conference, event_name, level, level_input, is_team=False):
    df = get_contest_results(year, conference, event_name, level, level_input, is_team)
    if df is None or df.empty:
        return df, []
    
    return process_results_df(df, is_team)
