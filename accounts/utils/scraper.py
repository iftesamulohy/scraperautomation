import cloudscraper
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from urllib.parse import urljoin
import os
import mimetypes

from accounts.models import ScrapedItem

def scrape_fbi_seeking_info():
    base_url = (
        "https://www.fbi.gov/wanted/seeking-info/@@castle.cms.querylisting/querylisting-1"
        "?display_type=wanted-grid"
        "&sort_on=getObjPositionInParent"
        "&missing_text=No+results+were+found."
        "&limit=40"
        "&query.i:records=path"
        "&query.o:records=plone.app.querystring.operation.string.relativePath"
        "&query.v:records=.%2F"
        "&query.i:records=portal_type"
        "&query.o:records=plone.app.querystring.operation.selection.any"
        "&query.v:records=%5Bu%27Person%27%5D"
        "&query.i:records=review_state"
        "&query.o:records=plone.app.querystring.operation.selection.any"
        "&query.v:records=%5Bu%27published%27%5D"
        "&display_fields=%28%27image%27%2C%29"
        "&page="
    )

    scraper = cloudscraper.create_scraper()
    page = 1
    total = 0

    while True:
        url = base_url + str(page)
        print(f"🔄 Scraping page {page}...")

        res = scraper.get(url)
        if res.status_code != 200:
            print(f"❌ Failed to fetch page {page}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("li", class_="portal-type-person")
        if not items:
            print("✅ No more data.")
            break

        for item in items:
            name_tag = item.find("h3", class_="title")
            a_tag = name_tag.find("a") if name_tag else None
            name = a_tag.text.strip() if a_tag else ""
            link = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""

            img_tag = item.find("img")
            image = img_tag.get("src") or img_tag.get("data-src") or "" if img_tag else ""

            if image and image.startswith("/"):
                image = urljoin("https://www.fbi.gov", image)

            if name and link and image:
                # Download image
                img_response = scraper.get(image)
                if img_response.status_code == 200:
                    # Determine the proper file extension
                    content_type, _ = mimetypes.guess_type(image)
                    if content_type:
                        extension = content_type.split("/")[1]
                    else:
                        extension = 'jpg'  # default to jpg if no extension found

                    image_name = os.path.basename(image.split("?")[0])  # clean image name
                    image_name_with_extension = f"{os.path.splitext(image_name)[0]}.{extension}"

                    scraped_item = ScrapedItem(
                        name=name,
                        details_link=link,
                        image=image
                    )
                    scraped_item.image_file.save(image_name_with_extension, ContentFile(img_response.content), save=True)
                    print(f"✔ Saved: {name}")
                    total += 1

        page += 1

    print(f"🎯 Total scraped: {total}")
