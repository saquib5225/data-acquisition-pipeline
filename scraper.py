import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://en.wikipedia.org/wiki/Counter-Strike_Major_Championships"

def scrape_csgo_majors():
    """
    Scrapes the CS:GO Major Championships table from Wikipedia
    and returns a cleaned pandas DataFrame.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    # first wikitable
    table = soup.find("table", {"class": "wikitable"})

    # Parse to df
    df = pd.read_html(str(table))[0]

    new_cols = []
    for col in df.columns:
        if isinstance(col, tuple):
            # Join tuple parts into one string
            new_cols.append(" ".join([str(x) for x in col if x]))
        else:
            new_cols.append(col)

    df.columns = new_cols

    df.columns = [c.strip() for c in df.columns]

    return df


if __name__ == "__main__":
    df = scrape_csgo_majors()
    print(df.head())


