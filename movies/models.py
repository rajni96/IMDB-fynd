from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movies(models.Model):
    name = models.CharField(max_length=100)
    imdb_score = models.FloatField(default=0.00)
    popularity = models.FloatField(default=0.00)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        unique_together = [["name", "director"]]

