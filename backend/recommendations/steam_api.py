import requests
import subprocess
import json
from bs4 import BeautifulSoup

class SteamAPI:
    def __init__(self):
        self.base_url = "https://store.steampowered.com"

    def get_game_details(self, appid):
        result = subprocess.run(['node', 'scrapesteam.js', 'details', str(appid)], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for game details of appid {appid}: {e}")
                print(f"Output was: {result.stdout}")
        return None

    def scrape_review_summary(self, appid):
        url = f"https://store.steampowered.com/app/{appid}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        review_summary = soup.find('span', {'class': 'game_review_summary'})
        return review_summary.text if review_summary else 'No reviews'

    def search_game(self, game_name):
        search_url = f"{self.base_url}/search/?term={game_name}"
        print(f"Search URL: {search_url}")  # 검색 URL 출력
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', {'class': 'search_result_row'})
        if first_result:
            appid = first_result['data-ds-appid']
            print(f"First result appid: {appid}")  # 첫 번째 결과 appid 출력
            return self.scrape_similar_games(appid)
        return []

    def scrape_similar_games_by_name(self, game_name):
        search_url = f"{self.base_url}/search/?term={game_name}"
        print(f"Search URL: {search_url}")  # 검색 URL 출력
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', {'class': 'search_result_row'})
        if first_result:
            appid = first_result['data-ds-appid']
            print(f"First result appid: {appid}")  # 첫 번째 결과 appid 출력
            return self.scrape_similar_games(appid)
        return []

    def scrape_similar_games(self, appid):
        result = subprocess.run(['node', 'scrapesteam.js', 'similar', str(appid)], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for similar games of appid {appid}: {e}")
                print(f"Output was: {result.stdout}")
        return []

    def scrape_top_games_by_genre(self, genre):
        try:
            search_url = f"{self.base_url}/search/?term={genre}"
            print(f"Search URL: {search_url}")  # 검색 URL 출력
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            game_divs = soup.find_all('a', {'class': 'search_result_row'})[:5]  # 상위 5개의 게임만 가져옴
            top_games = []
            for game_div in game_divs:
                try:
                    appid = game_div.get('data-ds-appid')
                    if not appid:  # appid가 없으면 bundleid를 사용
                        appid = game_div.get('data-ds-bundleid')
                    if appid:
                        name = game_div.find('span', {'class': 'title'}).text.strip()
                        review_summary_element = game_div.find('span', {'class': 'search_review_summary'})
                        review_summary = 'No reviews'
                        if review_summary_element:
                            review_summary = review_summary_element['data-tooltip-html'].split('<br>')[0]
                        price_element = game_div.find('div', {'class': 'search_price'})
                        price = price_element.text.strip() if price_element else 'No price info'
                        image_url = game_div.find('img')['src']
                        top_games.append({
                            'appid': appid,
                            'name': name,
                            'review_summary': review_summary,
                            'price': price,
                            'image_url': image_url
                        })
                    else:
                        print(f"Neither appid nor bundleid found for game element: {game_div}")
                except KeyError as ke:
                    print(f"KeyError scraping game card: {ke}, element: {game_div}")
                except Exception as e:
                    print(f"Error scraping game card: {e}, element: {game_div}")
            return top_games
        except Exception as e:
            print(f"Error scraping games: {e}")
            return []

    def scrape_games_by_name_or_genre(self, name_or_genre):
        search_url = f"{self.base_url}/search/?term={name_or_genre}"
        print(f"Search URL: {search_url}")  # 검색 URL 출력
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        game_divs = soup.find_all('a', {'class': 'search_result_row'})[:5]  # 상위 5개의 게임만 가져옴
        games = []
        for game_div in game_divs:
            try:
                appid = game_div.get('data-ds-appid')
                if not appid:  # appid가 없으면 bundleid를 사용
                    appid = game_div.get('data-ds-bundleid')
                if appid:
                    name = game_div.find('span', {'class': 'title'}).text.strip()
                    review_summary_element = game_div.find('span', {'class': 'search_review_summary'})
                    review_summary = 'No reviews'
                    if review_summary_element:
                        review_summary = review_summary_element['data-tooltip-html'].split('<br>')[0]
                    price_element = game_div.find('div', {'class': 'search_price'})
                    price = price_element.text.strip() if price_element else 'No price info'
                    image_url = game_div.find('img')['src']
                    games.append({
                        'appid': appid,
                        'name': name,
                        'review_summary': review_summary,
                        'price': price,
                        'image_url': image_url
                    })
                else:
                    print(f"Neither appid nor bundleid found for game element: {game_div}")
            except KeyError as ke:
                print(f"KeyError scraping game card: {ke}, element: {game_div}")
            except Exception as e:
                print(f"Error scraping game card: {e}, element: {game_div}")
        return games
