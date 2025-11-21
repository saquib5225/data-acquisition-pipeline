import sys
import os

# Fix import path so tests can find project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from transform import clean_csgo_majors

def test_clean_csgo_majors():
    data = {
        "Tournament": ["Test Major"],
        "Date": ["January 1–3, 2020"],
        "Location": ["Test City [1]"],
        "Prize Pool": ["$250,000"],
        "Winner": ["Team A [12]"],
        "Runner-up": ["Team B [99]"]
    }

    df = pd.DataFrame(data)
    clean = clean_csgo_majors(df)

    assert "Test City" in clean["Location"].iloc[0]
    assert "[" not in clean["Winner"].iloc[0]
    assert clean["Prize Pool"].iloc[0] == 250000.0
    assert clean["Date"].iloc[0] == "January 1, 2020"

