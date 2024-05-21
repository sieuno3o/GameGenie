from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from .steam_api import SteamAPI
from openai import OpenAI
from GameGenie import config

client = OpenAI(
    api_key=config.OPENAI_API_KEY,
)

# Steam 클라이언트 설정
steam_client = SteamAPI()

class GameViewSet(viewsets.ViewSet):
    genre_mapping = {
        'sports': 'Sports',
        'sports game': 'Sports',
        'football game': 'Football',
        'soccer game': 'Football',
        'soccer games': 'Football',
        'soccer': 'Football',
        'action': 'Action',
        'action game': 'Action',
        'adventure': 'Adventure',
        'adventure game': 'Adventure',
        'rpg': 'RPG',
        'role-playing game': 'RPG',
        'strategy': 'Strategy',
        'strategy game': 'Strategy',
        'simulation': 'Simulation',
        'simulation game': 'Simulation',
        'puzzle': 'Puzzle',
        'puzzle game': 'Puzzle',
        'racing': 'Racing',
        'racing game': 'Racing',
        'casual': 'Casual',
        'casual game': 'Casual',
        'roguelike': 'Roguelike',  # 추가된 매핑
        # 필요에 따라 추가 장르 매핑
    }

    abbreviation_mapping = {
        '레데리': '레드 데드 리뎀션',
        '포나': '포트나이트',
        '라오어': '라스트 오브 어스',
        # 추가적인 줄임말 매핑
    }

    def list(self, request):
        user_input = request.query_params.get('user_input')
        print(f"받은 사용자 입력: {user_input}")

        if user_input:
            try:
                # 줄임말을 원래 이름으로 변환
                for abbreviation, full_name in self.abbreviation_mapping.items():
                    if abbreviation in user_input:
                        user_input = user_input.replace(abbreviation, full_name)
                print(f"변환된 사용자 입력: {user_input}")

                # 사용자 입력에서 게임 이름 또는 장르 추출
                extracted_info, info_type = self.extract_game_name_or_genre(user_input)
                print(f"추출된 정보: {extracted_info}, 타입: {info_type}")

                if not extracted_info:
                    return Response({"error": "Game name or genre not found in user input"}, status=status.HTTP_400_BAD_REQUEST)

                if info_type == 'genre':
                    # 추출된 장르를 매핑
                    mapped_genre = self.genre_mapping.get(extracted_info.lower(), extracted_info.capitalize())
                    print(f"매핑된 장르: {mapped_genre}")

                    # 장르 기반 상위 게임 스크래핑
                    top_games = steam_client.scrape_top_games_by_genre(mapped_genre)
                    if top_games:
                        return Response({"similar_games": top_games})
                    else:
                        return Response({"error": f"No top games found for the genre {mapped_genre}"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    # 스팀에서 게임 정보 및 비슷한 게임 검색
                    similar_games_info = steam_client.scrape_similar_games_by_name(extracted_info)
                    if not similar_games_info:
                        return Response({"error": "No similar games found"}, status=status.HTTP_404_NOT_FOUND)
                
                    return Response({"similar_games": similar_games_info})
            except Exception as e:
                print(f"list 메서드에서 에러 발생: {e}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response([])

    def extract_game_name_or_genre(self, query):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that identifies if the user input is a game name or a genre. If it is a genre, return only the genre name in English. If it is a game name, return only the name in English."},
                    {"role": "user", "content": f"Identify if the following query is a game name or a genre: '{query}'"}
                ],
                max_tokens=50
            )

            print('OpenAI 응답:', response)

            extracted_info = response.choices[0].message.content.strip()
            if 'genre' in extracted_info:
                genre = extracted_info.split('genre')[-1].strip().replace('.', '').replace('"', '').split(':')[-1].strip()
                mapped_genre = self.genre_mapping.get(genre.lower(), genre.capitalize())
                return mapped_genre, 'genre'
            else:
                name = extracted_info.split('game name')[-1].strip().replace('.', '').replace('"', '').split(':')[-1].strip()
                return name, 'name'
        except Exception as e:
            print(f"extract_game_name_or_genre 메서드에서 에러 발생: {e}")
            return None, None
