from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name' : TextInput(
                attrs={
                    'id' : 'tags',
                    'class' : 'input',
                    'placeholder' : 'City Name',
                    'name' : 'city_name',
                    'autofocus' : ''
                }
        )}
