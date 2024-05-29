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
            review_summary = self.get_all_reviews_summary(soup)
            price = self.extract_price(soup)

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

    def get_all_reviews_summary(self, soup):
        try:
            # 'All Reviews'가 있는 div를 정확히 찾아서 텍스트를 추출
            reviews = soup.find_all('div', {'class': 'user_reviews_summary_row'})
            for review in reviews:
                if 'All Reviews' in review.text:
                    all_reviews_summary = review.find('span', {'class': 'game_review_summary'}).text.strip()
                    return all_reviews_summary
            return 'No reviews'
        except Exception as e:
            print(f"Error scraping all reviews summary: {e}")
            return 'No reviews'

    def extract_price(self, soup):
        # 가격 요소를 찾아서 추출
        price_element = soup.find('div', {'class': 'game_purchase_price price'})
        if not price_element:
            price_element = soup.find('div', {'class': 'discount_final_price'})

        if price_element:
            price = price_element.text.strip()
            if "무료 데모" not in price and "FREE" not in price.upper():
                return price

        # 여러 버전의 게임 가격을 포함하는 경우를 처리
        prices = soup.find_all('div', {'class': 'game_area_purchase_game_wrapper'})
        for price_div in prices:
            if price_div.find('h1', text=lambda x: x and "DEMO" not in x.upper()):
                price = price_div.find('div', {'class': 'game_purchase_price price'})
                if not price:
                    price = price_div.find('div', {'class': 'discount_final_price'})

                if price:
                    return price.text.strip()

        return 'No price'
