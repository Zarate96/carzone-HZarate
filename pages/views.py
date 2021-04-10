from django.shortcuts import render
from .models import Team
from cars.models import Car

# Create your views here.

def home(request):
    teams = Team.objects.all()
    cars = Car.objects.order_by('-created_date')
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    context = {
        'teams': teams,
        'featured_cars': featured_cars,
        'cars': cars,
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

def contact(request):
    return render(request, 'pages/contact.html')