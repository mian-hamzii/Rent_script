# Generated by Django 4.2.4 on 2023-08-08 13:03

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('rent_car', '0013_alter_reservation_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='car',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='type_and_rate', chained_model_field='type_and_rate', null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_car.car'),
        ),
    ]
