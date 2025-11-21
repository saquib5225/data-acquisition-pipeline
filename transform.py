import pandas as pd
import re

def clean_csgo_majors(df):
    """
    Cleans and transforms the CS:GO Majors DataFrame.
    """

    df = df.copy()

    # Remove reference numbers like [77]
    df = df.replace(r"\[\d+\]", "", regex=True)

    # Clean prize pool column (convert "$250,000" → 250000)
    if "Prize Pool" in df.columns:
        df["Prize Pool"] = (
            df["Prize Pool"]
            .replace(r"[$,]", "", regex=True)
            .astype(float)
        )

    # Fix date field: "January 1–3, 2020" → "January 1, 2020"
    if "Date" in df.columns:

        def fix_date(d):
            d = str(d)
            if "–" in d:
                # Split at the dash
                left, right = d.split("–", 1)

                left = left.strip()

                # Extract year from right side
                year = right.strip().split(",")[-1].strip()

                return f"{left}, {year}"

            return d

        df["Date"] = df["Date"].apply(fix_date)

    # Strip whitespace from all string columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

    return df


if __name__ == "__main__":
    from scraper import scrape_csgo_majors

    raw_df = scrape_csgo_majors()
    clean_df = clean_csgo_majors(raw_df)
    print(clean_df.head())
