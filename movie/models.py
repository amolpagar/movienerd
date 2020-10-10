from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.

#{'Title': 'Ghatak', 'Year': '2006', 'Rated': 'NA', 'Released': 'A', 'Runtime': '135 min', 
# 'Genre': 'Action Drama Musical', 'Director': 'Swapan Saha', 'Writer': 'NA', 
# 'Actors': 'Jeet, Koyel Mallick, Tapas Pal, Master Angshu', 'Plot': 'Bijoy (Jeet) came to Kolkata with his brother and met with Puja (Koyel Mallick).', 
# 'Language': 'Bengali', 'Country': 'India', 'Awards': 'NA', 'Poster': 'NA', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '8.010'}], 
# 'Metascore': 'NA', 'imdbRating': '8.0', 'imdbVotes': '31', 'imdbID': 'tt4771744', 'Type': 'movie', 
# 'DVD': 'NA', 'BoxOffice': 'N/A', 'Production': 'NA', 'Website': 'NA', 'Response': 'True'}
class Movie(models.Model):   

    title = models.CharField(max_length=50)
    cast = ArrayField(models.CharField(max_length=200), blank=True)
    year = models.DateField(auto_now=False, auto_now_add=False)
    runtime = models.CharField(max_length=50, blank=True)
    genre = models.CharField( max_length=50,blank=True)
    director = models.CharField( max_length=50,blank=True)
    writer = models.CharField( max_length=50, blank=True)
    plot = models.CharField( max_length=350, blank=True)
    language = models.CharField( max_length=50, blank=True)
    country = models.CharField( max_length=10, blank=True)
    awards = models.CharField( max_length=50, blank=True)
    poster = models.CharField(max_length=450, blank=True)
    ratings = models.CharField(max_length=50, blank=True)
    imdbVotes = models.CharField( max_length=10, blank=True)
    category = models.CharField( max_length=50, blank=True )
    platform = ArrayField(models.CharField(max_length=200), blank=True)
 
    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Recommendation(models.Model):
    def __str__(self):
        return str(self.user)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    def __str__(self):
        return str(self.user)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribing_user_id = models.IntegerField(default=0)    
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    
class Watch(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = ArrayField(models.IntegerField(), blank=True)
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    