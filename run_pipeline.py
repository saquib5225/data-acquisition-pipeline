from scraper import scrape_csgo_majors
from transform import clean_csgo_majors
from load import init_db, load_data


def run_pipeline():
    print("🔵 Starting CS:GO Major Championships pipeline...")

    # 1. Scrape data
    print("📥 Scraping data from Wikipedia...")
    raw_df = scrape_csgo_majors()
    print(f"   ✔ Scraped {len(raw_df)} rows")

    # 2. Transform data
    print("🔧 Cleaning and transforming data...")
    clean_df = clean_csgo_majors(raw_df)
    print(f"   ✔ Cleaned {len(clean_df)} rows")

    # 3. Load into database
    print("💾 Initializing database...")
    init_db()

    print("⬆️ Loading data into SQLite database...")
    load_data(clean_df)

    print("🎉 Pipeline completed successfully!")
    return clean_df


if __name__ == "__main__":
    run_pipeline()
