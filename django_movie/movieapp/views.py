from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# Create your views here.
def base(request):
    name = '영화'
    return render(request, 'movieapp/index.html')