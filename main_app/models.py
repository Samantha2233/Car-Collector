from django.db import models
from django.urls import reverse

TERMS = (
    ('W', 'Weekly (7 Days)'),
    ('BW', 'Bi-Weekly (14 Days)'),
    ('M', 'Monthly (30 Days)'),
    ('BM', 'Bi-Monthly (60 Days)'),
)

# Create your models here.
class Car(models.Model):
    purchase_date = models.DateField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vehicle_cost = models.IntegerField()
    reg_and_tax = models.IntegerField()
    repair_and_init_expense = models.IntegerField()

    def __str__(self):
        return f'{self.make} {self.model} {self.year} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat-id': self.id})


class Agreement(models.Model):
    agreement_num = models.IntegerField()
    unit_num = models.IntegerField()
    vin = models.CharField(max_length=17)
    license_num = models.CharField(max_length=25)
    mileage_out = models.IntegerField()
    condition = models.TextField(max_length=250)
    date = models.DateField()
    term = models.CharField(
        max_length=2,
        choices=TERMS,
        default=TERMS[2][0]
    )
    payment_freq = models.CharField(
        max_length=2,
        choices=TERMS,
        default=TERMS[2][0]
    )

    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_term_display()} for Agreement Number: {self.agreement_num}'