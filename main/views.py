# Create your views here.
from django.template import Context, loader, RequestContext
from main.models import Place, Company, Concurent, District, Review, StoreDetail, Stores_q, Price, Card
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

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

def review_detail(request, review_id):
    r = get_object_or_404(Review, pk=review_id)
    p = Place.objects.get(id=4)
    cards = Card.objects.all()
    classif = Card.objects.distinct()
    try:
        selected_choice = p.review_set.get(pk=request.POST['place'])
    except (KeyError, Review.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('main/form_detail.html', {
            'classif': classif,                                                
            'cards': cards,                                                
            'place': p,
            'review': r,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('main.views.store_compare', args=(p.id,)))
    