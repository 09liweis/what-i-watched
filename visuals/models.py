from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Visual(models.Model):
    title = models.CharField(max_length=60, blank=True)
    original_title = models.CharField(max_length=60, blank=True)
    douban_id = models.CharField(max_length=60, unique=True)
    douban_rating = models.FloatField(blank=True, default=0.0)
    imdb_id = models.CharField(max_length=60, blank=True)
    imdb_rating = models.FloatField(blank=True, default=0.0)
    rotten_id = models.CharField(max_length=60, blank=True)
    rotten_rating = models.IntegerField(blank=True, default=0)
    rotten_audience_rating = models.IntegerField(blank=True, default=0)
    release_date = models.TextField(blank=True)
    poster = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    online_source = models.TextField(blank=True)
    episodes = models.IntegerField(blank=True, default=0)
    current_episode = models.IntegerField(blank=True, default=0)
    date_watched = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now = True)
    visual_type = models.TextField(default='movie')
    # visual_type = models.ManyToManyField(Type, blank=True)
    # favorite = models.ManyToManyField(User, blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_watched']

class Song(models.Model):
    title = models.CharField(max_length=60, blank=True)
    url = models.TextField(blank=True)
    image = models.TextField(blank=True)
    artist = models.CharField(max_length=60, blank=True)
    visual = models.ForeignKey(Visual, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('date_updated',)

class VisualImage(models.Model):
    pass