from django import forms
from django.contrib.auth.models import User
from .models import ProfilePic, InputPic

#form to update profile picture
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= ProfilePic
        fields= ['image']

#form to update profile picture
class InputPicForm(forms.Form):
    image = forms.ImageField()

    image.widget.attrs.update({'onchange': 'readURL(this);', 'class': 'form-group'})
