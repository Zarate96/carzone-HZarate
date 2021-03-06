from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from contacts.models import Contact
from .decorators import check_recaptcha

# Create your views here.
@check_recaptcha
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if request.recaptcha_is_valid:
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Ingreso correcto')
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciales no validas')
                return redirect('login')
        else: 
            messages.error(request, 'Porfavor verifique la información')
        
    return render(request, 'accounts/login.html')

@check_recaptcha
def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Usuario ya registrado!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Este email ya existe!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    auth.login(request, user)
                    messages.success(request, 'Inicio de session exitoso.')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request, 'Registrado exitosamente.')
                    return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    count = Contact.objects.order_by('-create_date').filter(user_id=request.user.id).count()

    context = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'Cierre de sesión exitoso')
        return redirect('home')
    return redirect('home')