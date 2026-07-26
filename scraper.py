import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import csv

BASE_URL = "https://mdcomputers.in/"


def search_products(search_term):
    url = f"{BASE_URL}?route=product/search&search={quote(search_term)}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/125.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    # Update selectors if the website changes
    product_cards = soup.select(".product-layout")

    for card in product_cards:

        name = ""
        product_url = ""
        price = ""
        availability = ""
        image = ""

        title = card.select_one(".caption h4 a")
        if title:
            name = title.get_text(strip=True)
            product_url = urljoin(BASE_URL, title.get("href", ""))

        price_tag = card.select_one(".price")
        if price_tag:
            price = " ".join(price_tag.stripped_strings)

        img = card.select_one("img")
        if img:
            image = urljoin(BASE_URL, img.get("src", ""))

        availability_tag = card.select_one(".stock, .availability")
        if availability_tag:
            availability = availability_tag.get_text(strip=True)

        products.append({
            "name": name,
            "price": price,
            "availability": availability,
            "url": product_url,
            "image": image,
        })

    return products


def save_csv(products, filename="mdcomputers_products.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "price",
                "availability",
                "url",
                "image"
            ]
        )
        writer.writeheader()
        writer.writerows(products)


if __name__ == "__main__":
    query = "external harddrive"

    products = search_products(query)

    print(f"Found {len(products)} products\n")

    for p in products:
        print("=" * 60)
        print("Name:", p["name"])
        print("Price:", p["price"])
        print("Availability:", p["availability"])
        print("URL:", p["url"])
        print("Image:", p["image"])

    save_csv(products)
    print("\nSaved to mdcomputers_products.csv")