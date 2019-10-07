from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username = models.CharField('username',unique=True, max_length=64)
    email = models.EmailField('email',unique=True)
    password = models.CharField('password', max_length=16, help_text="密码长度为8到16位字符串, 需包含大小写字母和数字")
    following = models.ManyToManyField("self", symmetrical=False)
    # TODO: adding user detailed profile, like birthday/location/avatar/bio

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    modified_at =models.DateTimeField('modified_at')
    content = models.TextField('content')
    # TODO: the content of the recipe may be divided into several text/form/img

class Dish(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    content = models.TextField('content')
    # TODO: content also need img src path

# TODO: for future extension
class Question(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField('created_at')

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    created_at = models.DateTimeField('created_at')

class Category(models.Model):
    pass

class Event(models.Model):
    pass

'''
TODO:
one-to-many mapping: user->recipe, user->dish, recipe->question, dish->comment
many-to-many mapping: user<->user, recipe<->category, dish<->event
[?] since django offer the admin dashboard, I was not sure I still need a Role table and role->user mapping
'''
