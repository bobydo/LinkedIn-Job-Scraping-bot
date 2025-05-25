from LinkedinScraping import LinkedinScraper
import datetime

def build_linkedin_url(role, location):
    geo_ids = {
        "Canada": "101174742",
        "United States": "103644278"
    }
    base_url = "https://ca.linkedin.com/jobs/search?keywords={role}&location={location}&locationId=&geoId={geo_id}&f_TPR=r86400&position=1&pageNum=0"
    return base_url.format(
        role=role.replace(' ', '%20'),
        location=location.replace(' ', '%20'),
        geo_id=geo_ids.get(location, "")
    )

if __name__ == "__main__":
    # Download url https://googlechromelabs.github.io/chrome-for-testing/#stable
    chrome_driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv_path = f"output_{now_str}.csv"

    role = "Data Analyst"
    locations = ["Canada", "United States"]

    for location in locations:
        linkedin_url = build_linkedin_url(role, location)
        scraper = LinkedinScraper(
            chrome_driver_path=chrome_driver_path,
            output_csv_path=output_csv_path
        )
        scraper.run(linkedin_url)
