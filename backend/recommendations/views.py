from rest_framework import viewsets, status
from rest_framework.response import Response
from .steam_api import SteamAPI
from openai import OpenAI
from GameGenie import config

client = OpenAI(
    api_key=config.OPENAI_API_KEY,
)

# Steam 클라이언트 설정
steam_client = SteamAPI()

class GameViewSet(viewsets.ViewSet):
    def list(self, request):
        user_input = request.query_params.get('user_input')

        print(f"받은 사용자 입력: {user_input}")

        if not user_input:
            return Response({"error": "No user input provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # AI에게 사용자 입력을 이해하도록 요청
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                        {"role": "system", "content": "당신은 사용자들이 Steam에서 유사한 게임을 찾도록 돕는 유용한 도우미입니다. 사용자가 게임 추천을 요청하면 사용자의 입력을 분석하고 Steam 데이터를 기반으로 최대 5개의 추천 게임 목록을 제공합니다."},
                        {"role": "user", "content": f"다음 사용자 입력을 기반으로 최대 5개의 게임을 추천해줘: '{user_input}'"}
                ],
                max_tokens=500  # 토큰 수를 늘림
            )

            print('OpenAI 응답:', response)

            ai_response = response.choices[0].message.content.strip()
            print(f"AI 응답: {ai_response}")

            # 추천 게임 목록에서 게임 이름 추출
            game_names = self.extract_game_names(ai_response)
            if not game_names:
                return Response({"error": "추천 목록에서 게임 이름을 추출할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 추천 게임 목록을 스팀에서 검색하여 첫 번째 결과 가져오기
            similar_games_info = []
            for game_name in game_names[:5]:  # 최대 5개의 게임만 가져옴
                game = steam_client.get_top_search_result(game_name)
                if game:
                    similar_games_info.append(game)
                else:
                    print(f"게임 정보를 가져오는 데 실패했습니다: {game_name}")

            if not similar_games_info:
                return Response({"error": "유사한 게임을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"similar_games": similar_games_info})
        except Exception as e:
            print(f"list 메서드에서 에러 발생: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_game_names(self, recommendations):
        game_names = []
        try:
            # 줄바꿈 또는 숫자 목록으로 분리된 게임 이름 추출
            for line in recommendations.split('\n'):
                if line.strip() and any(char.isdigit() for char in line):
                    # 게임 이름 추출
                    game_name = line.split('**')[1].strip()
                    if game_name:
                        game_names.append(game_name)
        except Exception as e:
            print(f"extract_game_names 메서드에서 에러 발생: {e}")
        return game_names
