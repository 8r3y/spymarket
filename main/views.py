# Create your views here.
from django.template import Context, loader
from main.models import Place, Company, Concurent, District, Review, StoreDetail, Stores_q
from django.http import HttpResponse

#from django.db import connection, transaction

def index(request):
    our_stores = Place.objects.filter(id='1').all()
    enemy_stores_id = Concurent.objects.filter(store_id=1).all()
#    id.enemy_stores.all() 
    t = loader.get_template('main/index.html')
    c = Context({
        'our_stores': our_stores,
        'enemy_stores_id': enemy_stores_id,
        })
    return HttpResponse(t.render(c))

def store_detail(request, place_id):
    target_store = Place.objects.filter(id=place_id).all()
    concurent_stores = Concurent.objects.filter(store_id=place_id).all()
#    id.enemy_stores.all() 
    t = loader.get_template('main/store_detail.html')
    c = Context({
        'target_store': target_store,
        'concurent_stores': concurent_stores,
        })
    return HttpResponse(t.render(c))


def store_list(request):
    our_stores = Place.objects.filter(owner=1).all()
    concurent_stores = Place.objects.filter(owner__lt=1).all()
    t = loader.get_template('main/store_list.html')
    c = Context({
        'our_stores': our_stores,
        'concurent_stores': concurent_stores,        
        })
    return HttpResponse(t.render(c))

def store_compare(request):
    stores_q = Stores_q.objects.raw('SELECT mp.id id, mp.name place_name, mr.date review from main_place as mp '
                                    'left join main_review as mr on mp.id = mr.place_id')
#    stores = StoreDetail.all_stores()
    stores = Place.objects.all()
    concurent_stores = Place.objects.filter(owner__lt=1).all()
    company_link = Company.objects.all()
#    district_link = District.objects.all()
    last_list = Review.objects.all()
    t = loader.get_template('main/store_compare.html')
    c = Context({
        'stores': stores,
        'stores_q': stores_q,
        'concurent_stores': concurent_stores,   
        'company_link': company_link,
#        'district_link': district_link,
        'last_list': last_list,     
        })
    return HttpResponse(t.render(c))

def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)

def list_detail(request, list_id):
    return HttpResponse("You're looking at poll %s." % list_id)

def all_list(request):
    all_stores = Place.objects.all() 
    last_list = Review.objects.all()
    t = loader.get_template('main/list.html')
    c = Context({
        'last_list': last_list,
        'all_stores': all_stores,      
        })
    return HttpResponse(t.render(c))
    