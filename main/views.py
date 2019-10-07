from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .forms import loginForm, registerForm
from .models import User

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.password == password:
                    return redirect('/')
                else: # password is not valid
                    # https://docs.djangoproject.com/en/2.2/ref/forms/api/#django.forms.Form.add_error
                    # form.add_error(field,error) 如果field为None, error就会添加到form.non_field_errors
                    # 显示的时候就不会与某一个具体的字段(field)关联
                    form.add_error( None, "用户名或密码不正确.")
                    return render(request, 'main/login.html', {'form': form })
            except ObjectDoesNotExist:
                # user does not exist, redirect user to register
                return redirect('/register')
        else: # input is not valid, form will carry form.errors to display
            return render(request, 'main/login.html', {'form':form})
    else:
        form = loginForm()
        return render(request, 'main/login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user=User(username=username, email=email, password=password)
            user.save()
            return redirect('/')
        else:
            return render(request, 'main/register.html',{'form':form})
    else:
        form = registerForm()
        return render(request, 'main/register.html', {'form': form})


def index(request):
    return HttpResponse("Welcome to the homepage!")
