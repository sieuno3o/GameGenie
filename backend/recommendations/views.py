import logging
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .steam_api import SteamAPI
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from GameGenie import config
from .models import Favorite
from .serializers import FavoriteSerializer
import re

# Logger 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = OpenAI(api_key=config.OPENAI_API_KEY)

# Steam 클라이언트 설정
steam_client = SteamAPI()


class GameViewSet(viewsets.ViewSet):
    system_instructions = """
    당신은 사용자들이 Steam에서 유사한 게임을 찾도록 돕는 유용한 도우미입니다.
    사용자가 게임 추천을 요청하면 사용자의 입력을 분석하고 Steam 데이터를 기반으로 최대 5개의 추천 게임 목록을 제공합니다.
    추천하는 게임은 반드시 Steam에서 사용할 수 있는 게임이어야 하며 확장팩이나 DLC는 추천해주지 않습니다.
    게임 추천 목록은 반드시 다음과 같은 형식으로 제공하세요:
    1. 게임 이름
    2. 게임 이름
    3. 게임 이름
    4. 게임 이름
    5. 게임 이름
    """

    conversation_history = [
        {"role": "system", "content": system_instructions}
    ]

    def list(self, request):
        user_input = request.query_params.get('user_input')
        if not user_input:
            return Response({"error": "No user input provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 검색어 유효성 검사
        if not self.is_valid_search_query(user_input):
            return Response({"error": "Invalid search query"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.conversation_history.append({"role": "user", "content": user_input})
            logger.info(f"User input: {user_input}")

            response = client.chat.completions.create(
                model="gpt-4",
                messages=self.conversation_history,
                max_tokens=500
            )
            ai_response = response.choices[0].message.content.strip()
            logger.info(f"AI response: {ai_response}")

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

            if not similar_games_info:
                return Response({"error": "유사한 게임을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"similar_games": similar_games_info})
        except Exception as e:
            logger.error(f"Error in list method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_game_names(self, recommendations):
        game_names = []
        try:
            for line in recommendations.split('\n'):
                line = line.strip()
                if line and line[0].isdigit() and '.' in line:
                    parts = line.split('. ')
                    if len(parts) > 1:
                        game_name = parts[1].strip().split('**')[0]  # 불필요한 텍스트 제거
                        if game_name:
                            game_names.append(game_name)
        except Exception as e:
            logger.error(f"Error in extract_game_names method: {e}")
        return game_names

    def is_valid_search_query(self, query):
        if re.match(r'^[^a-zA-Z0-9가-힣]+$', query):
            return False
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
