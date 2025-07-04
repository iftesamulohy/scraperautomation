import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from accounts.models import ScrapedItem

async def scrape_fbi_seeking_info_playwright():
    url = "https://www.fbi.gov/wanted/seeking-info"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless browser
        page = await browser.new_page()
        await page.goto(url)
        # Wait for the grid to load
        await page.wait_for_selector('ul.wanted-grid-natural')

        # Scroll to bottom to trigger lazy loading if any
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3)  # wait for lazy loaded images/content

        content = await page.content()
        await browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    grid = soup.find('ul', class_='wanted-grid-natural')
    if not grid:
        print("Grid not found")
        return

    items = grid.find_all('li', class_='portal-type-person')
    if not items:
        print("No wanted items found")
        return

    for item in items:
        name_tag = item.find('h3', class_='title')
        if name_tag:
            a_tag = name_tag.find('a')
            name = a_tag.text.strip() if a_tag else ''
            link = a_tag['href'] if a_tag and a_tag.has_attr('href') else ''
        else:
            name = ''
            link = ''

        img_tag = item.find('img')
        image = ''
        if img_tag:
            image = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-original') or ''

        print(f"Name: {name}\nLink: {link}\nImage: {image}\n{'-'*40}")

        if name and link and image:
            ScrapedItem.objects.get_or_create(
                name=name,
                details_link=link,
                image=image
            )

# Run the async function
asyncio.run(scrape_fbi_seeking_info_playwright())
