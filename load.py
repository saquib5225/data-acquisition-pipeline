import sqlite3

DB_NAME = "csgo_majors.db"

def init_db():
    """
    Creates the SQLite database and table if they do not exist yet.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS majors (
            tournament TEXT,
            date TEXT,
            organizer TEXT,
            location TEXT,
            prize_pool REAL,
            winner TEXT,
            runner_up TEXT,
            finals_result TEXT
        )
    """)

    conn.commit()
    conn.close()


def load_data(clean_df):
    """
    Loads the cleaned DataFrame into the SQLite database.
    Ensures prize_pool is always stored as float.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ensure column presence
    for required in ["Tournament", "Date", "Organizer", "Location", "Prize Pool", "Winner", "Runner-up", "Finals Result"]:
        if required not in clean_df.columns:
            clean_df[required] = "" if required != "Prize Pool" else 0.0

    # Enforce float type for Prize Pool
    clean_df["Prize Pool"] = clean_df["Prize Pool"].astype(float)

    for _, row in clean_df.iterrows():
        cursor.execute(
            """
            INSERT INTO majors (tournament, date, organizer, location, prize_pool, winner, runner_up, finals_result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["Tournament"],
                row["Date"],
                row["Organizer"],
                row["Location"],
                row["Prize Pool"],
                row["Winner"],
                row["Runner-up"],
                row["Finals Result"]
            )
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized. Run run_pipeline.py to load data.")
