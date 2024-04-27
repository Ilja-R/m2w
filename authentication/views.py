from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from authentication.forms import EmailUserCreationForm
from common.logger import Logger

logger = Logger(__name__)


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"User with email {user.username} logged in successfully.")
            return redirect('index')
        else:
            messages.error(request, 'Invalid login credentials')

    context = {'page': page}
    return render(request, 'authentication/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')


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
            logger.info(f"User with email {user.username} registered successfully.")
            return redirect('index')
        else:
            messages.error(request, form.errors)
    return render(request, 'authentication/register.html', {'page': page, 'form': form})

# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Log the user in after registration
#             login(request, user)
#             # Redirect to a success page or home page
#             return redirect('success_page')  # Replace 'success_page' with the name of your success page URL pattern
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})
