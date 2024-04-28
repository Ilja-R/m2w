from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from authentication.forms import EmailUserCreationForm


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('my-profile')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('my-profile')
        else:
            messages.error(request, 'Invalid login credentials')

    context = {'page': page}
    return render(request, 'authentication/login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def register_user(request):
    page = 'register'
    form = EmailUserCreationForm()
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, form.errors)
    return render(request, 'authentication/register.html', {'page': page, 'form': form})
