from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


def loginpage(request):
    errors = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            auth_user = User.objects.get(email=email)
            user = authenticate(request, username=auth_user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                errors['login_error'] = "Incorrect password"
                return render(request, 'auth/loginpage.html', {'errors': errors})

        except User.DoesNotExist:
            errors['login_error'] = "Email does not exist"
            return render(request, 'auth/loginpage.html', {'errors': errors})

    return render(request, 'auth/loginpage.html')

   

def register(request):
    errors = {}
    if request.method =='POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username:
            errors['username'] = "username is required"
       
        if not first_name:
            errors['first_name'] = "first name is required"
        
        if not last_name:
            errors['last_name'] = "lastname is required"
        
        if not email:
            errors['email'] = "email is required"


        if password != confirm_password:
            errors['confirm_password']= "password didnot match"

        if not password:
            errors['password'] = "password is require"

        if not confirm_password:
            errors['confirm_password'] = "confirmpassword is required"

        if not errors:
            user = User.objects.create_user(
                username= username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password
            )
            user.save()
            return redirect('login')
        else:
            errors['errors'] = "failed to login"
            return render(request, 'auth/register.html',{'errors':errors})
    return render(request, 'auth/register.html')

def hospindex(request):
    return render(request, 'auth/hospindex.html')