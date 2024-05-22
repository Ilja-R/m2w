from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from profiles.forms import ProfileForm, FriendSearchForm
from profiles.models import Profile, Relationship


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
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            new_friend = Profile.objects.get(email=email)
            if new_friend == Profile.objects.get(user=request.user):
                messages.error(request, 'You cannot add yourself as a friend')
                return redirect('friends')
            user = Profile.objects.get(user=request.user)
            if new_friend.user in user.friends.all():
                messages.error(request, 'User is already your friend')
                return redirect('friends')
            relationship = Relationship.objects.create(sender=user, receiver=new_friend)
            relationship.save()
            messages.info(request, f'Friend request sent to user {email}')
        except Profile.DoesNotExist:
            messages.error(request, 'User does not exist')
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()

    form = FriendSearchForm()

    outgoing_requests = Relationship.objects.filter(sender=profile, status='send')
    # outgoing_requests = Relationship.objects.get(sender=profile, status='send')
    incoming_requests = Relationship.objects.filter(receiver=profile, status='send')

    context = {
        'friends': friends,
        'outgoing_requests': outgoing_requests,
        'incoming_requests': incoming_requests,
        'form': form,
    }
    return render(request, 'profiles/friends.html', context)


@login_required(login_url='login')
def delete_request(request, pk):
    request = Relationship.objects.get(id=pk)
    request.delete()
    return redirect('friends')


@login_required(login_url='login')
def accept_request(request, pk):
    request = Relationship.objects.get(id=pk)
    request.status = 'accepted'
    request.save()
    return redirect('friends')

@login_required(login_url='login')
def delete_friend(request, pk):
    friend = Profile.objects.get(id=pk)
    user = Profile.objects.get(user=request.user)
    user.friends.remove(friend.user)
    friend.friends.remove(user.user)
    relationship = Relationship.objects.filter(
        Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user)
    ).first()

    if relationship:
        relationship.delete()
    user.save()
    friend.save()
    return redirect('friends')