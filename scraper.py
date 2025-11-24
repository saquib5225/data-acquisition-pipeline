import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

URL_CURRENT = "https://en.wikipedia.org/wiki/Counter-Strike_Major_Championships"
PRIZE_CSV = "prize_pools.csv"


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten MultiIndex → normal strings."""
    new_cols = []
    for col in df.columns:
        if isinstance(col, tuple):
            parts = [str(x) for x in col if x and str(x) != "nan"]
            new_cols.append(" ".join(parts))
        else:
            new_cols.append(str(col))
    df.columns = [c.strip() for c in new_cols]
    return df


def _scrape_main_table(html: str) -> pd.DataFrame:
    """Scrape the CURRENT Wikipedia Majors table."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"class": "wikitable"})

    if table is None:
        raise RuntimeError("Could not find main wikitable.")

    df = pd.read_html(str(table))[0]
    df = _flatten_columns(df)

    # Normalize column names
    rename_map = {}
    for col in df.columns:
        low = col.lower()
        if "tournament" in low:
            rename_map[col] = "Tournament"
        elif "date" in low:
            rename_map[col] = "Date"
        elif "organizer" in low:
            rename_map[col] = "Organizer"
        elif "host city" in low or "city" in low:
            rename_map[col] = "Location"
        elif "winners" in low or "winner" in low:
            rename_map[col] = "Winner"
        elif "runners-up" in low or "runner" in low:
            rename_map[col] = "Runner-up"
        elif "finals result" in low or "result" in low:
            rename_map[col] = "Finals Result"

    df = df.rename(columns=rename_map)

    keep_cols = [
        "Tournament", "Date", "Organizer",
        "Location", "Winner", "Runner-up", "Finals Result"
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]
    return df[keep_cols]


def scrape_csgo_majors():
    """Scrapes Majors + merges Prize Pool from CSV."""

    # 1) Scrape current Wikipedia table
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL_CURRENT, headers=headers)
    resp.raise_for_status()

    main_df = _scrape_main_table(resp.text)

    # 2) Load prize pools from CSV
    prize_df = pd.read_csv(PRIZE_CSV)

    # Ensure correct naming
    prize_df["Tournament"] = prize_df["Tournament"].astype(str).str.strip()
    prize_df["Prize Pool"] = prize_df["Prize Pool"].astype(float)

    # 3) Merge datasets
    merged = main_df.merge(prize_df, on="Tournament", how="left")

    # Missing values → 0.0 prize pool
    merged["Prize Pool"] = merged["Prize Pool"].fillna(0.0)

    return merged


if __name__ == "__main__":
    df = scrape_csgo_majors()
    print(df.head())
    print(df.columns)
