from django.db import models
from martor.models import MartorField
from martor.fields import MartorFormField

class Simple(models.Model):  #it is created by sk
    title = models.CharField(max_length=200)
    description = MartorFormField()
    #wiki = MartorFormField()

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = MartorField()
    #wiki = MartorField()
