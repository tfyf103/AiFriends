from django.urls import path, re_path
from web.views.index import index
from web.views.user.account.get_user_info import GetUserInfo
from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.register import RegisterView
from web.views.user.profile.update import UpdateProfileView

urlpatterns = [
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    path('api/user/account/get_user_info/', GetUserInfo.as_view()),
    path('api/user/profile/update/', UpdateProfileView.as_view()),
    path('',index),
    re_path(r'^(?!media/|static/|assets/).*$', index),
]
