import requests
from bs4 import BeautifulSoup
import pandas as pd

def event_code(event):
    """Map event name to UIL Archives event code."""
    mapping = {
        # TODO: Add back in team results
        # "Journalism team results": -3,
        # "Speech team results": -2,
        # "Overall school sweepstakes": -1,
        "Accounting": "ACC",
        "Computer Applications": "COM",
        "Current Issues and Events": "CIE",
        "Literary Criticism": "LIT",
        "Ready Writing": "RWR",
        "Social Studies": "SOC",
        "Spelling": "SPV",
        "Calculator Applications": "CAL",
        "Computer Science": "CSC",
        "Mathematics": "MTH",
        "Number Sense": "NUM",
        "Science": "SCI",
        "Copy Editing": "CPY",
        "Editorial": "EWR",
        "Feature Writing": "FWR",
        "Headline Writing": "HWR",
        "News Writing": "NWR",
        "Informative Speaking": "INF",
        "Persuasive Speaking": "PER",
        "Lincoln Douglas Debate": "LDD",
        "Poetry Interpretation": "POE",
        "Prose Interpretation": "PRO",
    }
    if event not in mapping:
        raise ValueError(f"Unknown event name: {event}")
    return mapping[event]

def level_code(level):
    if level == "district":
        l_code = "D"
    elif level == "region":
        l_code = "R"
    elif level == "state":
        l_code = "S"
    else:
        raise ValueError(f"Unsupported level: {level}")
    return l_code

def build_url(year, event, conference, level, level_input):
    base = "https://utdirect.utexas.edu/nlogon/uil/vlcp_pub_arch.WBX"
    e_code = event_code(event)
    c_code = conference + "A"
    l_code = level_code(level)
    url = (
        f"{base}?s_year={year}&s_conference={c_code}&s_level_id={l_code}"
        f"&s_level_nbr={level_input}&s_event_abbr={e_code}&s_submit_sw=X"
    )
    return url

def scrape_individual_table(soup):
    tables = soup.find_all("table")
    if len(tables) < 1:
        return pd.DataFrame()
    individual_table = tables[0]
    rows = individual_table.find_all("tr")
    headers = [td.get_text(strip=True) for td in rows[0].find_all("td")]
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        data.append([col.get_text(strip=True) for col in cols])
    return pd.DataFrame(data, columns=headers)

def scrape_team_table(soup, is_science):
    tables = soup.find_all("table")
    team_table = None

    if is_science and len(tables) >= 3:
        team_table = tables[2]
    elif not is_science and len(tables) >= 2:
        team_table = tables[1]
    
    if team_table is None:
        return pd.DataFrame()

    rows = team_table.find_all("tr")
    headers = [td.get_text(strip=True) for td in rows[0].find_all("td")]
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        data.append([col.get_text(strip=True) for col in cols])
    return pd.DataFrame(data, columns=headers)

def normalize_name(name: str) -> str:
    """Convert 'Last, First' to 'First Last'."""
    if not name or ',' not in name:
        return name.strip()
    last, first = name.split(',', 1)
    return f"{first.strip()} {last.strip()}"

def normalize_individual_df(df, year, event_name, conference, level_name, level_input):
    if df.empty:
        return df
    col_map = {
        'Contestant': 'student_name',
        'School': 'school_name',
        'Place': 'placement',
        'Score': 'score',
        'Points': 'points',
        'Advance': 'advancement_status'
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

    # Apply UIL-specific name normalization
    if 'student_name' in df.columns:
        df['student_name'] = df['student_name'].astype(str).apply(normalize_name)

    for col in ['school_name', 'advancement_status']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

def normalize_team_df(df, year, event_name, conference, level_name, level_input):
    if df.empty:
        return df
    col_map = {
        'Place': 'placement',
        'Score': 'score',
        'Points': 'points',
        'Advance': 'advancement_status',
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

def scrape_uil_archives(year, event, conference, level, level_input):
    url = build_url(year, event, conference, level, level_input)
    print(f"Fetching URL: {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "lxml")

    raw_individual_df = scrape_individual_table(soup)
    raw_team_df = scrape_team_table(soup, event == "Science")

    individual_df = normalize_individual_df(raw_individual_df, year, event, conference, level, level_input)
    team_df = normalize_team_df(raw_team_df, year, event, conference, level, level_input)

    # Add a 'district' column if level is district (zero-padded two digits)
    individual_df = individual_df.copy()
    if level.lower() == "district":
        individual_df["district"] = str(level_input).zfill(2)
    else:
        individual_df["district"] = None

    # Generate codes for individual results
    if not individual_df.empty:
        def make_code(row):
            if row["level_name"].strip().lower() == "district":
                # For district level: district-conference-unique_number (e.g. 07-5A-03)
                # Find all rows with same district and conference to assign sequence number
                subset = individual_df[
                    (individual_df["level_name"].str.lower() == "district") &
                    (individual_df["district"] == row["district"]) &
                    (individual_df["conference"].astype(str) == str(row["conference"]))
                ]
                seq_num = subset.index.get_loc(row.name) + 1
                return f"{row['district']}-{row['conference']}A-{str(seq_num).zfill(2)}"
            else:
                # For non-district: conference-unique_number (e.g. 4A-02)
                subset = individual_df[
                    individual_df["conference"].astype(str) == str(row["conference"])
                ]
                seq_num = subset.index.get_loc(row.name) + 1
                return f"{row['conference']}A-{str(seq_num).zfill(2)}"

        individual_df["code"] = individual_df.apply(make_code, axis=1)

    print("Individual Results Columns:", individual_df.columns)
    print(individual_df.head())
    print("Team Results Columns:", team_df.columns)
    print(team_df.head())

    return individual_df, team_df

