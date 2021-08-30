from django.urls import path,include

from .views import *
app_name="core"

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path("login/",Login,name="login"),
    path("sign_up/",Sign_Up,name="sign_up"),
    path("logout/",Logout,name="logout"),
    path("user_setting/",UserSetting,name="user_setting")
]
