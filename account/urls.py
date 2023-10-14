from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from . import api
from . import views

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('editprofile/', api.edit_profile, name='edit_profile'),
    path('editpassword/', api.edit_password, name='edit_password'),
    path('get-users/', api.get_users, name='get_users'),
    path('<uuid:id>/follow/', api.follow, name='follow'),
    path('<uuid:id>/get-follows/', api.get_follows, name='get_follows'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]