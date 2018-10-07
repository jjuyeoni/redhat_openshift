from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('mypage', views.mypage, name='mypage'),
    path('cancer/<num>', views.cancer, name='cancer'),
]
