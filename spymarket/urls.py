from django.conf.urls import patterns, include, url

from main.forms import ReviewForm1, ReviewForm2
from main.views import ReviewWizard, FORMS

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.index', name='index'),
    url(r'^store/(?P<place_id>\d+)/$', 'main.views.store_detail', name='store_detail'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'main.views.detail'),
    # url(r'^spymarket/', include('spymarket.foo.urls')),
    url(r'^list/(?P<list_id>\d+)/$', 'main.views.list_detail'),
    url(r'^list/', 'main.views.all_list'),
    url(r'^store/', 'main.views.store_compare', name='store_compare'),

    url(r'^review/(?P<review_id>\d+)/$', 'main.views.review_detail'),
#    url(r'^contact/', 'main.views.contact'),
#    url(r'^contact1/', 'main.views.contact1'),
    
    url(r'^review_add/', 'main.views.review_add'),
    
    url(r'^review_wizard/$', ReviewWizard.as_view(FORMS), name='add_review_wizard'),    
        
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

#    url(r'^review/', 'main.views.review'),    
)
