from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile
from web.serializers.account import LoginSerializer, validation_response_data
from web.views.user.account.cookies import set_refresh_cookie


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(validation_response_data(serializer), status=400)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if not user:
            return Response({
                'result': '用户名或密码错误',
                'code': 'AUTH_INVALID_CREDENTIALS',
            }, status=401)

        user_profile = UserProfile.objects.get(user=user)
        refresh = RefreshToken.for_user(user)
        response = Response({
            'result': 'success',
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
            'photo': user_profile.photo.url,
            'profile': user_profile.profile,
        })
        return set_refresh_cookie(response, refresh)
