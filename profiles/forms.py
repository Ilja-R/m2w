from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'avatar')


class FriendSearchForm(forms.Form):
    email = forms.EmailField(label='Add new friend by email', max_length=100, required=True)
