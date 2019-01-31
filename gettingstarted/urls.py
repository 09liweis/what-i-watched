from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView
import visuals.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', visuals.views.index, name='index'),
    # url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    
    
    url(r'^api/visuals', visuals.views.visuals, name='visuals'),
    url(r'^api/visual/(?P<id>\d+)', visuals.views.visual_detail, name='visual_detail'),
    url(r'^api/visual/submit', visuals.views.visual_submit, name='visual_submit'),
    url(r'^api/visual/delete', visuals.views.visual_delete, name='visual_delete'),
    url(r'^api/visual/increase_episode', visuals.views.increase_episode, name='increase_episode'),
    url(r'^api/get_imdb_id', visuals.views.get_imdb_id, name='get_imdb'),
    url(r'^api/get_imdb_detail', visuals.views.get_imdb_detail, name='get_imdb_detail'),
    url(r'^api/visual_update_cron', visuals.views.visual_update_cron, name='visual_update_cron'),
    url(r'^api/visual_import', visuals.views.visual_import, name='visual_import'),
    
    url(r'^api/songs', visuals.views.songs, name='songs'),
    url(r'^api/song/submit', visuals.views.song_submit, name='song_submit'),
    url(r'^api/song/(?P<id>\d+)', visuals.views.song_detail, name='song_detail'),
    
    url(r'^api/images', visuals.views.images, name='images'),
    url(r'^api/image/submit', visuals.views.image_submit, name='image_submit'),
]
