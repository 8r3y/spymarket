# Create your views here.
from django.template import Context, loader, RequestContext
from main.models import Place, Company, Concurent, District, Review, StoreDetail, Price, Card, Message, MessageForm, ReviewForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.response import TemplateResponse
from django.contrib.formtools.wizard.views import SessionWizardView
from main.forms import ReviewForm1, ReviewForm2

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
    stores_q = Place.objects.raw('SELECT mp.id id, ' 
                                    'mp.name place_name, '
                                    'mc.id company_id, '
                                    'mc.name company_name, '
                                    'md.name district_name, '
                                    'md.id district_id, '
                                    '(SELECT max(date) from main_review '
                                    'WHERE place_id = mp.id) review_date, '
                                    '(SELECT id from main_review '
                                    'WHERE place_id = mp.id) review_id '                                    
                                    'FROM main_place as mp '
                                    'LEFT JOIN main_company as mc, main_district as md '
                                    'ON mc.id=mp.company_id and md.id = mp.district_id ')
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
    price_link = []
    for i in range(len(cards)):
        i=i+1
        card_link = Card.objects.get(pk=i)
        a = card_link.price_set.all()
        price_link.append(a)

    try:
        selected_choice = p.review_set.get(pk=request.POST['place'])
    except (KeyError, Review.DoesNotExist):
        return render_to_response('main/form_detail.html', {
            'classif': classif,                                                
            'cards': cards,                                                
            'place': p,
            'review': r,
            'price_link': price_link,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('main.views.store_compare', args=(p.id,)))
    
def contact(request):
    errors = []
#    p = Message.objects.all()
    form = MessageForm(request.POST or None)
    context = {
               'subject': request.POST.get('subject', ''),
               'message': request.POST.get('message', ''),
               'email': request.POST.get('email', ''),
               'errors': errors, 
               }
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if not request.POST.get('email'):
            errors.append('Enter an email')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            if request.method == 'POST' and form.is_valid():
                form.save()
                return HttpResponseRedirect('/contact/')
    return TemplateResponse(request, 'main/contact_form.html', context)
#            p.message = request.POST.get('message')
#            p.message.save()
#            p.subject = request.POST.get('subject')
#            p.save()
#            p.email = request.POST.get('email')
#            p.save()
#            send_mail(
#                request.POST['subject'],
#                request.POST['message'],
#                request.POST.get('email', 'noreply@example.com'),
#                ['mind_art@mail.ru'],
#            )
#            return HttpResponseRedirect('/contact/thanks/')
#    return TemplateResponse(request, 'main/contact_form.html', {
#        'errors': errors,
#        'subject': request.POST.get('subject', ''),
#        'message': request.POST.get('message', ''),
#        'email': request.POST.get('email', ''),
#    })
    
def contact1(request):
    p = Message(subject='Test_subj', message='Test_message', email='Test@email.com')
    p.save()
    return HttpResponseRedirect('/contact/')

def review_add(request):
    errors = []
    form = ReviewForm(request.POST or None)
#    r = Review.objects.get(id=self.review_id)
    context = {
               'form': form,
               'errors': errors, 
               }
    if request.method == 'POST':
        if not errors:
            if request.method == 'POST' and form.is_valid():
                form.save()
#                return HttpResponseRedirect(reverse('main.views.review_edit', args=(r)))        
    return TemplateResponse(request, 'main/review_add.html', context)    

# Djangobook examples here:

FORMS = [("place", ReviewForm1),
         ("card", ReviewForm2)]

TEMPLATES = {"place": "main/place_form.html",
             "card": "main/card_form.html"}

class ReviewWizard(SessionWizardView):
    cards = Card.objects.all() 

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(ReviewWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'card':
            context.update({'ok': 'True'})
        return context
   
#    def done(self, form_list, **kwargs):
#        return render_to_response('done.html', {
#            'form_data': [form.cleaned_data for form in form_list],
#        })
    def done(self, form_list, **kwargs):
        place_form    = form_list[0].cleaned_data
        card_form   = form_list[1].cleaned_data
        r = Review.objects.create(
            date        =   place_form['date'],
            pub_date    =   place_form['pub_date'],
            user_name   =   place_form['user_name'],
            pos         =   place_form['pos'],
            cheque      =   place_form['cheque'],
            place       =   place_form['place'],
        )
        p = Price.objects.create(
            review      =   r,
            sku         =   card_form['sku'],
            price       =   card_form['price'],
            price_delta =   card_form['price_delta'],
        )
        return HttpResponseRedirect(reverse('main.views.review_detail', args=(r.id,)))