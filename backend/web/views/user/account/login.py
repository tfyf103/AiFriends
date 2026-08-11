from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile
from web.views.user.account.cookies import set_refresh_cookie


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = (request.data.get('username') or '').strip()
        password = (request.data.get('password') or '').strip()

        if not username or not password:
            return Response({'result': '用户名和密码不能为空'}, status=400)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'result': '用户名或密码错误'}, status=401)

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
