# Generated by Django 4.2.4 on 2023-08-08 08:19

from django.db import migrations, models
import rent_car.models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_car', '0010_alter_reservation_pickup_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='return_date',
            field=models.DateTimeField(blank=True, default=rent_car.models.return_date, null=True),
        ),
    ]
