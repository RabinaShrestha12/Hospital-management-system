from django.urls import path
from .view.auth_views import hospindex, loginpage, register


urlpatterns = [
    path('hospindex/', hospindex, name='hospindex'),
    path('login/', loginpage, name='login'),
    path('register/', register, name='register')
     
]
