from django import forms

from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from blog.models import *

MAX_UPLOAD_SIZE = 2500000

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ( 'bio', 'picture')
        widgets = {
            'bio': Textarea(attrs={'cols': 120, 'rows': 10}),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ( 'bio', 'picture')
        widgets = {
            'bio': Textarea(attrs={'cols': 120, 'rows': 10}),
        }

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
