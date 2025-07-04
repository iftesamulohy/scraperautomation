import cloudscraper
from bs4 import BeautifulSoup

# URL
url = "https://www.fbi.gov/wanted/seeking-info"

# Create a scraper that bypasses Cloudflare
scraper = cloudscraper.create_scraper()

# Send request
response = scraper.get(url)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())  # Full rendered HTML
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
