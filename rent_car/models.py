from datetime import date, timedelta, datetime

from django.db import models
from django_countries.fields import CountryField
from smart_selects.db_fields import ChainedForeignKey


# Create your models here
class OfficeLocation(models.Model):
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=250)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = CountryField()
    zip = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.address


class TypeRate(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('semi-automatic', 'Semi-Automatic'),
    ]
    type = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    price_per_day = models.IntegerField()
    price_per_hour = models.IntegerField()
    num_of_passenger = models.IntegerField()
    piece_of_bag = models.IntegerField()
    limit_mileage = models.IntegerField()
    num_of_door = models.IntegerField()
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)

    def __str__(self):
        return self.type


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50)
    current_mileage = models.IntegerField()
    office_location = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE)
    type_and_rate = models.ForeignKey(TypeRate, on_delete=models.CASCADE, related_name='type_rate')

    def __str__(self):
        return f'{self.make} {self.model} - {self.registration_number}'


def return_date():
    return datetime.today() + timedelta(days=1)


class Reservation(models.Model):
    PICKUP_CHOICES = (
        ('Card', 'Card'),
        ('Cash', 'Cash'),
    )
    pickup_date = models.DateTimeField(default=datetime.today, blank=True, null=True)
    return_date = models.DateTimeField(default=return_date, blank=True, null=True)
    payment = models.CharField(max_length=10, choices=PICKUP_CHOICES, blank=True, null=True)
    pickup_location = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, related_name='pickup_location')
    return_location = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, related_name='return_location')
    type_and_rate = models.ForeignKey(TypeRate, on_delete=models.CASCADE)
    car = ChainedForeignKey(
        Car,
        chained_field="type_and_rate",
        chained_model_field="type_and_rate",
        show_all=False,
        auto_choose=True,
        sort=True,
    )


class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return self.name


class Extra(models.Model):
    PICKUP_CHOICES = (
        ('Per reservation', 'Per reservation'),
        ('Per day', 'Per day'),
    )
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    price_type = models.CharField(max_length=250, choices=PICKUP_CHOICES, null=True)

    def __str__(self):
        return self.name


def default_return_date():
    return date.today() + timedelta(days=7)


class Availability(models.Model):
    pickup_date = models.DateField(default=date.today)
    return_date = models.DateField(default=default_return_date)
    type_and_rate = models.ForeignKey(TypeRate, on_delete=models.CASCADE)
    car = ChainedForeignKey(
        Car,
        chained_field="type_and_rate",
        chained_model_field="type_and_rate",
        show_all=False,
        auto_choose=True,
        sort=True
    )
