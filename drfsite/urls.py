"""
URL configuration for drfsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from blog_app.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='main_home'),
    path('posts/', PostView.as_view(), name='posts'),
    path('get_cryptocurrency_prices/', cryptocurrency_prices, name='get_cryptocurrency_prices'),

    # все что связано с аутентификацией
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html')
         , name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # только представление регистрации мы создаем сами наследуясь от формы UserCreationForm
    # остальное и так уже имеет свое собственное представление в auth

    # подключение системы аутентификации
    path('', include('django.contrib.auth.urls')),

    # admin
    path('admin/', admin.site.urls),

    # все что связано с API
    path('api/v1/post_list/', BlogAPIView.as_view()),
    path('api/v1/post_list/<int:pk>/', BlogAPIView.as_view()),
]
