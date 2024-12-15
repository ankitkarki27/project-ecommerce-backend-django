from django.shortcuts import render

# Create your views here.
def index(request):
    context={}
    return render(request,"index.html",context)

def cart(request):
    context={}
    return render(request,"cart.html",context)
    