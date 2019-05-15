"""MovieSizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import xadmin
from django.urls import path
from django.conf.urls import url
from operation.views import IndexView, refresh, calDefault8Recommendations , reCal_spark ,reCal_normal
from user.views import LoginView, LogoutView
from movies.views import ContentView,AddComment
from user.views import RegisterView
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 首页
    path('', IndexView.as_view(), name='index'),
    path('index.html/', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('content/', ContentView.as_view(), name="content",),
    path('register/', RegisterView.as_view(), name="register",),
    path('movieinfo/<int:movie_id>', ContentView.as_view(), name='movieinfo'),
    path('add_comment/', AddComment.as_view(), name='addcomments'),
    
    #weisg
    path('index.html/~', refresh, name='refresh'),
    #path('content.html/~', refresh2, name='refresh2')
    #path('index.html/~', calDefault8Recommendations, name = 'refresh')
    # xgm
    path('base.html/~', reCal_spark, name='reCal_spark'),
    path('index.html/~', reCal_normal, name='reCal_normal'),

]
