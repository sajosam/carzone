import django
from django.core.checks import messages
from contacts.models import Contact
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
# Create your views here.


def inquiry(request):
    if request.method == 'POST':
        car_id=request.POST['car_id']
        car_title=request.POST['car_title']
        user_id=request.POST['user_id']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        customer_need=request.POST['customer_need']
        city=request.POST['city']
        state=request.POST['state']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']

        if request .user.is_authenticated:
            user_id=request.user.id
            has_contacted=Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'you have already made enquiry about this car, please until we get back you')
                return redirect('/cars/'+car_id)
                

        admin_info = User.objects.get(is_superuser= True)
        admin_email = admin_info.email
        contact=Contact(car_id=car_id, car_title=car_title, user_id=user_id, first_name=first_name, last_name=last_name, customer_need=customer_need, city=city, state=state, email=email, phone=phone, message=message)
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
                'New Car Inquiry',
                'You have a new inquiry for the car ' + car_title + '. Please login to your admin panel for more info.',
                'anjubinu866@gmail.com',
                [admin_email],
                fail_silently=False,
            )
        contact.save()

        messages.success(request, 'thank you, your request has been submitted, we will get back you soon')
        return redirect('/cars/'+car_id)