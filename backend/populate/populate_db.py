import sqlite3
import pandas as pd

from backend.constants.db_path import DB_PATH

# Connect to SQLite DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# -------------------------
# Note: Lookup tables are initialized when the database is created
# using create_database.py - no need to initialize them here
# -------------------------

# -------------------------
# Caches for lookup tables
# -------------------------
school_cache = {}
event_cache = {}
level_cache = {}
status_cache = {}

# -------------------------
# Lookup + Insert Helpers
# -------------------------

def get_or_create_id(table, name, cache):
    """Lookup or insert and cache a name in a lookup table."""
    if name in cache:
        return cache[name]
    cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        cache[name] = row[0]
    else:
        cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
        conn.commit()
        cache[name] = cursor.lastrowid
    return cache[name]

def get_or_create_school_id(name):
    return get_or_create_id("schools", name, school_cache)

def get_or_create_event_id(name):
    return get_or_create_id("events", name, event_cache)

def get_or_create_level_id(name):
    return get_or_create_id("levels", name, level_cache)

def get_or_create_status_id(name):
    return get_or_create_id("advancement_status", name, status_cache)

def get_or_create_student_id(name, school_id):
    cursor.execute("SELECT id FROM students WHERE name = ? AND school_id = ?", (name, school_id))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("INSERT INTO students (name, school_id) VALUES (?, ?)", (name, school_id))
    conn.commit()
    return cursor.lastrowid

def get_or_create_contest_id(year, level_id, level_input, conference, event_id):
    cursor.execute("""
        SELECT id FROM contests
        WHERE year = ? AND level_id = ? AND level_input = ? AND conference = ? AND event_id = ?
    """, (year, level_id, level_input, conference, event_id))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("""
        INSERT INTO contests (year, level_id, level_input, conference, event_id)
        VALUES (?, ?, ?, ?, ?)
    """, (year, level_id, level_input, conference, event_id))
    conn.commit()
    return cursor.lastrowid

# -------------------------
# Helper Functions for Integer Conversion
# -------------------------

def safe_int_convert(value):
    """Convert a value to integer, return None if conversion fails."""
    if pd.isna(value) or value == "" or value is None:
        return None
    try:
        # Handle string values that might have decimal points
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return int(float(value))  # Convert to float first to handle "123.0" strings
    except (ValueError, TypeError):
        return None

def convert_placement_to_int(placement_str):
    """
    Converts placement strings like '1st', '2nd', '3rd' to integers
    
    Args:
        placement_str: String representation of placement (e.g., '1st', '2nd', '3rd')
    
    Returns:
        int: Integer value of placement, or None if conversion fails
    """
    if pd.isna(placement_str) or not placement_str or str(placement_str).strip() == "":
        return None
    
    # Convert to string and remove common suffixes and whitespace
    cleaned = str(placement_str).strip().lower()
    
    # Remove ordinal suffixes (st, nd, rd, th)
    if cleaned.endswith(('st', 'nd', 'rd', 'th')):
        cleaned = cleaned[:-2]
    
    # Try to convert to integer
    try:
        return int(cleaned)
    except ValueError:
        # Handle special cases like 'DNP' (Did Not Place), 'DQ' (Disqualified), etc.
        if cleaned in ['dnp', 'dq', 'ns', 'absent', 'no show']:
            return None  # or you could use a special code like 999
        return None

# -------------------------
# Insert Individual Results
# -------------------------

def insert_individual_results(df):
    conn.execute("BEGIN")
    try:
        for _, row in df.iterrows():
            # Get lookup table values
            school_id = get_or_create_school_id(row['school_name'])
            student_id = get_or_create_student_id(row['student_name'], school_id)
            event_id = get_or_create_event_id(row['event_name'])
            level_id = get_or_create_level_id(row['level_name'])
            adv_status_id = get_or_create_status_id(row['advancement_status'])
            contest_id = get_or_create_contest_id(
                row['year'], level_id, row['level_input'], row['conference'], event_id
            )

            # Convert score-related columns to integers
            placement = convert_placement_to_int(row.get('placement'))
            score = safe_int_convert(row.get('score'))
            tiebreaker = safe_int_convert(row.get('tiebreaker'))
            objective_score = safe_int_convert(row.get('objective_score'))
            essay_score = safe_int_convert(row.get('essay_score'))
            biology_score = safe_int_convert(row.get('biology_score'))
            chemistry_score = safe_int_convert(row.get('chemistry_score'))
            physics_score = safe_int_convert(row.get('physics_score'))
            points = safe_int_convert(row.get('points'))

            # Insert into individual_results
            cursor.execute("""
                INSERT INTO individual_results (
                    contest_id, student_id, code, placement, score, tiebreaker,
                    objective_score, essay_score, biology_score, chemistry_score,
                    physics_score, points, advancement_status_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contest_id,
                student_id,
                row.get('code'),
                placement,
                score,
                tiebreaker,
                objective_score,
                essay_score,
                biology_score,
                chemistry_score,
                physics_score,
                points,
                adv_status_id
            ))
        conn.commit()
        print(f"Successfully inserted {len(df)} individual results")
    except Exception as e:
        conn.rollback()
        print("Error inserting individual results:", e)
        raise

# -------------------------
# Insert Team Results
# -------------------------

def insert_team_results(df):
    conn.execute("BEGIN")
    try:
        for _, row in df.iterrows():
            # School + contest
            school_id = get_or_create_school_id(row['school_name'])
            event_id = get_or_create_event_id(row['event_name'])
            level_id = get_or_create_level_id(row['level_name'])
            adv_status_id = get_or_create_status_id(row['advancement_status'])
            contest_id = get_or_create_contest_id(
                row['year'], level_id, row['level_input'], row['conference'], event_id
            )

            # Student IDs (may be None)
            student_ids = []
            for i in range(1, 5):
                name_key = f"student_{i}_name"
                if pd.notna(row.get(name_key)) and row.get(name_key, "").strip():
                    student_ids.append(
                        get_or_create_student_id(row[name_key], school_id)
                    )
                else:
                    student_ids.append(None)

            # Convert score-related columns to integers
            placement = convert_placement_to_int(row.get('placement'))
            score = safe_int_convert(row.get('score'))
            programming_score = safe_int_convert(row.get('programming_score'))
            points = safe_int_convert(row.get('points'))

            # Insert into team_results
            cursor.execute("""
                INSERT INTO team_results (
                    contest_id, school_id, placement,
                    student_1_id, student_2_id, student_3_id, student_4_id,
                    score, programming_score, points, advancement_status_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contest_id,
                school_id,
                placement,
                student_ids[0],
                student_ids[1],
                student_ids[2],
                student_ids[3],
                score,
                programming_score,
                points,
                adv_status_id
            ))
        conn.commit()
        print(f"Successfully inserted {len(df)} team results")
    except Exception as e:
        conn.rollback()
        print("Error inserting team results:", e)
        raise

# -------------------------
# Usage Example
# -------------------------

if __name__ == "__main__":
    # Example usage - assumes database already exists with lookup tables populated
    print("Database insertion functions ready to use!")
    print("Make sure to run create_database.py first to set up the schema and lookup tables.")