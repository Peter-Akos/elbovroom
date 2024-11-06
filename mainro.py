import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import re


def scrape_autovit(max_page):
    base_url = "https://www.autovit.ro/autoturisme/second"
    params = {"search[order]": "filter_float_price:asc"}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    data = []

    for page in range(1, max_page + 1):
        if page == 1:
            url = f"{base_url}?{requests.compat.urlencode(params)}"
        else:
            params["page"] = page
            url = f"{base_url}?{requests.compat.urlencode(params)}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            items = soup.find_all('article')
            for item in items:
                title = item.find('h1', class_='epwfahw9').text.strip() if item.find('h1', class_='epwfahw9') else "N/A"

                details_div = item.find('dl', class_='ooa-1uwk9ii epwfahw11')
                year = "N/A"
                km = "N/A"
                fuel_type = "N/A"

                if details_div:
                    details_text = details_div.text.strip()
                    # Extract year, km, and fuel type from details_text
                    year_match = re.search(r'\b(\d{4})\b', details_text)
                    year = year_match.group(1) if year_match else "N/A"

                    km_match = re.search(r'(\d+(?:\s*\d+)*)\s*km', details_text, re.IGNORECASE)
                    km = km_match.group(1).replace(" ", "") if km_match else "N/A"

                    fuel_types = ['Benzină', 'Diesel', 'Electric', 'Hibrid']
                    for fuel in fuel_types:
                        if fuel in details_text:
                            fuel_type = fuel
                            break

                power = item.find('p', class_='epwfahw10').text.strip() if item.find('p', class_='epwfahw10') else "N/A"
                price = item.find('div', class_='ooa-2p9dfw').text.strip() if item.find('div',
                                                                                        class_='ooa-2p9dfw') else "N/A"
                link = item.find('h1', class_='epwfahw9').find('a')['href'] if item.find('h1',
                                                                                         class_='epwfahw9') and item.find(
                    'h1', class_='epwfahw9').find('a') else "N/A"

                if title != "N/A" and price != "N/A":  # Only add non-empty entries
                    data.append([title, year, km, power, fuel_type, price, link])

            print(f"Scraped page {page}")

            if page % 5 == 0:
                save_to_csv(data, f"autovit_data_page_{page}.csv")
                data = []
            time.sleep(2)

        except requests.RequestException as e:
            print(f"An error occurred while scraping page {page}: {e}")

    if data:
        save_to_csv(data, f"autovit_data_final.csv")

    print("Scraping completed")


def save_to_csv(data, filename):
    headers = ['Title', 'Year', 'Km', 'Power', 'Fuel Type', 'Price', 'Link']

    os.makedirs('data', exist_ok=True)

    filepath = os.path.join('data', filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Data saved to {filepath}")


# Run the scraper
scrape_autovit(1230)