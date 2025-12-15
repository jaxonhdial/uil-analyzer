import argparse
import time
import traceback
import sys

from backend.populate.scrape_uil_archives import scrape_uil_archives
from backend.populate.scrape_speechwire import scrape_speechwire
from backend.populate.populate_db import insert_individual_results, insert_team_results

VALID_YEARS = list(range(2015, 2026))
UIL_ARCHIVE_YEARS = list(range(2015, 2023))
SPEECHWIRE_YEARS = list(range(2023, 2026))

DEFAULT_EVENTS = [
    "Accounting", "Computer Applications", "Current Issues and Events", "Literary Criticism",
    "Ready Writing", "Social Studies", "Spelling", "Calculator Applications", "Computer Science",
    "Mathematics", "Number Sense", "Science", "Copy Editing", "Editorial", "Feature Writing",
    "Headline Writing", "News Writing", "Informative Speaking", "Persuasive Speaking",
    "Lincoln Douglas Debate", "Poetry Interpretation", "Prose Interpretation"
]

DEFAULT_CONFERENCES = ['1', '2', '3', '4', '5', '6']
DEFAULT_LEVELS = ['district', 'region', 'state']
VALID_LEVEL_INPUTS = {
    'district': [str(i) for i in range(1, 33)],
    'region': [str(i) for i in range(1, 5)],
    'state': ['1'],
}


def with_exponential_retry(fn, max_retries=5, base_delay=1):
    attempt = 0
    while True:
        try:
            return fn()
        except Exception:
            attempt += 1
            if attempt > max_retries:
                print("❌ Max retries exceeded. Aborting run.")
                traceback.print_exc()
                sys.exit(1)
            delay = base_delay * (2 ** (attempt - 1))
            print(f"⚠️ Scrape failed (attempt {attempt}/{max_retries}). Retrying in {delay}s...")
            time.sleep(delay)


def scrape_and_insert(year, event, conference, level, level_input, scrape_order_id):
    print(f"\n🔎 [{scrape_order_id}] Scraping: year={year} event={event} "
          f"conference={conference} level={level} level_input={level_input}")

    def scrape():
        if year in UIL_ARCHIVE_YEARS:
            return scrape_uil_archives(year, event, conference, level, level_input)
        elif year in SPEECHWIRE_YEARS:
            return scrape_speechwire(year, event, conference, level, level_input)
        else:
            raise ValueError(f"Unsupported year: {year}")

    indiv_df, team_df = with_exponential_retry(scrape)

    if indiv_df is not None and not indiv_df.empty:
        indiv_df["scrape_order_id"] = scrape_order_id
        insert_individual_results(indiv_df)
        print(f"✅ Inserted {len(indiv_df)} individual rows")

    if team_df is not None and not team_df.empty:
        team_df["scrape_order_id"] = scrape_order_id
        insert_team_results(team_df)
        print(f"✅ Inserted {len(team_df)} team rows")


def expand_param(param, valid_values):
    return valid_values if param == 'all' else [param]


def main():
    parser = argparse.ArgumentParser(description="UIL Archives Scraper")
    parser.add_argument('--year', type=str, default='all')
    parser.add_argument('--event', type=str, default='Computer Science')
    parser.add_argument('--conference', type=str, default='5')
    parser.add_argument('--level', type=str, default='district')
    parser.add_argument('--level_input', type=str, default='all')
    args = parser.parse_args()

    years = VALID_YEARS if args.year == 'all' else [int(args.year)]
    events = expand_param(args.event, DEFAULT_EVENTS)
    conferences = expand_param(args.conference, DEFAULT_CONFERENCES)
    levels = expand_param(args.level, DEFAULT_LEVELS)

    scrape_order_id = 0

    for event in events:
        for year in years:
            for conference in conferences:
                for level in levels:
                    if year == 2020 and level in ("region", "state"):
                        continue

                    level_inputs = VALID_LEVEL_INPUTS.get(level, ['1']) if args.level_input == 'all' else [args.level_input]

                    for level_input in level_inputs:
                        scrape_order_id += 1
                        scrape_and_insert(year, event, conference, level, level_input, scrape_order_id)
                        time.sleep(1)

    print("🎉 Scraping complete.")


if __name__ == "__main__":
    main()
