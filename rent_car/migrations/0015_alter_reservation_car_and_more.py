# Generated by Django 4.2.4 on 2023-08-08 13:34

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('rent_car', '0014_alter_reservation_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='car',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='type_and_rate', chained_model_field='type_and_rate', default=2, on_delete=django.db.models.deletion.CASCADE, to='rent_car.car'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='type_and_rate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_car.typerate'),
        ),
    ]