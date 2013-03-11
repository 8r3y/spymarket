from django.db import models

# Create your models here.
class Classif(models.Model):
    name = models.CharField(max_length=200)
    sm_id = models.IntegerField()
    def __unicode__(self):
        return self.name

class Card(models.Model):
    articul = models.CharField(max_length=14)
    name = models.CharField(max_length=200)
    bar = models.CharField(max_length=40)
    classif = models.ForeignKey(Classif)
    base_price = models.FloatField()
    def __unicode__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    
class Place(models.Model):
    name = models.CharField(max_length=200)
    district = models.ForeignKey(District, related_name='Store_district')
    company = models.ForeignKey(Company)
    owner = models.BooleanField()
    location = models.CharField(max_length=200)
#    reviews = models.ManyToManyField('Review', related_name='Store_review', null = True)
    def __unicode__(self):
        return self.name

class Review(models.Model):
    date = models.DateField()
    pub_date = models.DateTimeField()
    user_name = models.CharField(max_length=200)
    pos = models.IntegerField()
    cheque = models.IntegerField()
    place = models.ForeignKey(Place)
    def __unicode__(self):
        return u'%s %s' % (self.id, self.date)

class Price(models.Model):
    review = models.ForeignKey(Review)
    sku = models.ForeignKey(Card)
    price = models.FloatField()
    price_delta = models.FloatField()
    def __unicode__ (self):
        return u'%s %s %s' % (self.review, self.sku, self.price) 
    
class Concurent(models.Model): 
    store = models.ForeignKey(Place, related_name='our')
    concurent = models.ForeignKey(Place, related_name='enemy')
    #concurent = models.ManyToManyField(Place, related_name='enemy')
#    def __unicode__(self):
#        return self.concurent

class StoreDetail(models.Manager):
    def all_stores(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
                select * from main_place as mp
                left join main_review as mr on mp.id = mr.place_id
            """)
        result_list = cursor.fetchall()
        return result_list
    
class Stores_q(models.Model):
    place_name = models.CharField(max_length=200)
    district_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    review = models.DateField()
    
class Classif_price(models.Model):
    review = models.ForeignKey(Review)
    classif = models.ForeignKey(Classif)
    price_delta = models.FloatField()
    def __unicode__ (self):
        return u'%s %s %s' % (self.review, self.classif, self.price_delta)        