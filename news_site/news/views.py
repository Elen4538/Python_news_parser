from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
#from django.views.generic.base import TemplateView

from .models import *

menu = [{'title': "Main_info", 'url_name': 'common'},
        {'title': "TJ", 'url_name': 'tj'},
        {'title': "VC", 'url_name': 'vc'},
        {'title': "Habr", 'url_name': 'habr'},
        {'title': "Logout", 'url_name': 'logout'}
        ]

def main_page(request):
    context_main = {
        'title': 'Login_page',       
    }
    return render(request, 'news/main.html', context=context_main) 


def common(request):

    context = {
        'title': 'Common page',
        'menu': menu,
    }
    return render(request,'news/common.html', context=context)


def tj(request):
    context_tj = {
        'title':'TJ_news',
        'menu': menu,
    }
    return render(request,'news/tj.html', context=context_tj)

   
def vc(request):
    context_vc = {
        'title':'VC_news',
        'menu': menu,        
    }
    return render(request,'news/vc.html', context=context_vc)
    

def habr(request):
    context_habr = {
        'title':'Habr_news',
        'menu': menu,       
    }
    return render(request,'news/habr.html', context=context_habr)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class Login_User(TemplateView):
    template_name = 'news/login_page.html'

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("common/")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)

class RegisterAccount(TemplateView):
    template_name = 'news/register_acc.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User.objects.create_user(username, email, password)
                return redirect(reverse("login"))

        return render(request, self.template_name)

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")



    



