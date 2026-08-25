from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    titels = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    image = models.ImageField(upload_to='photos/')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Photo, on_delete=models.CASCADE)
    value = models.IntegerField()
