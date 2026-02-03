from django.urls import path

from . import views
from users.views import contact_view

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    path('package/<slug:slug>/', views.package_detail, name='package-detail'),
    path('hotels/', views.hotels, name='hotels'),
    path('about/', views.about, name='about'),
    path('corporates/', views.corporates, name='corporates'),
    path('contact/', contact_view, name='contact'),
]
