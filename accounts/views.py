from contacts.models import Contact
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username already exist')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already exists')
                    return redirect('register')
                else:
                    user=User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                    auth.login(request, user)
                    messages.success(request, 'you are logged in')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request, 'you are registered successfully')
                    return redirect('login')
        else:
            messages.error(request, 'password doesnot match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')
@login_required(login_url='login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-created_date').filter(user_id=request.user.id)
    # count = Contact.objects.order_by('-create_date').filter(user_id=request.user.id).count()

    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)
    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are successfully logged out')
        return redirect('home')
    return redirect('home')
    