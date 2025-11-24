import pandas as pd
import re

def clean_csgo_majors(df):
    """
    Cleans and transforms the CS:GO Majors DataFrame.
    Ensures Prize Pool is numeric and fields are tidy.
    """

    df = df.copy()

    # 1) Remove Wikipedia [number] references from all string cells
    df = df.replace(r"\[\d+\]", "", regex=True)

    # 2) Clean Prize Pool column -> always float
    if "Prize Pool" in df.columns:

        def clean_prize(x):
            if x is None:
                return 0.0
            x = str(x).strip()
            x = x.replace("$", "").replace(",", "")

            if x == "" or x.lower() in ["nan", "none"]:
                return 0.0

            try:
                return float(x)
            except:
                return 0.0

        df["Prize Pool"] = df["Prize Pool"].apply(clean_prize)
    else:
        df["Prize Pool"] = 0.0

    # 3) Fix Date column: "January 1–3, 2020" -> "January 1, 2020"
    if "Date" in df.columns:

        def fix_date(d):
            d = str(d)
            if "–" in d:
                left, right = d.split("–", 1)
                left = left.strip()
                year = right.strip().split(",")[-1].strip()
                return f"{left}, {year}"
            return d

        df["Date"] = df["Date"].apply(fix_date)

    # 4) Strip whitespace from all string columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    return df


if __name__ == "__main__":
    from scraper import scrape_csgo_majors
    raw = scrape_csgo_majors()
    clean = clean_csgo_majors(raw)
    print(clean.head())
    print(clean.dtypes)
