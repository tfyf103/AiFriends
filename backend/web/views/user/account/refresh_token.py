from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from web.views.user.account.cookies import REFRESH_COOKIE_NAME, set_refresh_cookie


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not refresh_token:
            return Response({
                'result': 'refresh token不存在',
                'code': 'REFRESH_TOKEN_MISSING',
            }, status=401)

        # Use SimpleJWT's maintained serializer instead of mutating the token JTI
        # ourselves. With ROTATE_REFRESH_TOKENS + BLACKLIST_AFTER_ROTATION enabled,
        # this blacklists the credential that was just used and returns a new one.
        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response({
                'result': 'refresh token无效或已过期',
                'code': 'REFRESH_TOKEN_INVALID',
            }, status=401)

        data = serializer.validated_data
        response = Response({
            'result': 'success',
            'access': data['access'],
        })
        new_refresh = data.get('refresh')
        if new_refresh:
            return set_refresh_cookie(response, new_refresh)
        return response
