from django.conf import settings
from django.shortcuts import render, redirect
from .models import Team
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .decorators import check_recaptcha


# Create your views here.

def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    cars = Car.objects.order_by('-created_date')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    context = {
        'teams': teams,
        'featured_cars': featured_cars,
        'cars': cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    teams = Team.objects.all()
    context = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', context)

def services(request):
    return render(request, 'pages/services.html')

@check_recaptcha
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        if request.recaptcha_is_valid:
            email_subject = 'You have a new message from Carzone website regarding ' + subject
            message_body = 'Name: ' + name + '. Email: ' + email + '. Phone: ' + phone + '. Message: ' + message

            admin_info = User.objects.get(is_superuser=True)
            admin_email = admin_info.email
            send_mail(
                email_subject,
                message_body,
                settings.EMAIL_HOST,
                [admin_email],
                fail_silently=False,
            )
            messages.success(request, 'Gracias por ponerte en contacto con nosotros. Te responderemos en breve')
            return redirect('contact')
        else: 
            messages.error(request, 'Porfavor verifique la información')

    return render(request, 'pages/contact.html')