from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Bear

class BearCreate(CreateView):
    model = Bear
    fields = '__all__'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def bears_index(request):
    bears = Bear.objects.all()
    return render(request, 'bears/index.html', {'bears': bears})

def bears_detail(request, bear_id):
    bear = Bear.objects.get(id=bear_id)
    return render(request, 'bears/detail.html', {'bear': bear})
