from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
from .models import Car, Agreement, Photo
from .forms import AgreementForm

S3_BASE_URL='s3.amazonaws.com/'
BUCKET='carcollector-amerimex'

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
    print(form)
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


def add_photo(request, car_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
             s3.upload_fileobj(photo_file, BUCKET, key)
             url = f"{S3_BASE_URL}{BUCKET}/{key}"
             photo = Photo(url=url, car_id=car_id)
             photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('detail', car_id=car_id)