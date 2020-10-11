from django.shortcuts import render
from django.contrib.auth.models import User
from movie.models import Recommendation, Movie, Subscription,Watch
from django.core.paginator import Paginator
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

 #http://www.omdbapi.com/?i=tt3896198&apikey=618ee319
# Create your views here.

def index(request, username):
    user = User.objects.filter(username=username).first()  
    if user:
        baseurl = 'http://www.omdbapi.com/'
    
        if 'moviename' in request.GET:
            baseurl = baseurl+ '?t=' +  request.GET['moviename']+'&apikey=618ee319'
            response = requests.get(baseurl)
            movies = response.json()
            print(movies)
            context = {"movies": movies}
            return render(request, "movie/searchmovies.html", context)
    else:
        return render(request, "movie/invalid-user.html")

    return render(request, "movie/searchmovies.html")

@login_required
def searchmovie(request, username):
    user = User.objects.filter(username=username).first()  
    if user:
        #baseurl = 'https://api.themoviedb.org/3/search/movie?api_key=61e8f206a9a1e964cc3d57e67e2c15e3&language=en-US&query=ssadak&page=1&include_adult=false"
        #https://api.themoviedb.org/3/search/movie?api_key=61e8f206a9a1e964cc3d57e67e2c15e3&language=en-US&query=ssadak&page=1&include_adult=false
        if 'moviename' in request.GET:            
            title = request.GET['moviename']
            baseurl = "https://api.themoviedb.org/3/search/movie?api_key=61e8f206a9a1e964cc3d57e67e2c15e3&language=en-US&query="+title+"&page=1&include_adult=false"
            response = requests.get(baseurl).json()
            total_movies = response['total_results']
            movies = response['results']          
            context = {"response": response, "title": title}

            return render(request, "movie/searchmovies.html", context)
    else:
        return render(request, "movie/invalid-user.html")

    return render(request, "movie/searchmovies.html")

@login_required
def recommend(request, username):
    context = {}
    return render(request, "movie/searchmovies.html", context)

@login_required
def subscribe(request, username):
    user = User.objects.get(username=username)
    if user:
        subscription = Subscription.objects.create(user=request.GET.user, subscribing_user_id=user.id)
        subscription.save()
        context = {}
        return redirect('mysubscriptions', username=request.GET.username)
    else:
        return render(request, "movie/invalid-user.html")


def myrecommendations(request, username):
    user = User.objects.get(username=username)
    movies = []
    if user:
        rd = Recommendation.objects.filter(user=user)
        if len(rd) > 0: 
            for rd_item in rd:
                movie = Movie.objects.get(id=rd_item.movie_id)
                movies.append(movie)
            
            context = {"movies": movies, "username": username}
        else:
            context = {"Error":"You havent recommended anything yet, recommend kar salya"}
        
        return render(request, "movie/myrecommendations.html", context)

    else:
        return render(request, "movie/invalid-user.html")    

@login_required
def mysubscriptions(request, username):
    searched_users = None
    if 'user_name' in request.GET:
        searched_users = User.objects.filter(username__contains=request.GET['user_name'])
        paginator = Paginator(searched_users, 3)
        page = request.GET.get('page')
        searched_users_page  = paginator.get_page(page)

    mysubscriptions = Subscription.objects.filter(user=request.user.id)
    subscribed_users = []
    for each_subscription in mysubscriptions:
        user = User.objects.get(id=each_subscription.subscribing_user_id)
        subscribed_users.append(user)

    context = {"searched_users":searched_users, "subscribed_users": subscribed_users}
    return render(request, "movie/mysubscriptions.html", context)

@login_required
def watchlist(request, username):
    movies = get_object_or_404(Watch, user=request.user.id)
    context = {"watchlist": movies.watchlist}
    return render(request, "movie/watchlist.html", context)