from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visuals.models import Visual
# Create your views here.
import urllib2
import re

def index(request):
    return render(request, 'index.html')

def list(request):
    visuals = Visual.objects.all()
    results = []
    for visual in visuals:
        results.append({
            'id': visual.id,
            'title': visual.title,
            'original_title': visual.original_title,
            'douban_rating': visual.douban_rating,
            'poster': visual.poster
        })
    return JsonResponse({'results': results})

def detail(request, id):
    visual = get_object_or_404(Visual, pk=id)
    result = {
        'id': visual.id,
        'title': visual.title,
        'original_title': visual.original_title,
        'douban_id': visual.douban_id,
        'douban_rating': visual.douban_rating,
        'imdb_id': visual.imdb_id,
        'imdb_rating': visual.imdb_rating,
        'rotten_id': visual.rotten_id,
        'rotten_rating': visual.rotten_rating,
        'rotten_audience_rating': visual.rotten_audience_rating,
        'release_date': visual.release_date,
        'poster': visual.poster,
        'summary': visual.summary,
        'online_source': visual.online_source,
        'episodes': visual.episodes,
        'current_episode': visual.current_episode,
        'visual_type': visual.visual_type
    }
    return JsonResponse({'result': result})

@csrf_exempt
def submit(request):
    id = int(request.POST.get('id'))
    kv = dict(request.POST)
    del kv['id']
    if id == 0:
        visual = Visual.objects.create()
    else:
        visual = Visual.objects.get(id=id)
    for key in kv:
        value = kv[key][0]
        if key in ['douban_rating', 'imdb_rating']:
            value = float(value)
        if key in ['rotten_rating', 'rotten_audience_rating', 'episodes', 'current_episode']:
            if value == '':
                value = 0
            value = int(value)
        setattr(visual, key, value)
    visual.save()
    return JsonResponse({'status': 200})

@csrf_exempt
def get_imdb_id(request):
    douban_id = request.GET.get('douban_id')
    url = 'https://movie.douban.com/subject/' + douban_id
    url_content = urllib2.urlopen(url).read()
    answers = re.findall('href="http://www.imdb.com/title/(.*?)"', url_content)
    imdb_id = ''
    if len(answers) > 0:
        imdb_id = answers[0]
    response = {'imdb_id': imdb_id}
    return JsonResponse(response)