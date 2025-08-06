import sqlite3
def create_db():
    with open("backend/database/schema.sql", "r") as f:
        schema_sql = f.read()
    
    conn = sqlite3.connect("backend/database/uil_archives.db")
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database created successfully")

if __name__ == "__main__":
    create_db()