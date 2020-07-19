from django.contrib import admin

# Register your models here.
from .models import Movies, Genre, Director

admin.site.register(Movies)
admin.site.register(Genre)
admin.site.register(Director)
