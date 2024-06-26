import re
from rest_framework.response import Response
from accounts.serializers import UserSerializer, UserProfileSerializer
from accounts.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView


import logging

logger = logging.getLogger(__name__)

class CreateView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # 이메일 형식 검증
                    return Response({'message': '올바른 이메일 형식이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

                password = serializer.validated_data.get('password')
                if not password:
                    return Response({'message': '비밀번호를 입력해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

                if User.objects.filter(email=email).exists():  # 이메일 중복 확인
                    return Response({'message': '중복된 email입니다.'}, status=status.HTTP_400_BAD_REQUEST)

                nickname = serializer.validated_data.get('nickname')
                if User.objects.filter(nickname=nickname).exists():
                    return Response({'message': '중복된 닉네임입니다.'}, status=status.HTTP_400_BAD_REQUEST)

                user = serializer.save()
                user.set_password(password)
                if 'profile_image' in request.FILES:
                    user.profile_image = request.FILES['profile_image']
                user.save()
                return Response({"message": "저장되었습니다", "userId": user.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error during user creation: {str(e)}')
            return Response({'message': '서버 오류가 발생했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LogoutView(APIView):

    def post(self, request):
        token = request.data.get('refresh')
        if token:
            try:
                token_obj = RefreshToken(token)
                token_obj.blacklist()
                return Response({'message': '성공적으로 로그아웃 되었습니다.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': '유효하지 않은 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '유효하지 않은 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        password = request.data.get('password')

        if not password:
            return Response({'message': '비밀번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            if id:
                user = get_object_or_404(User, id=id)
            else:
                user = request.user
            serializer = UserProfileSerializer(user)
            data = serializer.data
            data['is_superuser'] = user.is_superuser  # 슈퍼유저 정보 추가
            return Response(data)
        except Exception as e:
            print(f"Error: {e}")  # 예외 메시지를 로그로 출력
            return Response({'message': '프로필을 불러오는 중 오류가 발생했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id=None):
        user = request.user
        serializer = UserProfileSerializer(
            user, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            email = request.data.get('email')
            if email and email != user.email:
                if User.objects.filter(email=email).exclude(id=user.id).exists():
                    return Response({'message': '이미 사용 중인 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            if old_password and new_password:
                if not user.check_password(old_password):
                    return Response({'message': '예전 password와 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
                if new_password == old_password:
                    return Response({'message': '동일한 password입니다.'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(new_password)
            user.save()
            serializer.save()
            return Response({'message': '프로필이 업데이트 되었습니다.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
