from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# Create your views here.
def base(request):
    name = '영화'
    return render(request, 'movieapp/index.html')

def contact(request):
    name = '영화'
    return render(request, 'movieapp/contact.html')

def about(request):
    name = '영화'
    return render(request, 'movieapp/about.html')

def services(request):
    name = '영화'
    return render(request, 'movieapp/services.html')

def works(request):
    name = '영화'
    return render(request, 'movieapp/works.html')

def work_single(request):
    name = '영화'
    return render(request, 'movieapp/work-single.html')