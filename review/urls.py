from django.urls import path
from .views import create,login,logout,homepage,add_service_form
from .views import myservice,admin_login,auth,main
from .views import myservice,admin_login,auth,admin_home, add_category
from .views import service_category, service_question, delete_category
from .views import search,review,category_review
from .views import reject_service,accept_service,get_question

urlpatterns = [
    path('',main),
    path('create',create),
    path('login',login),
    path('homepage',homepage),
    path('logout',logout),
    path('add_service_form',add_service_form),
    path('myservice/<int:id>',myservice),
    path('admin_login',admin_login),
    path('auth',auth),
    path('admin_home', admin_home),
    path('admin_service_category', service_category),
    path('add_category', add_category),
    path('delete_category', delete_category),
    path('admin_question', service_question),
    path('search',search),
    path('accept_service', accept_service),
    path('reject_service', reject_service),
    path('review',review),
    path('add_review',category_review),
    path('get_question', get_question)
]
