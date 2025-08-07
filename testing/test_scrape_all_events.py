import time

from backend.populate.scraper import scrape_and_insert

EVENTS = [
    "Accounting",
    "Calculator Applications",
    "Computer Applications",
    "Computer Science",
    "Copy Editing",
    "Current Issues and Events",
    "Editorial",
    "Feature Writing",
    "Headline Writing",
    "Informative Speaking",
    "Lincoln Douglas Debate",
    "Literary Criticism",
    "Mathematics",
    "News Writing",
    "Number Sense",
    "Persuasive Speaking",
    "Poetry Interpretation",
    "Prose Interpretation",
    "Ready Writing",
    "Science",
    "Social Studies",
    "Spelling"
]

def test_all_events():
    year = 2024
    conference = 6
    level = "region"
    level_input = 3
    
    for event in EVENTS:
        print("=" * 50)
        print(f"Testing event: {event}")
        try:
            scrape_and_insert(year, event, conference, level, level_input)
        except Exception as e:
            print(f"❌ Failed for {event}: {e}")

        time.sleep(1)

if __name__ == "__main__":
    test_all_events()
