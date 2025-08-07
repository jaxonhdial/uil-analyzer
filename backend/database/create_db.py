import sqlite3
import os

def create_database(db_path="backend/database/uil_archives.db"):
    """
    Creates the UIL Archives database with proper schema and populates lookup tables.
    
    Args:
        db_path: Path to the SQLite database file
    """

    schema_path = "backend/database/schema.sql"
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        cursor.executescript(schema_sql)
        
        # Populate lookup tables with predefined data
        populate_lookup_tables(cursor)
        
        conn.commit()
        print(f"✅ Database '{db_path}' created successfully!")
        print("✅ Schema applied with INTEGER columns for scores and placements")
        print("✅ Lookup tables populated")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creating database: {e}")
        raise
    finally:
        conn.close()

def populate_lookup_tables(cursor):
    """Populate lookup tables with predefined data."""
    
    # Events data
    events_data = [
        # (-3, "Journalism team results"),
        # (-2, "Speech team results"),
        # (-1, "Overall school sweepstakes"),
        (1, "Accounting"),
        (2, "Computer Applications"),
        (3, "Current Issues and Events"),
        (4, "Literary Criticism"),
        (5, "Ready Writing"),
        (6, "Social Studies"),
        (7, "Spelling"),
        (8, "Calculator Applications"),
        (9, "Computer Science"),
        (10, "Mathematics"),
        (11, "Number Sense"),
        (12, "Science"),
        (13, "Copy Editing"),
        (14, "Editorial"),
        (15, "Feature Writing"),
        (16, "Headline Writing"),
        (17, "News Writing"),
        (18, "Informative Speaking"),
        (19, "Persuasive Speaking"),
        (20, "Lincoln Douglas Debate"),
        (21, "Poetry Interpretation"),
        (22, "Prose Interpretation")
    ]
    
    # Advancement status data
    advancement_status_data = [
        (1, "Region"),
        (2, "State"),
        (3, "Alternate"),
        (4, "")  # Empty string for no advancement
    ]
    
    # Levels data
    levels_data = [
        (1, "district"),
        (2, "region"),
        (3, "state")
    ]
    
    # Insert data using INSERT OR IGNORE to prevent duplicates
    cursor.executemany("INSERT OR IGNORE INTO events (id, name) VALUES (?, ?)", events_data)
    cursor.executemany("INSERT OR IGNORE INTO advancement_status (id, name) VALUES (?, ?)", advancement_status_data)
    cursor.executemany("INSERT OR IGNORE INTO levels (id, name) VALUES (?, ?)", levels_data)
    
    print("✅ Lookup tables populated")

# def recreate_database(db_path="backend/database/uil_archives.db"):
def recreate_database(db_path="testing/test.db"):
    """
    Completely recreate the database from scratch.
    WARNING: This will delete all existing data!
    """
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️  Deleted existing database: {db_path}")
    
    create_database(db_path)

if __name__ == "__main__":
    # Choose one of the following:
    
    # Option 1: Create database (won't overwrite existing)
    # create_database()
    
    # Option 2: Completely recreate database (DELETES ALL DATA!)
    recreate_database()