# Generated by Django 4.2.4 on 2023-08-02 10:41

from django.db import migrations, models
import rent_car.models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_car', '0008_alter_availability_pickup_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='return_date',
            field=models.DateField(default=rent_car.models.default_return_date),
        ),
    ]