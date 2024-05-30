import requests
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
                price = first_result.find('div', {'class': 'discount_final_price'}).text.strip()
                if not price:
                    price = first_result.find('div', {'class': 'game_purchase_price price'}).text.strip()
                return self.get_game_details(appid, price)
            except Exception as e:
                print(f"Error scraping game card: {e}")
        return None

    def get_game_details(self, appid, price):
        game_url = f"{self.base_url}/app/{appid}/"
        response = requests.get(game_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            name = soup.find('div', {'class': 'apphub_AppName'}).text.strip()
            image_url = soup.find('img', {'class': 'game_header_image_full'})['src']
            review_summary = self.get_all_reviews_summary(soup)

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
            reviews = soup.find_all('div', {'class': 'user_reviews_summary_row'})
            for review in reviews:
                if 'All Reviews' in review.text:
                    all_reviews_summary = review.find('span', {'class': 'game_review_summary'}).text.strip()
                    return all_reviews_summary
            return 'No reviews'
        except Exception as e:
            print(f"Error scraping all reviews summary: {e}")
            return 'No reviews'