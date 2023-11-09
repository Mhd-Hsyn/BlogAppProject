from django.urls import path, include
from .views import *
from rest_framework import routers

user_router = routers.DefaultRouter()
user_router.register(r"userauth", UserAuthViewset, basename= "auth")
user_router.register(r"userapi", UserApi, basename= "auth")


urlpatterns = [

]

urlpatterns += user_router.urls