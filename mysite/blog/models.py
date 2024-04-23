from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=225)
    role = models.CharField(max_length=10)
    email = models.CharField(max_length=50)

class Blog(models.Model):
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    created_at = models.CharField(max_length=100)
    updated_at = models.CharField(max_length=100)

class Comments(models.Model):
    description = models.CharField(max_length=225)
    created_at = models.CharField(max_length=100)
