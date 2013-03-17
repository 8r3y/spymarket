from django import forms
from main.models import Place, Card

class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()

class ContactForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    

class ReviewForm1(forms.Form):
    date = forms.DateField(required=True,label=u'Review date: ', help_text=u'Enter date')
    pub_date = forms.DateField(required=True,label=u'Publication date: ', help_text=u'Enter date')
    user_name = forms.CharField(max_length=200)
    pos = forms.IntegerField()
    cheque = forms.IntegerField()
    place = NameModelChoiceField(label=u'Store',queryset=Place.objects.order_by('-name'),initial = Place.objects.get(id = 1))
    
class ReviewForm2(forms.Form):
    sku = NameModelChoiceField(label=u'Card',queryset=Card.objects.order_by('-name'))
    price = forms.FloatField()
    price_delta = forms.FloatField()
