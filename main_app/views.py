from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Car
from .forms import AgreementForm


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cars_index(request):
    cars = Car.objects.all()
    return render(request, 'cars/index.html', {'cars': cars})

def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    agreement_form = AgreementForm()
    return render(request, 'cars/detail.html', {
        'car': car,
        'agreement_form': agreement_form
        })

def add_agreement(request, car_id):
    form = AgreementForm(request.POST)
    if form.is_valid():
        new_agreement = form.save(commit=False)
        new_agreement.car_id = car_id
        new_agreement.save()
    return redirect('detail', car_id=car_id)

class CarCreate(CreateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'

class CarUpdate(UpdateView):
    model = Car
    fields = '__all__'

class CarDelete(DeleteView):
    model = Car
    success_url = '/cars/'