
from django.urls import path

from .views import *

urlpatterns = [
    path('', main_page, name ='home'),
    path('login/', Login_User.as_view(), name="login_page"),
    path('acc_register/', RegisterAccount.as_view(), name = 'register'),
    path('logout/', logout_request, name= "logout"),
    path('common/', common, name='common'),
    path('common/tj/', tj, name='tj'),
    path('common/vc/', vc, name='vc'),
    path('common/habr/', habr, name='habr'),
]