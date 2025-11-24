from flask import Flask, render_template
import sqlite3
import os

DB_NAME = "csgo_majors.db"

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    """
    Homepage: show summary, table of majors, and yearly prize chart.
    """
    conn = get_db_connection()

    # Fetch all tournaments
    majors = conn.execute("""
        SELECT rowid AS id, * FROM majors
        ORDER BY date
    """).fetchall()

    # Aggregate prize pool by year
    yearly = conn.execute("""
        SELECT substr(date, -4) AS year, SUM(prize_pool) AS total_prize
        FROM majors
        GROUP BY year
        ORDER BY year
    """).fetchall()

    conn.close()

    # Prepare cleaned values for Chart.js
    years = []
    prizes = []

    for row in yearly:
        year = row["year"]
        total = row["total_prize"]

        # Convert year to string
        if year is None:
            continue
        years.append(str(year))

        # Convert prize to float
        try:
            prizes.append(float(total))
        except:
            prizes.append(0.0)

    return render_template(
        "index.html",
        majors=majors,
        years=years,
        prizes=prizes
    )

if __name__ == "__main__":
    # Run Flask on port 8080 for easier GCP firewall setup
    app.run(host="0.0.0.0", port=8080, debug=True)
