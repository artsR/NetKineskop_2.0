from django import forms

from .models import Tag



class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name', 'color')
        widgets = {
            'color': forms.widgets.TextInput(attrs={
                'type': 'color'
            })
        }
