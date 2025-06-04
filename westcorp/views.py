from django.shortcuts import render,HttpResponse
def homePage(request):
    return render(request, 'westcorp/home.html')

def contact(request):
    return render(request, 'westcorp/contact.html')

def about(request):
    return render(request, 'westcorp/about.html')

# Create your views here.
