from django.contrib import admin
from movie.models import Movie
from movie.models import Recommendation, Subscription, Watch


# Register your models here.

admin.site.register(Movie)
admin.site.register(Recommendation)
admin.site.register(Subscription)
admin.site.register(Watch)
