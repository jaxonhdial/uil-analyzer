import argparse
import pandas as pd

from backend.populate.scrape_uil_archives import (
    scrape_individual_uil_archives,
    scrape_team_uil_archives,
)
from backend.populate.scrape_speechwire import (
    scrape_individual_speechwire,
    scrape_team_speechwire,
)
from backend.populate.populate_db import (
    insert_individual_results,
    insert_team_results,
)

# Year ranges
VALID_YEARS = list(range(2015, 2026))
UIL_ARCHIVE_YEARS = list(range(2015, 2023))
SPEECHWIRE_YEARS = list(range(2023, 2026))

DEFAULT_EVENTS = [
    "Journalism team results", "Speech team results", "Overall school sweepstakes",
    "Accounting", "Computer Applications", "Current Issues and Events", "Literary Criticism",
    "Ready Writing", "Social Studies", "Spelling", "Calculator Applications", "Computer Science",
    "Mathematics", "Number Sense", "Science", "Copy Editing", "Editorial", "Feature Writing",
    "Headline Writing", "News Writing", "Informative Speaking", "Persuasive Speaking",
    "Lincoln Douglas Debate", "Poetry Interpretation", "Prose Interpretation"
]

DEFAULT_CONFERENCES = ['1', '2', '3', '4', '5', '6']
DEFAULT_LEVELS = ['district', 'region', 'state']

# Valid level inputs as strings, matching what your scrapers expect in URLs
VALID_LEVEL_INPUTS = {
    'district': [str(i) for i in range(1, 33)],
    'region': [str(i) for i in range(1, 5)],
    'state': ['1'],  # use '1' for state level (or adapt if you prefer)
}

def expand_param(param, valid_values):
    return valid_values if param == 'all' else [param]

def scrape_and_insert(year, event, conference_num, level, level_input):
    # conference_num passed as-is (e.g., '5'), no 'A' appended
    print(f"\n🔎 Scraping: year={year} event={event} conference={conference_num} level={level} level_input={level_input}")

    if year in UIL_ARCHIVE_YEARS:
        indiv_df = scrape_individual_uil_archives(year, event, conference_num, level, level_input)
        team_df = scrape_team_uil_archives(year, event, conference_num, level, level_input)
    elif year in SPEECHWIRE_YEARS:
        indiv_df = scrape_individual_speechwire(year, event, conference_num, level, level_input)
        team_df = scrape_team_speechwire(year, event, conference_num, level, level_input)
    else:
        print(f"❌ Unsupported year: {year}")
        return

    if indiv_df is not None and not indiv_df.empty:
        insert_individual_results(indiv_df)
        print(f"✅ Inserted {len(indiv_df)} individual rows")

    if team_df is not None and not team_df.empty:
        insert_team_results(team_df)
        print(f"✅ Inserted {len(team_df)} team rows")

    if (indiv_df is None or indiv_df.empty) and (team_df is None or team_df.empty):
        print("⚠️ No data returned")

def main():
    parser = argparse.ArgumentParser(description="UIL Archives Scraper")

    parser.add_argument('--year', type=str, default='all', help="e.g. 2024 or 'all'")
    parser.add_argument('--event', type=str, default='Computer Science', help="Event or 'all'")
    parser.add_argument('--conference', type=str, default='5', help="Conference number (e.g. 5 for 5A)")
    parser.add_argument('--level', type=str, default='district', help="district, region, state, or 'all'")
    parser.add_argument('--level_input', type=str, default='all', help="e.g. 6 or 'all'")

    args = parser.parse_args()

    years = VALID_YEARS if args.year == 'all' else [int(args.year)]
    events = expand_param(args.event, DEFAULT_EVENTS)
    conferences = expand_param(args.conference, DEFAULT_CONFERENCES)
    levels = expand_param(args.level, DEFAULT_LEVELS)

    for event in events:
        for year in years:
            for conference in conferences:
                for level in levels:
                    # Skip 2020 for region or state level
                    if year == 2020 and (level == "region" or level == "state"):
                        print(f"⏭️ Skipping {level} {year} due to no competition")
                        continue

                    # Expand level_input 'all' to all valid inputs for that level
                    if args.level_input == 'all':
                        level_inputs = VALID_LEVEL_INPUTS.get(level, ['1'])
                    else:
                        level_inputs = [args.level_input]

                    for level_input in level_inputs:
                        scrape_and_insert(year, event, conference, level, level_input)

if __name__ == "__main__":
    main()
