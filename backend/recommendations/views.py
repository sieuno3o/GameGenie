from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView  # 추가된 부분
from .steam_api import SteamAPI
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from GameGenie import config
from .models import Favorite
from .serializers import FavoriteSerializer
import re

client = OpenAI(api_key=config.OPENAI_API_KEY)

# Steam 클라이언트 설정
steam_client = SteamAPI()


class GameViewSet(viewsets.ViewSet):
    system_instructions = """
    당신은 사용자들이 Steam에서 유사한 게임을 찾도록 돕는 유용한 도우미입니다.
    사용자가 게임 추천을 요청하면 사용자의 입력을 분석하고 Steam 데이터를 기반으로 최대 5개의 추천 게임 목록을 제공합니다.
    추천하는 게임은 반드시 Steam에서 사용할 수 있는 게임이어야 하며 확장팩이나 DLC는 추천해주지 않습니다.
    만약 사용자가 의미 없는 단어나 문자만 입력하여 추천해줄 수 없다면 추천해주지 말아주세요.
    게임 추천 목록은 다음과 같은 형식으로 제공하세요:
    1. "게임 이름"
    2. "게임 이름"
    3. "게임 이름"
    4. "게임 이름"
    5. "게임 이름"
    """

    conversation_history = [
        {"role": "system", "content": system_instructions}
    ]

    def list(self, request):
        user_input = request.query_params.get('user_input')
        print(f"받은 사용자 입력: {user_input}")

        if not user_input:
            return Response({"error": "No user input provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 검색어 유효성 검사
        if not self.is_valid_search_query(user_input):
            return Response({"error": "Invalid search query"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.conversation_history.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=self.conversation_history,
                max_tokens=500
            )

            print('OpenAI 응답:', response)
            ai_response = response.choices[0].message.content.strip()
            print(f"AI 응답: {ai_response}")

            self.conversation_history.append({"role": "assistant", "content": ai_response})

            game_names = self.extract_game_names(ai_response)
            if not game_names:
                return Response({"error": "추천 목록에서 게임 이름을 추출할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

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
            for line in recommendations.split('\n'):
                line = line.strip()
                if line and any(char.isdigit() for char in line):
                    parts = line.split('. ')
                    if len(parts) > 1:
                        game_name = parts[1].strip()
                        if game_name:
                            game_names.append(game_name)
        except Exception as e:
            print(f"extract_game_names 메서드에서 에러 발생: {e}")
        return game_names

    def is_valid_search_query(self, query):
        """
        검색어의 유효성을 검사합니다.
        """
        # 의미 없는 검색어 필터링 (특수 문자만 포함된 경우 등)
        if re.match(r'^[^a-zA-Z0-9가-힣]+$', query):
            return False

        # 최소 길이 조건
        if len(query) < 1:
            return False

        return True


class FavoriteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            game_name=data.get('game_name'),
            defaults={
                'game_image': data.get('game_image'),
                'game_review': data.get('game_review'),
                'game_price': data.get('game_price'),
                'game_url': data.get('game_url')
            }
        )
        if not created:
            return Response({'message': '이미 즐겨찾기에 추가되어 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)


class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        favorite = Favorite.objects.filter(user=request.user, pk=pk).first()
        if not favorite:
            return Response({'message': '즐겨찾기 항목을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
