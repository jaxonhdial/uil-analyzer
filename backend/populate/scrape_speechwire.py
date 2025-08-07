import requests
from bs4 import BeautifulSoup
import pandas as pd

def event_code(event):
    """Map event name to SpeechWire event code."""
    mapping = {
        # TODO: Add back in team results
        # "Journalism team results": -3,
        # "Speech team results": -2,
        # "Overall school sweepstakes": -1,
        "Accounting": 1,
        "Computer Applications": 2,
        "Current Issues and Events": 3,
        "Literary Criticism": 4,
        "Ready Writing": 5,
        "Social Studies": 6,
        "Spelling": 7,
        "Calculator Applications": 8,
        "Computer Science": 9,
        "Mathematics": 10,
        "Number Sense": 11,
        "Science": 12,
        "Copy Editing": 13,
        "Editorial": 14,
        "Feature Writing": 15,
        "Headline Writing": 16,
        "News Writing": 17,
        "Informative Speaking": 18,
        "Persuasive Speaking": 19,
        "Lincoln Douglas Debate": 20,
        "Poetry Interpretation": 21,
        "Prose Interpretation": 22,
    }
    if event not in mapping:
        raise ValueError(f"Unknown event name: {event}")
    return mapping[event]

def year_code(year):
    mapping = {2025: 17, 2024: 16, 2023: 15}
    if year not in mapping:
        raise ValueError(f"Unsupported year: {year}")
    return mapping[year]

def build_url(year, event, conference, level, level_input):
    base = "https://postings.speechwire.com/r-uil-academics.php?Submit=View+postings"
    e_code = event_code(event)
    y_code = year_code(year)

    district_number = level_input if level == "district" else ""
    region_number = level_input if level == "region" else ""
    state_number = "1" if level == "state" else ""

    url = (
        f"{base}&groupingid={e_code}&seasonid={y_code}&conference={conference}"
        f"&district={district_number}&region={region_number}&state={state_number}"
    )
    return url

def scrape_individual_table(soup):
    tables = soup.find_all("table")
    if len(tables) < 6:
        return pd.DataFrame()
    individual_table = tables[5]
    rows = individual_table.find_all("tr")
    headers = [td.get_text(strip=True) for td in rows[0].find_all("td")]
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        data.append([col.get_text(strip=True) for col in cols])
    df = pd.DataFrame(data, columns=headers)
    return df

def scrape_team_table(soup):
    tables = soup.find_all("table")
    if len(tables) < 7:
        return pd.DataFrame()
    team_table = tables[6]
    rows = team_table.find_all("tr")

    orig_headers = [td.get_text(strip=True) for td in rows[0].find_all("td")]

    new_headers = []
    for h in orig_headers:
        new_headers.append(h)
        if h == "School":
            new_headers.extend(["student_1_name", "student_2_name", "student_3_name", "student_4_name"])

    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        school_html = cols[1].decode_contents()
        school_soup = BeautifulSoup(school_html, "html.parser")
        members = list(school_soup.stripped_strings)
        members = members[:5] + [''] * (5 - len(members))  # school + 4 members

        row_data = [cols[0].get_text(strip=True)] + members + [col.get_text(strip=True) for col in cols[2:]]
        data.append(row_data)

    df = pd.DataFrame(data, columns=new_headers)
    return df

def normalize_individual_df(df, year, event_name, conference, level_name, level_input):
    if df.empty:
        return df
    col_map = {
        'Entry': 'student_name',
        'School': 'school_name',
        'Code': 'code',
        'Place': 'placement',
        'TotalScore': 'score',
        'Written': 'score',     # Used For Computer Science
        'AccuracyScore': 'tiebreaker',
        'Objective': 'objective_score',
        'EssayScore': 'essay_score',
        'ScoresTotaled': 'score',    # Used for Current Events and Social Studies
        'ScienceTotal': 'score',     # Used for Science
        'Biology': 'biology_score',
        'Chemistry': 'chemistry_score',
        'Physics': 'physics_score',
        'Points': 'points',
        'Advance?': 'advancement_status'
    }
    existing_renames = {k: v for k, v in col_map.items() if k in df.columns}
    df = df.rename(columns=existing_renames)

    for col in col_map.values():
        if col not in df.columns:
            df[col] = None

    df['event_name'] = event_name
    df['year'] = year
    df['conference'] = conference
    df['level_name'] = level_name
    df['level_input'] = level_input

    for col in ['student_name', 'school_name', 'advancement_status']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

def normalize_team_df(df, year, event_name, conference, level_name, level_input):
    if df.empty:
        return df
    col_map = {
        'Place': 'placement',
        'Total': 'score',
        'Programming': 'programming_score',
        'Points': 'points',
        'Advance?': 'advancement_status',
        'School': 'school_name',
    }
    existing_renames = {k: v for k, v in col_map.items() if k in df.columns}
    df = df.rename(columns=existing_renames)

    for col in ['placement', 'score', 'programming_score', 'points', 'advancement_status', 'school_name']:
        if col not in df.columns:
            df[col] = None

    df['event_name'] = event_name
    df['year'] = year
    df['conference'] = conference
    df['level_name'] = level_name
    df['level_input'] = level_input

    for col in ['advancement_status', 'school_name']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for i in range(1, 5):
        col = f'student_{i}_name'
        if col not in df.columns:
            df[col] = None

    return df

def scrape_speechwire(year, event, conference, level, level_input):
    url = build_url(year, event, conference, level, level_input)
    print(f"Fetching URL: {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "lxml")

    raw_individual_df = scrape_individual_table(soup)
    raw_team_df = scrape_team_table(soup)

    individual_df = normalize_individual_df(raw_individual_df, year, event, conference, level, level_input)
    team_df = normalize_team_df(raw_team_df, year, event, conference, level, level_input)

    # Debug prints — remove or comment out later
    print("Individual Results Columns:", individual_df.columns)
    print(individual_df.head())
    print("Team Results Columns:", team_df.columns)
    print(team_df.head())

    return individual_df, team_df
