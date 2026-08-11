from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile
from web.serializers.account import RegisterSerializer, validation_response_data
from web.views.user.account.cookies import set_refresh_cookie


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(validation_response_data(serializer), status=400)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            return Response({
                'result': '用户名已存在',
                'code': 'USERNAME_EXISTS',
            }, status=409)

        user = User.objects.create_user(username=username, password=password)
        user_profile = UserProfile.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        response = Response({
            'result': 'success',
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
            'photo': user_profile.photo.url,
            'profile': user_profile.profile,
        }, status=201)
        return set_refresh_cookie(response, refresh)
