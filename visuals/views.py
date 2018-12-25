from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visuals.models import Visual, Song, VisualImage
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
import urllib3, json
import re
import time

def index(request):
    # return json_response({
    #     'status': 200,
    #     'msg': 'Something is comming'
    # })
    return render(request, 'index.html')

def json_response(result):
    resp = JsonResponse(result)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

# visual list function
def visuals(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    # ternary operator
    page = int(page) if page else 1
    limit = int(limit) if limit else Visual.objects.all().count()
    offset = (page - 1) * limit
    
    visuals = Visual.objects.all().order_by('-date_updated')[offset:offset + limit]
    results = []
    for v in visuals:
        results.append(v.json())
    return json_response({'results': results, 'count': len(results), 'per_page': limit, 'type': 'list'})

def check_douban_id(douban_id):
    '''
    Check if visual exists with douban id
    '''
    try:
        Visual.objects.get(douban_id=douban_id)
        exist = True
        
    except:
        exist = False
    return exist

def visual_detail(request, id):
    '''
    Return response of visual detail based on visual id.
    '''
    try: 
        visual = Visual.objects.get(id=id)
        result = visual.json()
    except ObjectDoesNotExist:
        result = 'Visual Not Exsit'
    return json_response({'result': result, 'type': 'detail'})

@csrf_exempt
def visual_submit(request):
    '''
    funciton to add or update visual
    '''
    id = int(request.POST.get('id'))
    kv = dict(request.POST)
    
    del kv['id']

    if id == 0:
        douban_id = kv['douban_id'][0]
        exist = check_douban_id(douban_id)
        
        if exist:
            result = {
                'msg': 'Douban Id exist',
                'code': 'exist'
            }
            return json_response(result)
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
    return json_response({'status': 200})
    
@csrf_exempt
def visual_delete(request):
    '''Delete a visual'''
    visual_id = request.POST.get('id')
    if not visual_id:
        msg = 'Id not found'
    elif not visual_id.isdigit():
        msg = 'Id is not invalid'
    else:
        visual_id = int(visual_id)
        try: 
            visual = Visual.objects.get(id=visual_id)
            visual.delete()
            msg = 'Visual ' + id + ' has been deleted'
        except ObjectDoesNotExist:
            msg = 'Visual Not Exsit'
    return json_response({'status': 200, 'msg': msg})

@csrf_exempt
def increase_episode(request):
    '''
    Increase one episode of the unfinished visual
    '''
    visual = Visual.objects.get(id = request.GET.get('id'))
    visual.increase_episode()
    return json_response({
        'status': 200,
        'current_episode': visual.current_episode
    })

@csrf_exempt
def get_imdb_id(request):
    douban_id = request.GET.get('douban_id')
    if not douban_id:
        return json_response({
            'status': 200,
            'msg': 'Douban id not found'
        })
    douban_movie_url = 'https://movie.douban.com/subject/' + douban_id
    url_content = urllib3.PoolManager().request('GET', douban_movie_url)
    decode_data = url_content.data.decode('utf-8')
    imdb_list = re.findall('href="http://www.imdb.com/title/(.*?)"', decode_data)
    # get list of release dates from webpage
    release_dates = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}\([\u4e00-\u9fff]+\)', decode_data)
    # remove duplicate release date
    release_dates = list(set(release_dates))
    # initial imdb_id
    imdb_id = ''
    if len(imdb_list) > 0:
        imdb_id = imdb_list[0]
    return json_response({
        'status': 200,
        'imdb_id': imdb_id,
        'release_dates': release_dates
    })

def visual_update_cron(request):
    '''Update all the existing visuals with latest douban rating'''
    visuals = Visual.objects.all().order_by('-date_updated')
    for visual in visuals:
        douban_id = visual.douban_id
        if douban_id:
            douban_api = 'https://api.douban.com/v2/movie/subject/' + douban_id + '?apikey=0df993c66c0c636e29ecbb5344252a4a'
            url_content = urllib3.PoolManager().request('GET', douban_api)
            douban_data = json.loads(url_content.data.decode('utf-8'))
            
            # get douban rating
            douban_rating = douban_data['rating']['average']

            #update douban rating
            visual.douban_rating = douban_rating
            visual.save(update_fields=['douban_rating'])
            time.sleep(5)
    return json_response({
        'status': 200
    })

def visual_import(request):
    '''Import production data to development'''
    production_api = 'https://what-i-watched.herokuapp.com/api/visuals'
    url_content = urllib3.PoolManager().request('GET', production_api)
    decode_data = json.loads(url_content.data.decode('utf-8'))
    visuals = decode_data['results']
    if len(visuals) > 0:
        Visual.objects.all().delete()
    
    for i in range(len(visuals) - 1, 0, -1):
        print(i)
        visual = Visual.objects.create()
        # remove id attribute
        v = visuals[i]
        del v['id']
        for key in v:
            setattr(visual, key, v[key])
        visual.save()
    return json_response({
        'status': 200
    })

# /api/songs?visual_id=1
# /api/songs
def songs(request):
    visual_id = request.GET.get('visual_id')
    if (visual_id):
        # get songs for specific visual
        songs = Song.objects.filter(visual_id=visual_id).order_by('-date_updated')
    else:
        songs = Song.objects.all().order_by('-date_updated')
    results = []
    for s in songs:
        results.append(s.get_dict())
    return json_response({'results': results})

def song_detail(request, id):
    '''Return song with id'''
    song = Song.objects.get(id=id)
    return json_response({'result': song.get_dict()})

@csrf_exempt
def song_submit(request):
    id = request.POST.get('id')
    if int(id) == 0:
        # create song with initial visual relationship
        visual_id = request.POST.get('visual_id')
        visual = Visual.objects.get(id=visual_id)
        song = Song.objects.create(visual=visual)
    else:
        song = Song.objects.get(id=id)
    
    title = request.POST.get('title')
    artist = request.POST.get('artist')
    url = request.POST.get('url')
    image = request.POST.get('image')

    song.title = title
    song.artist = artist
    song.url = url
    song.image = image

    song.save()
    return json_response({'result': 200})

def images(request):
    visual_id = request.GET.get('visual_id')
    if (visual_id):
        images = VisualImage.objects.filter(visual_id=visual_id).order_by('-date_updated')
    else:
        images = VisualImage.objects.all().order_by('-date_updated')
    results = []
    for image in images:
        results.append({
            'id': image.id,
            'title': image.title,
            'url': image.url
        })
    return json_response(results)

@csrf_exempt
def image_submit(request):
    id = request.POST.get('id')
    if int(id) == 0:
        visual_id = request.POST.get('visual_id')
        visual = Visual.objects.get(id=visual_id)
        image = VisualImage.objects.create(visual=visual)
    else:
        image = VisualImage.objects.get(id=id)
    
    title = request.POST.get('title')
    url = request.POST.get('url')
    image.title = title
    image.url = url
    image.save()
    result = {'result': 200}
    return json_response(result)