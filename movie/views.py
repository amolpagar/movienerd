from django.shortcuts import render
from django.contrib.auth.models import User
from movie.models import Recommendation, Movie, Subscription,Watch
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
        baseurl = 'http://www.omdbapi.com/'
    
        if 'moviename' in request.GET:
            baseurl = baseurl+ '?t=' +  request.GET['moviename']+'&apikey=618ee319'
            response = requests.get(baseurl)
            movies = response.json()
            print(movies)
            if movies['Response'] == 'False':
                context = {"Error": movies['Error'],"title":request.GET['moviename'] }
            else:
                context = {"movies": movies}
            
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
    context = {}
    return render(request, "movie/myrecommendations.html", context)

@login_required
def myrecommendations(request, username):
    user = User.objects.get(username=username)
    movies = []
    if user:
        rd = Recommendation.objects.filter(user=user)
        if len(rd) > 0: 
            for rd_item in rd:
                movie = Movie.objects.get(id=rd_item.movie_id)
                movies.append(movie)
            
            context = {"movies": movies}
        else:
            context = {"Error":"You havent recommended anything yet, recommend kar salya"}
        
        return render(request, "movie/myrecommendations.html", context)

    else:
        return render(request, "movie/invalid-user.html")    


def mysubscriptions(request, username):
    context = {}
    return render(request, "movie/mysubscriptions.html", context)

@login_required
def watchlist(request, username):
    movies = get_object_or_404(Watch, user=request.user.id)
    context = {"watchlist": movies.watchlist}
    return render(request, "movie/watchlist.html", context)