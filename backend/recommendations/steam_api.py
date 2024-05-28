import requests
import json
from bs4 import BeautifulSoup

class SteamAPI:
    def __init__(self):
        self.base_url = "https://store.steampowered.com"

    def get_top_search_result(self, game_name):
        search_url = f"{self.base_url}/search/?term={game_name}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', {'class': 'search_result_row'})
        
        if first_result:
            try:
                appid = first_result['data-ds-appid']
                name = first_result.find('span', {'class': 'title'}).text.strip()
                review_summary_element = first_result.find('span', {'class': 'search_review_summary'})
                review_summary = 'No reviews'
                if review_summary_element:
                    review_summary = review_summary_element['data-tooltip-html'].split('<br>')[0]
                image_url = first_result.find('img')['src']
                price_element = first_result.find('div', {'class': 'col search_price responsive_secondrow'})
                price = price_element.text.strip() if price_element else 'No price'
                
                return {
                    'appid': appid,
                    'name': name,
                    'review_summary': review_summary,
                    'price': price,
                    'image_url': image_url,
                    'store_url': f"{self.base_url}/app/{appid}/"
                }
            except Exception as e:
                print(f"Error scraping game card: {e}")
        return None
