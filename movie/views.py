from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from movie.models import Recommendation, Movie, Subscription,Watch
from django.core.paginator import Paginator
import requests, json, ast
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
            #baseurl = "https://y6jvg90md0.execute-api.us-east-2.amazonaws.com/dev1/get_movies?movie="+title
            baseurl = "https://api.themoviedb.org/3/search/movie?api_key=61e8f206a9a1e964cc3d57e67e2c15e3&language=en-US&query="+title
            response = requests.get(baseurl).json()  
            print(response)
            print("*****************")                
            context = {"response": response, "title": title}

            return render(request, "movie/searchmovies.html", context)
    else:
        return render(request, "movie/invalid-user.html")

    return render(request, "movie/searchmovies.html")

# This method is used to retrieve recommendations of user
@login_required
def myrecommendations(request, username):  
    movies = []
    context = {}
    user_rd = Recommendation.objects.filter(user=request.user).exists()
    if user_rd:
        rd = Recommendation.objects.get(user=request.user)
        for rd_item in rd.recommendation_list:
            movie = Movie.objects.get(id=rd_item)
            movies.append(movie)            
        context = {"movies": reversed(movies), "username": username}               
    return render(request, "movie/myrecommendations.html", context)
    
# This method is used to add recommendations
@login_required
def recommend(request):
    movie = request.GET.get('movie')
    movie = cleanUpMovieData(movie)
    title = movie["title"]   
    year = movie["release_date"]
    movie = searchOrAddMovie(title=title, year=year, movie=movie)
    movieid = movie.id
    user_rd_info = Recommendation.objects.filter(user=request.user).exists()
    if user_rd_info:
        user_rd = Recommendation.objects.get(user=request.user)
        if movieid not in user_rd.recommendation_list:
            user_rd.recommendation_list.append(movieid)
            add_recommendation, created = Recommendation.objects.update_or_create(user=request.user, defaults={"recommendation_list":user_rd.recommendation_list})

    return redirect('myrecommendations', username=request.user.username)        


    context = {}
    return render(request, "movie/myrecommendations.html", context)

# DELETE: this method is used to delete movie recommendation for a user
def deleterecommendation(request, movieid):
    user_rd_info = Recommendation.objects.filter(user=request.user).exists()
    if user_rd_info:
        user_rd = Recommendation.objects.get(user=request.user)
        if movieid in user_rd.recommendation_list:
            user_rd.recommendation_list.remove(movieid)
            update_rd, created = Recommendation.objects.update_or_create(user=request.user, defaults={"recommendation_list": user_rd.recommendation_list})
    return redirect('myrecommendations', username=request.user.username)

@login_required
def mysubscriptions(request, username):
    searched_users = None
    if 'user_name' in request.GET:
        searched_users = User.objects.filter(username__contains=request.GET['user_name'])
        paginator = Paginator(searched_users, 3)
        page = request.GET.get('page')
        searched_users_page  = paginator.get_page(page)

    mysubscriptions = Subscription.objects.filter(user=request.user.id).exists()
    subscribed_users = []
    if mysubscriptions:
        mysubscriptions = Subscription.objects.get(user=request.user.id)
        for each_user_id in mysubscriptions.subscribing_user_id:
            user = User.objects.get(id=each_user_id)
            subscribed_users.append(user)

    context = {"searched_users":searched_users, "subscribed_users": subscribed_users}
    return render(request, "movie/mysubscriptions.html", context)

@login_required
def mysubscribers(request, username):
    mysubscribers = Subscription.objects.filter(user=request.user.id).exists()
    subscriber_users = []
    if mysubscribers:
        mysubscribers = Subscription.objects.get(user=request.user.id)
        for each_user_id in mysubscribers.subscribers_user_id:
            user = User.objects.get(id=each_user_id)
            subscriber_users.append(user)

    context = {"subscribed_users": subscriber_users}    
    return render(request, "movie/mysubscribers.html", context)

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

