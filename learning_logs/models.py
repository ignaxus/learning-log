from django.db import models
from django.conf import settings

class Topic(models.Model):
    #text length in topic is limited
    text = models.CharField(max_length=200)

    #record the date added
    date_added = models.DateTimeField(auto_now_add=True)

    #if the user is deleted, the topics will also be deleted
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
class Entry(models.Model):
    #if the topic is deleted, its enties should also be deleted
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    text = models.TextField()

    #record date added and modified
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]} ..."