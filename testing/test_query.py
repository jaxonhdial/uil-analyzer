from backend.query.query_db import get_contest_results 

# === Test Parameters ===
year = 2024
conference = 6
level = "region"
level_input = 3
events_to_test = [
    "Computer Science",
    "Calculator Applications",
    "Number Sense",
    "Mathematics",
    "Science",
    "Literary Criticism"
]

for event in events_to_test:
    print(f"\n=== {event} (Individual) ===")
    try:
        df_ind = get_contest_results(year, conference, event, level, level_input, is_team=False)
        print(df_ind.head())
    except Exception as e:
        print(f"Failed to get individual results for {event}: {e}")

    print(f"\n=== {event} (Team) ===")
    try:
        df_team = get_contest_results(year, conference, event, level, level_input, is_team=True)
        print(df_team.head())
    except Exception as e:
        print(f"Failed to get team results for {event}: {e}")
