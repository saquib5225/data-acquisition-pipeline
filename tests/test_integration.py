import sys
import os

# Allow importing from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run_pipeline import run_pipeline

def test_run_pipeline():
    df = run_pipeline()
    
    # Pipeline should return a DataFrame with at least 10 rows
    assert df is not None
    assert len(df) >= 10

    # Check important columns exist
    assert "tournament" not in df.columns  # raw columns exist before rename
    assert len(df.columns) >= 5
