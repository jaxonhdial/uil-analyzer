import sqlite3
import pandas as pd
from pathlib import Path

from backend.constants.db_path import DB_PATH

def get_contest_results(
    year: int,
    conference: int,
    event: str,
    level: str,           # "district", "region", "state"
    level_input: int,
    is_team: bool
) -> pd.DataFrame:
    """
    Query UIL contest results by resolving contest_id through the normalized contests table,
    then replace IDs with human-readable names/text and add contest metadata columns,
    including mapping student names and their schools, and team school names.

    Parameters:
        year (int)
        conference (int)
        event (str)
        level (str): 'district', 'region', 'state'
        level_input (int)
        is_team (bool): True for team_results, False for individual_results

    Returns:
        pd.DataFrame: Results with readable student names, advancement statuses, school names, and contest info.
    """
    results_table = "team_results" if is_team else "individual_results"

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get event_id from event name
        cursor.execute("SELECT id FROM events WHERE name = ?", (event,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"Event not found: '{event}'")
        event_id = row[0]

        # Get level_id from level name
        cursor.execute("SELECT id FROM levels WHERE name = ?", (level,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"Level not found: '{level}'")
        level_id = row[0]

        # Get contest_id from contests table
        cursor.execute("""
            SELECT id FROM contests
            WHERE year = ?
              AND conference = ?
              AND event_id = ?
              AND level_id = ?
              AND level_input = ?
        """, (year, conference, event_id, level_id, level_input))

        row = cursor.fetchone()
        if row is None:
            raise ValueError("No contest matches the provided filters.")
        contest_id = row[0]

        # Query the raw results table using contest_id
        df = pd.read_sql_query(
            f"SELECT * FROM {results_table} WHERE contest_id = ?",
            conn,
            params=[contest_id]
        )

        if df.empty:
            # If no results, return empty df immediately
            return df

        # Load students with school_id
        students_df = pd.read_sql_query("SELECT id, name, school_id FROM students", conn)

        # Load schools
        schools_df = pd.read_sql_query("SELECT id, name FROM schools", conn)
        school_id_to_name = dict(zip(schools_df.id, schools_df.name))

        # Load advancement status
        adv_status_df = pd.read_sql_query("SELECT id, name FROM advancement_status", conn)
        adv_status_id_to_text = dict(zip(adv_status_df.id, adv_status_df.name))

        # Load contests info
        contests_df = pd.read_sql_query("""
            SELECT c.id AS contest_id, c.year, c.level_input, c.conference,
                   l.name AS level, e.name AS event
            FROM contests c
            JOIN levels l ON c.level_id = l.id
            JOIN events e ON c.event_id = e.id
            WHERE c.id = ?
        """, conn, params=[contest_id])

        # Create helper dicts
        student_id_to_name = dict(zip(students_df.id, students_df.name))
        student_name_to_school_id = dict(zip(students_df.name, students_df.school_id))

        # Replace advancement_status_id with text if present
        if 'advancement_status_id' in df.columns:
            df['advancement_status'] = df['advancement_status_id'].map(adv_status_id_to_text).fillna("")

        # Replace student IDs with names and map schools
        if is_team:
            for col_id in ['student_1_id', 'student_2_id', 'student_3_id', 'student_4_id']:
                if col_id in df.columns:
                    df[col_id.replace('_id', '')] = df[col_id].map(student_id_to_name).fillna("")
            # Drop original *_id columns
            df.drop(columns=[col for col in ['student_1_id', 'student_2_id', 'student_3_id', 'student_4_id'] if col in df.columns], inplace=True)

            # Map team school_id to school_name
            if 'school_id' in df.columns:
                df['school_name'] = df['school_id'].map(school_id_to_name).fillna("")
                df.drop(columns=['school_id'], inplace=True)

        else:
            if 'student_id' in df.columns:
                df['student_name'] = df['student_id'].map(student_id_to_name).fillna("")
                df.drop(columns=['student_id'], inplace=True)

            # Map individual student_name to school_name
            if 'student_name' in df.columns:
                df['school_name'] = df['student_name'].map(student_name_to_school_id).map(school_id_to_name).fillna("")

        # Add contest metadata columns
        if not contests_df.empty:
            contest_info = contests_df.iloc[0]
            for col in ['year', 'level', 'level_input', 'conference', 'event']:
                df[col] = contest_info[col]

        # Drop replaced advancement_status_id column
        if 'advancement_status_id' in df.columns:
            df.drop(columns=['advancement_status_id'], inplace=True)

        # Drop 'id' and 'contest_id' columns if present
        cols_to_drop = [col for col in ['id', 'contest_id'] if col in df.columns]

        # Drop columns that have all null (NaN) values
        null_columns = df.columns[df.isnull().all()].tolist()

        df.drop(columns=cols_to_drop + null_columns, inplace=True)

        return df

    except Exception as e:
        raise RuntimeError(f"Query failed: {e}")
    finally:
        conn.close()
