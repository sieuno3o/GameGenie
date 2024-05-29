from rest_framework import viewsets, status
from rest_framework.response import Response
from .steam_api import SteamAPI
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from GameGenie import config

client = OpenAI(
    api_key=config.OPENAI_API_KEY,
)

# Steam 클라이언트 설정
steam_client = SteamAPI()


class GameViewSet(viewsets.ViewSet):
    # 대화를 위한 초기 시스템 메시지 설정
    system_instructions = """
    당신은 사용자들이 Steam에서 유사한 게임을 찾도록 돕는 유용한 도우미입니다.
    사용자가 게임 추천을 요청하면 사용자의 입력을 분석하고 Steam 데이터를 기반으로 최대 5개의 추천 게임 목록을 제공합니다.
    게임 추천 목록은 다음과 같은 형식으로 제공하세요:
    1. 게임 이름
    2. 게임 이름
    3. 게임 이름
    4. 게임 이름
    5. 게임 이름
    """

    # 대화 기록을 저장할 변수
    conversation_history = [
        {"role": "system", "content": system_instructions}
    ]

    def list(self, request):
        user_input = request.query_params.get('user_input')

        print(f"받은 사용자 입력: {user_input}")

        if not user_input:
            return Response({"error": "No user input provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 사용자 메시지를 대화 기록에 추가
            self.conversation_history.append({"role": "user", "content": user_input})

            # AI에게 사용자 입력을 이해하도록 요청
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=500  # 토큰 수를 늘림
            )

            print('OpenAI 응답:', response)

            ai_response = response.choices[0].message.content.strip()
            print(f"AI 응답: {ai_response}")

            # AI 응답을 대화 기록에 추가
            self.conversation_history.append({"role": "assistant", "content": ai_response})

            # 추천 게임 목록에서 게임 이름 추출
            game_names = self.extract_game_names(ai_response)
            if not game_names:
                return Response({"error": "추천 목록에서 게임 이름을 추출할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 병렬 처리로 추천 게임 목록을 스팀에서 검색하여 첫 번째 결과 가져오기
            similar_games_info = []
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(steam_client.get_top_search_result, game_name)
                            for game_name in game_names[:5]]
                for future in as_completed(futures):
                    game = future.result()
                    if game:
                        similar_games_info.append(game)
                    else:
                        print(f"게임 정보를 가져오는 데 실패했습니다")

            if not similar_games_info:
                return Response({"error": "유사한 게임을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"similar_games": similar_games_info})
        except Exception as e:
            print(f"list 메서드에서 에러 발생: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_game_names(self, recommendations):
        game_names = []
        try:
            # 줄바꿈으로 분리된 게임 이름 추출
            for line in recommendations.split('\n'):
                line = line.strip()
                if line and any(char.isdigit() for char in line):
                    # 게임 이름 추출
                    parts = line.split('. ')
                    if len(parts) > 1:
                        game_name = parts[1].strip()
                        if game_name:
                            game_names.append(game_name)
        except Exception as e:
            print(f"extract_game_names 메서드에서 에러 발생: {e}")
        return game_names
