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

client = OpenAI(api_key=config.OPENAI_API_KEY)

steam_client = SteamAPI()


class GameViewSet(viewsets.ViewSet):
    system_instructions = """
    You are a helpful assistant that helps users find similar games on Steam.
    When a user requests game recommendations, analyze the user's input and provide a list of up to 5 recommended games based on Steam data.
    The recommended games must be available on Steam and should not include expansions or DLCs.
    The game recommendation list should be provided in the following format:
    1. Game name
    2. Game name
    3. Game name
    4. Game name
    5. Game name
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_history = [{"role": "system", "content": self.system_instructions}]

    def list(self, request):
        user_input = request.query_params.get('user_input')
        if not user_input:
            return Response({"error": "No user input provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.is_valid_search_query(user_input):
            return Response({"error": "Invalid search query"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.conversation_history.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=self.conversation_history,
                max_tokens=500
            )
            ai_response = response.choices[0].message['content'].strip()
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            game_names = self.extract_game_names(ai_response)

            if not game_names:
                return Response({"error": "Unable to extract game names from the recommendation list."}, status=status.HTTP_400_BAD_REQUEST)

            similar_games_info = []
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(steam_client.get_top_search_result, game_name)
                           for game_name in game_names[:5]]
                for future in as_completed(futures):
                    game = future.result()
                    if game:
                        similar_games_info.append(game)

            if not similar_games_info:
                return Response({"error": "Could not find similar games."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"similar_games": similar_games_info})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_game_names(self, recommendations):
        game_names = []
        try:
            for line in recommendations.split('\n'):
                line = line.strip()
                if line and line[0].isdigit() and '.' in line:
                    parts = line.split('. ')
                    if len(parts) > 1:
                        game_name = parts[1].strip().split('**')[0]
                        if game_name:
                            game_names.append(game_name)
        except Exception as e:
            print(f"Error in extract_game_names method: {e}")
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
            return Response({'message': 'Already added to favorites.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)


class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        favorite = Favorite.objects.filter(user=request.user, pk=pk).first()
        if not favorite:
            return Response({'message': 'Favorite item not found.'}, status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
