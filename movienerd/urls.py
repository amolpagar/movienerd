"""movienerd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as authenication_views
from movie import views as movie_views
from users import views as user_views

urlpatterns = [
      # Admin management URL
    path('admin/', admin.site.urls),        

     # Authentication Related URLs
    path('login/', authenication_views.LoginView.as_view(template_name='users/login.html'), name="loginurl"), 
    path('logout/', user_views.logout_view, name="logout"),
    path('register/', user_views.register, name="register"),
 
    path('<str:username>/', movie_views.searchmovie, name='index'), # This page is used to search movies and recommend, only visitble to logged in user
    path('<str:username>/searchmovie/', movie_views.searchmovie, name='searchmovies'), # This page is used to search movies and recommend, only visitble to logged in user


    path('<str:username>/subscribe/', movie_views.subscribe, name='subscribe'), # POST:: This button on myrecommendations page will subscribe user with recommendations
    path('<str:username>/mysubscriptions/', movie_views.mysubscriptions, name='mysubscriptions'), # GET:: This page will load all recommendations from other subscribed users
    path('<str:username>/mysubscribers/', movie_views.mysubscribers, name='mysubscribers'), # GET:: This page will load all recommendations from other subscribed users
    path('unsubscribe/<int:userid>/', movie_views.unsubscribe, name='unsubscribe'), # GET:: This page will load all recommendations from other subscribed users

    # URLs for Recommendations
    path('<str:username>/myrecommendations/', movie_views.myrecommendations, name='myrecommendations'), # GET:: This page is used to display all recommendations of users
    path('recommendation/add/', movie_views.recommend, name='addrecommendation'), # POST:: This button is used to recommend searched movies only visitble to logged in user
    path('recommendation/delete/<int:movieid>/', movie_views.deleterecommendation, name='deleterecommendation'),# DELETE :: Delete recommendation from users recommendation list

    # URLs for watchlist
    path('<str:username>/watchlist/', movie_views.watchlist, name='watchlist'), # GET:: This page will load all watchlist items for a user
    path('watchlist/add/', movie_views.addtowatchlist, name='addtowatchlist'), # POST:: method to add/update watchlist
    path('watchlist/delete/<int:movieid>/', movie_views.deletefromwatchlist, name='deletefromwatchlist') # DELETE:: method to delete movie from watchlist

]
