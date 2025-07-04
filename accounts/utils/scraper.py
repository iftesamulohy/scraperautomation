import cloudscraper
from bs4 import BeautifulSoup
from accounts.models import ScrapedItem

def scrape_fbi_seeking_info():
    url = "https://www.fbi.gov/wanted/seeking-info"

    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container holding all wanted persons/items
    grid = soup.find('ul', class_='wanted-grid-natural')
    if not grid:
        print("Grid not found on the page")
        return

    # Find all individual wanted person blocks
    items = grid.find_all('li', class_='portal-type-person')
    if not items:
        print("No wanted items found")
        return

    for item in items:
        # Extract name and details link
        name_tag = item.find('h3', class_='title')
        if name_tag:
            a_tag = name_tag.find('a')
            name = a_tag.text.strip() if a_tag else ''
            link = a_tag['href'] if a_tag and a_tag.has_attr('href') else ''
        else:
            name = ''
            link = ''

        # Extract image url supporting lazy loading
        img_tag = item.find('img')
        image = ''
        if img_tag:
            image = img_tag.get('data-src') or img_tag.get('data-original') or img_tag.get('src') or ''

        # Print extracted info (for debug)
        print(f"Name: {name}\nLink: {link}\nImage: {image}\n{'-'*40}")

        # Save to database if all fields exist
        if name and link and image:
            ScrapedItem.objects.get_or_create(
                name=name,
                details_link=link,
                image=image
            )
