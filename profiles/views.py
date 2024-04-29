from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.forms import ProfileForm
from profiles.models import Profile


@login_required(login_url='login')
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/my_profile.html', context)


@login_required(login_url='login')
def my_friends(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    context = {
        'friends': friends,
    }
    return render(request, 'profiles/friends.html', context)
