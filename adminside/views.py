from django.shortcuts import get_object_or_404, render

from .models import Hotel, Package


def home(request):
    return render(request, 'pages/index.html')


def packages(request):
    package_list = Package.objects.filter(active=True).order_by("-created_at")
    return render(request, 'pages/packages.html', {"packages": package_list})


def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug, active=True)
    return render(request, 'pages/package-detail.html', {"package": package})


def hotels(request):
    hotel_list = Hotel.objects.filter(active=True).order_by("-created_at")
    return render(request, 'pages/hotels.html', {"hotels": hotel_list})


def about(request):
    return render(request, 'pages/aboutus.html')


def contact(request):
    return render(request, 'pages/contact.html')
