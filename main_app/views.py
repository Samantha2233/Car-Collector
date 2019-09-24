from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import uuid
import boto3
from .models import Car, Agreement, Photo, AirFreshener
from .forms import AgreementForm

S3_BASE_URL='https://s3.us-east-1.amazonaws.com/'
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
    unhad_air_fresheners = AirFreshener.objects.exclude(id__in = car.air_fresheners.all().values_list('id'))
    agreement_form = AgreementForm()
    return render(request, 'cars/detail.html', {
        'car': car,
        'agreement_form': agreement_form,
        'air_fresheners': unhad_air_fresheners
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
    fields = ['purchase_date', 'make', 'model', 'year', 'vehicle_cost', 'reg_and_tax', 'repair_and_init_expense']
    success_url = '/cars/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CarUpdate(UpdateView):
    model = Car
    fields = ['purchase_date', 'make', 'model', 'year', 'vehicle_cost', 'reg_and_tax', 'repair_and_init_expense']


class CarDelete(DeleteView):
    model = Car
    success_url = '/cars/'


def add_photo(request, car_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to car_id or car (if you have a car object)
            photo = Photo(url=url, car_id=car_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', car_id=car_id)



def assoc_air_freshener(request, car_id, air_freshener_id):
    Car.objects.get(id=car_id).air_fresheners.add(air_freshener_id)
    return redirect('detail', car_id=car_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cars')
        else:
            error_message = 'Invalid sign up - try agian'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)