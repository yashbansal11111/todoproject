from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    Title=models.CharField(max_length=100)
    memo=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True) #This parameter will autoadd the datetime when the todo is created.
    datecompleted=models.DateTimeField(null=True, blank=True)
    Important=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)#Parameter Definition - models.Foreignkey(<model_name>, on_delete=models.CASCADE)
    #CASCADE is a sql standard/term which says for eg. if u delete a blog, CASCADE will delete all of its comments from Database
    #there are other functions of on_delete - DELETE, SET_NULL, PROTECT, RESTRICT, DO_NOTHING, SET_DEFAULT, SET(...)

    def __str__(self):
        return self.Title