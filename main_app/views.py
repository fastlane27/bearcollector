from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Bear, Toy
from .forms import FeedingForm

class BearCreate(CreateView):
    model = Bear
    fields = ['name', 'species', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bears_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def bears_index(request):
    bears = Bear.objects.all()
    return render(request, 'bears/index.html', {'bears': bears})

def bears_detail(request, bear_id):
    bear = Bear.objects.get(id=bear_id)
    toys_bear_doesnt_have = Toy.objects.exclude(id__in=bear.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'bears/detail.html', {
        'bear': bear,
        'feeding_form': feeding_form,
        'toys': toys_bear_doesnt_have
    })

def add_feeding(request, bear_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.bear_id = bear_id
        new_feeding.save()
    return redirect('bears_detail', bear_id=bear_id)

def delete_feeding(request, bear_id, feeding_id):
    Bear.objects.get(id=bear_id).feeding_set.get(id=feeding_id).delete()
    return redirect('bears_detail', bear_id=bear_id)

def assoc_toy(request, bear_id, toy_id):
    Bear.objects.get(id=bear_id).toys.add(toy_id)
    return redirect('bears_detail', bear_id=bear_id)

def unassoc_toy(request, bear_id, toy_id):
    Bear.objects.get(id=bear_id).toys.remove(toy_id)
    return redirect('bears_detail', bear_id=bear_id)

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
