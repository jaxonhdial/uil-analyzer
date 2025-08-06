import sqlite3
import pandas as pd

# Connects to Database
conn = sqlite3.connect("testing/test.db")
cursor = conn.cursor()

# Caches for Lookup Tables
school_cache = {}
event_cache = {}
level_cache = {}
status_cache = {}

# Generic Helper: Get or Create ID with Cache
def get_or_create_id(table, name, cache):
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

# --- Insert School ---
def get_or_create_school_id(school_name):
    return get_or_create_id("schools", school_name, school_cache)

# --- Insert Event ---
def get_or_create_event_id(event_name):
    return get_or_create_id("events", event_name, event_cache)

# --- Insert Level ---
def get_or_create_level_id(level_name):
    return get_or_create_id("levels", level_name, level_cache)

# --- Insert Advancement Status ---
def get_or_create_status_id(status_name):
    return get_or_create_id("advancement_status", status_name, status_cache)

# --- Insert Student ---
def get_or_create_student_id(student_name, school_id):
    cursor.execute("""
        SELECT id FROM students WHERE name = ? AND school_id = ?
    """, (student_name, school_id))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("""
        INSERT INTO students (name, school_id) VALUES (?, ?)
    """, (student_name, school_id))
    conn.commit()
    return cursor.lastrowid

# --- Insert Contest ---
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

# --- Insert Individual Results from DataFrame ---
def insert_individual_results(df):
    conn.execute("BEGIN")
    try:
        for _, row in df.iterrows():
            # Lookup or insert all related IDs
            school_id = get_or_create_school_id(row['school_name'])
            student_id = get_or_create_student_id(row['student_name'], school_id)
            event_id = get_or_create_event_id(row['event_name'])
            level_id = get_or_create_level_id(row['level_name'])
            adv_status_id = get_or_create_status_id(row['advancement_status'])
            contest_id = get_or_create_contest_id(
                row['year'], level_id, row['level_input'], row['conference'], event_id
            )

            # Insert into individual_results
            cursor.execute("""
                INSERT INTO individual_results (
                    contest_id, student_id, code, placement, score, points, advancement_status_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                contest_id,
                student_id,
                row['code'],
                row['placement'],
                row['score'],
                row['points'],
                adv_status_id
            ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error inserting individual results:", e)
        raise

# --- Insert Team Results from DataFrame
def insert_team_results(df):
    conn.execute("BEGIN")
    try:
        for _, row in df.iterrows():
            # Get or create lookup IDs
            school_id = get_or_create_school_id(row['school_name'])
            event_id = get_or_create_event_id(row['event_name'])
            level_id = get_or_create_level_id(row['level_name'])
            adv_status_id = get_or_create_status_id(row['advancement_status'])
            contest_id = get_or_create_contest_id(
                row['year'], level_id, row['level_input'], row['conference'], event_id
            )

            # Resolve up to 4 team members student IDs, handle missing names gracefully
            student_ids = []
            for i in range(1, 5):
                student_key = f'student_{i}_name'
                student_name = row.get(student_key)
                if student_name and pd.notna(student_name):
                    student_id = get_or_create_student_id(student_name, school_id)
                    student_ids.append(student_id)
                else:
                    student_ids.append(None)

            # Insert into team_results
            cursor.execute("""
                INSERT INTO team_results (
                    contest_id,
                    school_id,
                    placement,
                    student_1_id,
                    student_2_id,
                    student_3_id,
                    student_4_id,
                    score,
                    programming_score,
                    points,
                    advancement_status_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contest_id,
                school_id,
                row.get('placement'),
                student_ids[0],
                student_ids[1],
                student_ids[2],
                student_ids[3],
                row.get('score'),
                row.get('programming_score'),
                row.get('points'),
                adv_status_id
            ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error inserting team results:", e)
        raise

# --- Close the connection when done (optional, can be left to caller) ---
def close_connection():
    conn.close()