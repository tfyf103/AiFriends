from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile
from web.views.user.account.cookies import set_refresh_cookie


class RegisterView(APIView):
    def post(self, request):
        username = (request.data.get('username') or '').strip()
        password = (request.data.get('password') or '').strip()

        if not username or not password:
            return Response({'result': '用户名或密码不能为空'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'result': '用户名已存在'}, status=409)

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
