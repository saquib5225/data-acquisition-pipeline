import sqlite3
import pandas as pd

DB_NAME = "csgo_majors.db"

def init_db():
    """
    Creates the database and table if it doesn't exist.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS majors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament TEXT,
            date TEXT,
            location TEXT,
            prize_pool REAL,
            winner TEXT,
            runner_up TEXT
        );
    """)

    conn.commit()
    conn.close()


def load_data(df):
    """
    Loads a cleaned DataFrame into the SQLite database.
    """

    conn = sqlite3.connect(DB_NAME)
    
    # Only keep relevant columns (rename to DB schema)
    df = df.rename(columns={
        df.columns[0]: "tournament",
        df.columns[1]: "date",
        df.columns[2]: "location",
        df.columns[3]: "prize_pool",
        df.columns[4]: "winner",
        df.columns[5]: "runner_up"
    })

    df_to_insert = df[["tournament", "date", "location", "prize_pool", "winner", "runner_up"]]

    df_to_insert.to_sql("majors", conn, if_exists="append", index=False)

    conn.close()


# For testing purposes
if __name__ == "__main__":
    from scraper import scrape_csgo_majors
    from transform import clean_csgo_majors

    raw = scrape_csgo_majors()
    clean = clean_csgo_majors(raw)

    init_db()
    load_data(clean)

    print("Database loaded successfully.")
