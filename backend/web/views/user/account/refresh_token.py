from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from web.views.user.account.cookies import REFRESH_COOKIE_NAME, set_refresh_cookie


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not refresh_token:
            return Response({'result': 'refresh token不存在'}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            return Response({'result': 'refresh token过期了'}, status=401)

        # Rotate the refresh token so a long-running browser session does not keep
        # reusing the exact same credential forever.
        refresh.set_jti()
        response = Response({
            'result': 'success',
            'access': str(refresh.access_token),
        })
        return set_refresh_cookie(response, refresh)