# This method is used to unsubscribe user
@login_required
def unsubscribe(request, userid):
    subscriptions = Subscription.objects.filter(user=request.user).exists()
    if subscriptions:
        subscriptions = Subscription.objects.get(user=request.user)
        subscribing_user_ids = subscriptions.subscribing_user_id
        if userid in subscribing_user_ids:
            subscribing_user_ids.remove(userid)
            update_subscription, created = Subscription.objects.update_or_create(user=request.user, defaults={"subscribing_user_id":subscribing_user_ids})
    
    return redirect('mysubscriptions', username=request.user.username)

# This method is used to retrieve user specific watchlist queue and display on page
@login_required
def watchlist(request, username):
    user_watchlist_exist = Watch.objects.filter(user=request.user).exists()
    context = {}
    if user_watchlist_exist:
        user_watch = Watch.objects.get(user=request.user)
        movies = []
        for movie_id in user_watch.watchlist:
            movies.append(Movie.objects.get(id=movie_id))
            movies = list(dict.fromkeys(movies)) # remove duplicates list to dictionary to list
        context = {"movies_watchlist": reversed(movies)}

    return render(request, "movie/watchlist.html", context)


# This method is used to add movie to watch table for user
def addtowatchlist(request):
    movie = request.GET.get('movie')
    movie = cleanUpMovieData(movie)
    title = movie["title"]
    year = movie["release_date"]
    user_watchlist = Watch.objects.filter(user=request.user).exists()
    user_watch = "{}"
    if user_watchlist:
        user_watch = Watch.objects.get(user=request.user)
    else:
        user_watch, created = Watch.objects.get_or_create(user=request.user, watchlist=user_watch)
        if created:
            user_watch = user_watch[0]

    movie = searchOrAddMovie(title=title, year=year, movie=movie)
    
    if movie.id not in user_watch.watchlist:   
        user_watch.watchlist.append(movie.id)        
        add_to_watchlist, created = Watch.objects.update_or_create(user=request.user, defaults={'watchlist': user_watch.watchlist})
    
    return redirect('watchlist', username=request.user.username)


# common method to search movie and ifs not present then add it to Movie table
def searchOrAddMovie(title, year, movie):
    movie_found_in_database = Movie.objects.filter(title=title, year=year).exists()    
    if movie_found_in_database:
        movie = Movie.objects.get(title=title, year=year)                
    else:
        movie = addMovieAndGet(movie)
    return movie

#clean up movie response json
def cleanUpMovieData(movie):
    print(movie)
    movie = movie.replace("False,", "false,")
    movie = movie.replace("True,", "true,")
    movie = movie.replace("', '", '\", \"')
    movie = movie.replace(", '", ', \"')
    movie = movie.replace("': '", '\": \"')
    movie = movie.replace("':", '\":')
    movie = movie.replace("{'", '{\"')
    movie = movie.replace("'}", '\"}')
    movie = movie.replace("None,", '\"None\",')
    print("##############")
    print(movie)
    movie = json.loads(movie)
    return movie

# This method will remove movie id from watchlist
def deletefromwatchlist(request, movieid):
    user_watchlist_info = Watch.objects.get(user=request.user)
    if movieid in user_watchlist_info.watchlist:
        user_watchlist_info.watchlist.remove(movieid)
        update_watchlist, created = Watch.objects.update_or_create(user=request.user, defaults={'watchlist': user_watchlist_info.watchlist})

    return redirect('watchlist', username=request.user.username)



# This method will find movie based on title and year in movie table 
def movieExist(title, year):
    moviefound = get_object_or_404(Movie, title=title, year=year)
    return moviefound

# This method is used to add movie into movie db and generate movie id
def addMovieAndGet(movie):
    title = movie["title"]
    year = movie["release_date"]
    cast = "{}" 
    # runtime = movie.runtime
    # genre = movie.genre
    # director = movie.director
    # writer = movie.writer
    plot = movie["overview"]
    language = movie["original_language"]
    # country = movie.country
    # awards = movie.awards
    poster = movie["poster_path"]
    ratings = movie["popularity"]
    # imdbvotes = movie.imdbvotes
    # category = movie.category    
    platform = "{}"
    movieadded = Movie.objects.create(title=title,
                                      year=year,
                                      cast=cast,                                                                            
                                      plot=plot,                                      
                                      poster=poster,
                                      language=language,
                                      ratings=ratings,                                      
                                      platform=platform)
    movieadded.save()
    return movieadded