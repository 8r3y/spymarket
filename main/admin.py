from main.models import Card, Review, Price, District, Place, Company, Concurent
from django.contrib import admin

class ReviewAdmin(admin.ModelAdmin):
#    fields = ['place', 'date']
    list_display = ('place', 'date')
    
class ConcurentAdmin(admin.ModelAdmin):
    list_display = ('store', 'concurent')
    list_filter = ['store']

admin.site.register(Card)
admin.site.register(Company)
admin.site.register(Price)
admin.site.register(District)
admin.site.register(Concurent, ConcurentAdmin)
admin.site.register(Place)
admin.site.register(Review, ReviewAdmin)
    