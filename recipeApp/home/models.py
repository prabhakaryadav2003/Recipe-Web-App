from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    description = models.TextField()
    link = models.URLField(null=True,blank=True)
    image = models.ImageField(upload_to="recipieImg")

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering = ['id']  # Default ordering by 'id'