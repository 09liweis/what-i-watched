from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visuals.models import Visual, Song, VisualImage, Country, Language
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
import urllib3, json
import re
import time
# import requests

def get_content_from_url(url):
    '''return url content'''
    url_content = urllib3.PoolManager().request('GET', url)
    decode_data = url_content.data.decode('utf-8')
    # decode_data = requests.get(url).text
    return decode_data

def index(request):
    '''API index page'''
    return json_response({
        'status': 200,
        'msg': 'Something is comming'
    })

def json_response(result):
    resp = JsonResponse(result)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

def stats(request):
    visuals = Visual.objects.all()
    statics = {
        'movie': 0,
        'tv': 0,
        'years':{},
        'countries':{},
        'languages':{}
    }
    for v in visuals:
        if v.visual_type == 'movie':
            statics['movie'] += 1
        else:
            statics['tv'] += 1
        
        countries = v.country_set.all()
        for c in countries:
            title_zh = c.title_zh
            if title_zh in statics['countries']:
                statics['countries'][title_zh] += 1
            else:
                statics['countries'][title_zh] = 1
        
        languages = v.language_set.all()
        for l in languages:
                title_zh = l.title_zh
                if title_zh in statics['languages']:
                    statics['languages'][title_zh] += 1
                else:
                    statics['languages'][title_zh] = 1
            
        release_date = v.release_date
        if release_date:
            year = release_date[0:4]
            if year in statics['years']:
                statics['years'][year] += 1
            else:
                statics['years'][year] = 1
    return json_response(statics)

