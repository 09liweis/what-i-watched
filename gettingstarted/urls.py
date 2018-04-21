from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import visuals.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', visuals.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    
    
    url(r'^api/visuals', visuals.views.visuals, name='visuals'),
    url(r'^api/visual/(?P<id>\d+)', visuals.views.detail, name='detail'),
    url(r'^api/visual/check/(?P<douban_id>\d+)', visuals.views.checkDoubanExist, name='check'),
    url(r'^api/visual/submit', visuals.views.submit, name='submit'),
    url(r'^api/visual/increase_episode', visuals.views.increase_episode, name='increase_episode'),
    url(r'^api/get_imdb_id', visuals.views.get_imdb_id, name='get_imdb'),
    
    url(r'^api/songs', visuals.views.songs, name='songs'),
    url(r'^api/song/submit', visuals.views.song_submit, name='song_submit'),
    url(r'^api/song/(?P<id>\d+)', visuals.views.song_detail, name='song_detail'),
    
    
]
