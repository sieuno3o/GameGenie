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
                return self.get_game_details(appid)
            except Exception as e:
                print(f"Error scraping game card: {e}")
        return None

    def get_game_details(self, appid):
        game_url = f"{self.base_url}/app/{appid}/"
        response = requests.get(game_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            name = soup.find('div', {'class': 'apphub_AppName'}).text.strip()
            image_url = soup.find('img', {'class': 'game_header_image_full'})['src']
            review_summary = soup.find('span', {'class': 'game_review_summary'}).text.strip()
            price_element = soup.find('div', {'class': 'game_purchase_price price'})
            if not price_element:
                price_element = soup.find('div', {'class': 'discount_final_price'})
            price = price_element.text.strip() if price_element else 'No price'

            return {
                'appid': appid,
                'name': name,
                'review_summary': review_summary,
                'price': price,
                'image_url': image_url,
                'store_url': game_url
            }
        except Exception as e:
            print(f"Error scraping game details: {e}")
        return None
