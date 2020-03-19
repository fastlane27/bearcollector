import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Bear, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'bearcollector'

class BearCreate(LoginRequiredMixin, CreateView):
    model = Bear
    fields = ['name', 'species', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BearUpdate(LoginRequiredMixin, UpdateView):
    model = Bear
    fields = ['species', 'description', 'age']

class BearDelete(LoginRequiredMixin, DeleteView):
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

@login_required
def bears_index(request):
    bears = Bear.objects.filter(user=request.user)
    return render(request, 'bears/index.html', {'bears': bears})

@login_required
def bears_detail(request, bear_id):
    bear = Bear.objects.get(id=bear_id)
    toys_bear_doesnt_have = Toy.objects.exclude(id__in=bear.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'bears/detail.html', {
        'bear': bear,
        'feeding_form': feeding_form,
        'toys': toys_bear_doesnt_have
    })

@login_required
def add_feeding(request, bear_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.bear_id = bear_id
        new_feeding.save()
    return redirect('bears_detail', bear_id=bear_id)

@login_required
def delete_feeding(request, bear_id, feeding_id):
    Bear.objects.get(id=bear_id).feeding_set.get(id=feeding_id).delete()
    return redirect('bears_detail', bear_id=bear_id)

@login_required
def add_photo(request, bear_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, bear_id=bear_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('bears_detail', bear_id=bear_id)

@login_required
def delete_photo(request, bear_id, photo_id):
    Bear.objects.get(id=bear_id).photo_set.get(id=photo_id).delete()
    return redirect('bears_detail', bear_id=bear_id)

@login_required
def assoc_toy(request, bear_id, toy_id):
    Bear.objects.get(id=bear_id).toys.add(toy_id)
    return redirect('bears_detail', bear_id=bear_id)

@login_required
def unassoc_toy(request, bear_id, toy_id):
    Bear.objects.get(id=bear_id).toys.remove(toy_id)
    return redirect('bears_detail', bear_id=bear_id)

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
