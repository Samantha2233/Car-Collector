from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


TERMS = (
    ('W', 'Weekly (7 Days)'),
    ('BW', 'Bi-Weekly (14 Days)'),
    ('M', 'Monthly (30 Days)'),
    ('BM', 'Bi-Monthly (60 Days)'),
)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField('Mobile Phone Number')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    license_num = models.CharField('Driver''s License No.', max_length=100)
    l_state = models.CharField('License: State', max_length=100)
    l_country = models.CharField('License: Country', max_length=100)
    l_zip = models.CharField('License: Zip Code', max_length=100)
    birth = models.DateField('Birth Date')
    

    def __str__(self):
        return f'{self.name}'



class AirFreshener(models.Model):
    scent = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.scent}'

# Create your models here.
class Car(models.Model):
    purchase_date = models.DateField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vehicle_cost = models.IntegerField()
    reg_and_tax = models.IntegerField()
    repair_and_init_expense = models.IntegerField()

    customers = models.ManyToManyField(Customer)
    air_fresheners = models.ManyToManyField(AirFreshener)


    def __str__(self):
        return f'{self.make} {self.model} {self.year} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})


class Agreement(models.Model):
    agreement_num = models.IntegerField('Agreement No.')
    unit_num = models.IntegerField('Unit No.')
    vin = models.CharField('VIN', max_length=17)
    license_num = models.CharField('License No.', max_length=25)
    mileage_out = models.IntegerField()
    condition = models.TextField('Condition of Car', max_length=250)
    date = models.DateField()
    term = models.CharField(
        max_length=2,
        choices=TERMS,
        default=TERMS[2][0]
    )
    payment_freq = models.CharField(
        'Payment Frequency',
        max_length=2,
        choices=TERMS,
        default=TERMS[2][0],
    )

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.get_term_display()} for Agreement Number: {self.agreement_num}'

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for car_id:{self.car_id} @{self.url}"

