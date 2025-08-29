from django.urls import path
from .view.main_views import index,abouthosp,department,createdoctors,editdoctors,singledoctors,deletedoctors
from .view.auth_views import hospindex, loginpage, register


urlpatterns = [
    path('hospindex/', hospindex, name='hospindex'),
    path('login/', loginpage, name='login'),
    path('register/', register, name='register'),
    path('about/', abouthosp, name='about'),
    path('department/', department, name='department'),
    path('doctor/', createdoctors, name='doctor'),
    path('doctor/<int:id>', editdoctors, name= 'doctor'),
    path('doctor/<int:id>', deletedoctors, name= 'doctor'),
    path('doctor/<int:id>', singledoctors, name= 'doctor')

]
