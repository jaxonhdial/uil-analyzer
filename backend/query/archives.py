from backend.query.query_db import get_contest_results

def format_archives_results(year, conference, event_name, level, level_input, is_team=False):
    # Fetch raw results from the database
    df = get_contest_results(year, conference, event_name, level, level_input, is_team)
    
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

    # Apply renaming
    df = df.rename(columns=rename_map)

    # Select only the present columns in correct order
    present_cols = [col for col in column_order if col in df.columns]
    return df[present_cols]
