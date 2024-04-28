from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.models import Profile


@login_required(login_url='login')
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user
    context = {
        'user': user,
        'profile': profile,
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
