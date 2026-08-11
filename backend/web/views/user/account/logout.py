from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.views.user.account.cookies import delete_refresh_cookie


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({'result': 'success'})
        return delete_refresh_cookie(response)
