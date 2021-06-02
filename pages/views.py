from django.core.checks import messages
from django.db.models.expressions import F
from cars import models
from cars.models import Car
from django.shortcuts import redirect, render
from .models import Team
# Create your views here.
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages



def home(request):
    teams=Team.objects.all()
    featured_cars=Car.objects.order_by('-created_date').filter(is_featured=True)
    all_cars=Car.objects.order_by('-created_date')
    model_search=Car.objects.values_list('model', flat=True).distinct()
    city_search=Car.objects.values_list('city', flat=True).distinct()
    year_search=Car.objects.values_list('year', flat=True).distinct()
    body_style_search=Car.objects.values_list('body_style', flat=True).distinct()


    data={
        'teams':teams,
        'featured_cars':featured_cars,
        'all_cars':all_cars,
        'model_search':model_search,
        'city_search':city_search,
        'year_search':year_search,
        'body_style_search':body_style_search,


    }
    return render(request, 'pages/home.html', data)

def about(request):
    teams=Team.objects.all()
    data={
        'teams':teams,

    }
    return render(request, 'pages/about.html', data)


def services(request):
    return render(request, 'pages/services.html')

    
def contact(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        phone=request.POST['phone']
        message=request.POST['message']
        messsage_body='Name '+name + '. Email'+email + '.Phone: '+ phone + '.Message: ' +message
        email_subject='you have a new message from the carzone website'+subject
        admin_info = User.objects.get(is_superuser= True)
        admin_email = admin_info.email

        send_mail(
                email_subject,
                messsage_body,
                'anjubinu866@gmail.com',
                [admin_email],
                fail_silently=False,
            )
        messages.success(request, 'thank you for contacting us')
        return redirect('contact')

    return render(request, 'pages/contact.html')