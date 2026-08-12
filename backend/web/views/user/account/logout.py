from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from web.views.user.account.cookies import REFRESH_COOKIE_NAME, delete_refresh_cookie


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Deleting a browser cookie is not token revocation: a copied refresh token
        # would otherwise remain usable until expiry. Blacklist it when available.
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                # Logout remains idempotent even when the cookie is expired,
                # malformed, or was already blacklisted during rotation.
                pass

        response = Response({'result': 'success'})
        return delete_refresh_cookie(response)
