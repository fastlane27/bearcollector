from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bear
from .forms import FeedingForm

class BearCreate(CreateView):
    model = Bear
    fields = '__all__'

class BearUpdate(UpdateView):
    model = Bear
    fields = ['species', 'description', 'age']

class BearDelete(DeleteView):
    model = Bear
    success_url = '/bears/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def bears_index(request):
    bears = Bear.objects.all()
    return render(request, 'bears/index.html', {'bears': bears})

def bears_detail(request, bear_id):
    bear = Bear.objects.get(id=bear_id)
    feeding_form = FeedingForm()
    return render(request, 'bears/detail.html', {
        'bear': bear,
        'feeding_form': feeding_form,
    })

def add_feeding(request, bear_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.bear_id = bear_id
        new_feeding.save()
    return redirect('bears_detail', bear_id=bear_id)
