from django.shortcuts import render
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

class CarCreate(CreateView):
    model = Car
    fields = '__all__'
    success_url = '/cats/'

class CarUpdate(UpdateView):
    model = Car
    feilds = '__all__'

class CarDelete(DeleteView):
    model = Car
    success_url = '/cars/'