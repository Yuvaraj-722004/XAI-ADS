from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render,redirect
from django.contrib import messages
import urllib.request
import urllib.parse
from django.conf import settings
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Assuming you have a User model defined



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def udashboard(request):
    return render(request, 'udashboard.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def alogin(req):
    if req.method == 'POST':
        username = req.POST.get('adminUsername')
        password = req.POST.get('adminPassword')
        print("hello")
        print(username,password)
        # Check if the provided credentials match
        if username == 'admin' and password   == 'admin':
            messages.success(req, 'You are logged in.')
            return redirect('dashboard')  # Redirect to the admin dashboard page
        else:
            messages.error(req, 'You are trying to log in with wrong details.')
            return redirect('alogin')  # Redirect to the login page (named 'admin' here)

    # Render the login page if the request method is GET
    return render(req, 'alogin.html')



def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        age = request.POST.get('age')
        address = request.POST.get('address')

        profile_picture = request.FILES.get('profile_picture')  # Handle file upload

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        user = User(name=name, mobile=mobile, email=email, password=password, age=age, address=address)

        if profile_picture:
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            user.profile_picture = filename

        user.save()

        messages.success(request, 'Registration successful! Please login.')
        return redirect('ulogin')

    return render(request, 'register.html')




def ulogin(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Get the username or email
        password = request.POST.get('password')  # Get the password

        # Check if the user exists and the password is correct
        try:
            user = User.objects.get(email=email)
            if user.password == password:  # Be cautious about plain text password comparison
                # Log the user in (you may want to set a session or token here)
                request.session['user_id'] = user.id  # Store user ID in session
                messages.success(request, 'Login successful!')
                return redirect('udashboard')  # Redirect to the index page or desired page
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'ulogin.html')