# visual list function
def visuals(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    tp = request.GET.get('type')
    total = Visual.objects.all().count()
    # ternary operator
    page = int(page) if page else 1
    limit = int(limit) if limit else total
    offset = (page - 1) * limit
    
    if tp == 'not_start':
        visuals = Visual.objects.filter(current_episode=0).order_by('-date_updated')
        total = len(visuals)
    else:
        visuals = Visual.objects.filter().order_by('-date_updated')[offset:offset + limit]
    results = []
    for v in visuals:
        results.append(v.json())
    return json_response(
        {
            'results': results,
            'total': total,
            'per_page': limit,
            'type': 'list',
            'page': page,
        }
    )

def visual_search(request):
    '''Function to search keyword for visuals'''
    keyword = request.GET.get('keyword')
    results = []
    if keyword:
        visuals = Visual.objects.filter(title__icontains=keyword)
        for v in visuals:
            results.append(v.json())
    return json_response({
        'results': results,
        'keyword': keyword
    })

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
    print(request.POST)
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
    if id == 0:
      visual.save()
    else:
      visual.save(update_fields=['douban_id','imdb_id','duration','douban_rating','website','release_date','imdb_rating','episodes','current_episode','original_title','title','poster'])
    # update_visual(visual)
    if 'countries[]' in kv:
      countries = kv['countries[]']
    if 'countries[0]' in kv:
      countries - kv['countries[0]']
    if countries:
      connectVC(visual, countries)
    if 'languages[]' in kv:
      languages = kv['languages[]']
    if 'languages[0]' in kv:
      languages - kv['languages[0]']
    if languages:
      connectVL(visual, languages)
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
    # douban_movie_url = 'https://movie.douban.com/subject/' + douban_id
    douban_movie_url = 'https://samliweisen.herokuapp.com/api/visuals/get_imdb_id?douban_id=' + douban_id
    decode_data = get_content_from_url(douban_movie_url)
    
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

def get_imdb_id_from_douban(douban_id):
    douban_movie_url = 'https://movie.douban.com/subject/' + douban_id
    decode_data = get_content_from_url(douban_movie_url)
    imdb_list = re.findall('href="http://www.imdb.com/title/(.*?)"', decode_data)
    imdb_id = ''
    if len(imdb_list) > 0:
        imdb_id = imdb_list[0]
    return imdb_id

@csrf_exempt
def get_imdb_detail(request):
    '''Get imdb detail with imdb id'''
    imdb_id = request.GET.get('imdb_id')
    imdb_rating = get_imdb_rating(imdb_id)
    return json_response({
        'statue': 200,
        'imdb_rating': imdb_rating
    })

def get_imdb_rating(imdb_id):
    '''Get imdb rating with imdb id from imdb website'''
    imdb_url = 'https://www.imdb.com/title/' + imdb_id
    decode_data = get_content_from_url(imdb_url)
    imdb_rating_array = re.findall('<span itemprop="ratingValue">(.*?)</span>', decode_data)
    imdb_rating = ''
    if len(imdb_rating_array) > 0:
        imdb_rating = imdb_rating_array[0]
    return imdb_rating

def visual_update_cron(request):
    '''Update all the existing visuals with latest douban info or imdb info'''
    t = request.GET.get('type')
    id = request.GET.get('id')
    if t or id:
        if t == 'random':
            visual = get_random_visual()
        if id:
            visual = Visual.objects.get(id=id)
        visual = update_visual(visual)
        return json_response({
            'result': visual.json()
        })
    else:
        visuals = Visual.objects.all().order_by('-date_updated')
        for visual in visuals:
            update_visual(visual)
            time.sleep(10)
        return json_response({
            'status': 200
        })

def random_visual(request):
    visual = get_random_visual()
    return json_response({'status':200,'result':visual.json()})

def get_random_visual():
    '''Return random Visual'''
    visual = Visual.objects.order_by('?')[0]
    return visual

def update_visual(visual):
    '''Return the updated visual'''
    douban_id = visual.douban_id
    website = ''
    imdb_id = visual.imdb_id
    if not imdb_id:
        try:
            imdb_id = get_imdb_id_from_douban(douban_id)
            visual.imdb_id = imdb_id
        except:
            print('Not able to get imdb id from douban website')
    try:
        imdb_api = 'https://www.omdbapi.com/?apikey=6ad10fa5&i=' + imdb_id
        imdb_data = json.loads(get_content_from_url(imdb_api))
        if 'Website' in imdb_data and imdb_data['Website'] != 'N/A':
            website = imdb_data['Website']
        if 'Ratings' in imdb_data:
            ratings = imdb_data['Ratings']
            for rating in ratings:
                if rating['Source'] == 'Rotten Tomatoes':
                    visual.rotten_rating = int(rating['Value'].replace('%',''))
    except Exception as e:
        print(str(e))

    if douban_id:
        try:
            # douban_api = 'https://api.douban.com/v2/movie/subject/' + douban_id + '?apikey=0df993c66c0c636e29ecbb5344252a4a'
            douban_api = 'https://samliweisen.herokuapp.com/api/visuals/douban?douban_id=' + douban_id
            douban_data = json.loads(get_content_from_url(douban_api))
            # print(douban_data)

            durations = douban_data['durations']
    
            if durations:
                durations = durations[0]
                duration = ''
                for s in durations:
                    if s.isdigit():
                        duration += s
                visual.duration = duration
            
            #country
            countries = douban_data['countries']
            connectVC(visual, countries)
            
            #language
            languages = douban_data['languages']
            connectVL(visual, languages)
            
            # get douban rating
            douban_rating = douban_data['rating']['average']
            if not website:
                website = douban_data['website']
    
            # release_date = douban_data['pubdate']
            # if release_date == '':
            #     release_date = douban_data['pubdates'][0]
            #     release_date = release_date[0:10]
            episodes = douban_data['episodes_count']
            title = douban_data['title']
            original_title = douban_data['original_title']
            if visual.imdb_id:
                imdb_rating = get_imdb_rating(visual.imdb_id)
                # in case imdb update the html class name
                if imdb_rating:
                    visual.imdb_rating = imdb_rating
    
            #update douban rating
            if douban_rating:
                visual.douban_rating = douban_rating
            if website:
                visual.website = website
            visual.original_title = original_title
            visual.title = title
            # if release_date:
            #     visual.release_date = release_date
            if episodes:
                visual.episodes = episodes
        except Exception as e:
            print(str(e))
        visual.save(update_fields=['duration','imdb_id','current_episode','douban_rating','website','release_date','imdb_rating','episodes','original_title','title','poster'])
        return visual

def visual_import(request):
    '''Import production data to development'''
    production_api = 'https://what-i-watched.herokuapp.com/api/visuals'
    decode_data = json.loads(get_content_from_url(production_api))
    visuals = decode_data['results']
    if len(visuals) > 0:
        Visual.objects.all().delete()
    
    for i in range(len(visuals) - 1, 0, -1):
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
    
def countries(request):
    '''Get all countries'''
    countries = Country.objects.all()
    result = []
    for c in countries:
        result.append(c.title_zh)
    return json_response({'status': 200, 'result':result})

def languages(request):
    languages = Language.objects.all()
    result = []
    for l in languages:
        result.append(l.title_zh)
    return json_response({'status':200,'result':result})
    
def connectVC(visual, countries):
    '''Connect Visual to Countries'''
    for c in countries:
        try:
            country = Country.objects.get(title_zh=c)
        except:
            country = Country.objects.create()
            country.title_zh = c
            country.save()
        if country not in visual.country_set.all():
            country.visuals.add(visual)

def connectVL(visual, languages):
    for lang in languages:
        try:
            l = Language.objects.get(title_zh=lang)
        except:
            l = Language.objects.create()
            l.title_zh = lang
            l.save()
        if l not in visual.language_set.all():
            l.visuals.add(visual)