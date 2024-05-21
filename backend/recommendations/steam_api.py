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
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', {'class': 'search_result_row'})
        if first_result:
            appid = first_result['data-ds-appid']
            return self.scrape_similar_games(appid)
        return []

    def scrape_similar_games_by_name(self, game_name):
        search_url = f"{self.base_url}/search/?term={game_name}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', {'class': 'search_result_row'})
        if first_result:
            appid = first_result['data-ds-appid']
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
        search_url = f"{self.base_url}/search/?term={genre}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        game_divs = soup.find_all('a', {'class': 'search_result_row'})[:5]  # 상위 5개의 게임만 가져옴
        top_games = []
        for game_div in game_divs:
            try:
                appid = game_div['data-ds-appid']
                name = game_div.find('span', {'class': 'title'}).text.strip()
                review_summary_element = game_div.find('span', {'class': 'search_review_summary'})
                review_summary = 'No reviews'
                if review_summary_element:
                    review_summary = review_summary_element['data-tooltip-html'].split('<br>')[0]
                image_url = game_div.find('img')['src']
                top_games.append({'appid': appid, 'name': name, 'review_summary': review_summary, 'image_url': image_url})
            except Exception as e:
                print(f"Error scraping game card: {e}")
        return top_games
