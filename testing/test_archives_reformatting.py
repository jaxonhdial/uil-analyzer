from backend.query.archives import format_archives_results

df_team = format_archives_results(
    year=2024,
    conference=6,
    level_input=3,
    level='region',
    event_name='Computer Science',
    is_team=True
)

df_ind = format_archives_results(
    year=2024,
    conference=6,
    level_input=3,
    level='region',
    event_name='Science',
    is_team=False
)

print("=== Computer Science (Team) ===")
print(df_team)

print("\n=== Science (Individual) ===")
print(df_ind)
