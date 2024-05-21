from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['avatar'].widget.attrs.update({'onchange': 'previewAvatar();'})
            self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
            if self.instance.avatar:
                self.fields['avatar'].widget.attrs.update({
                    'data-current-avatar-url': self.instance.avatar.url
                })


class FriendSearchForm(forms.Form):
    email = forms.EmailField(label='Add new friend by email', max_length=100, required=True)
