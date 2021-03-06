# Generated by Django 4.0.4 on 2022-06-08 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(choices=[('Punjab', 'Punjab'), ('Islamabad', 'ICT'), ('Sindh', 'Sindh'), ('Balochistan', 'Balochistan'), ('KPK', 'KPK')], max_length=50),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Punjab', 'Punjab'), ('Islamabad', 'ICT'), ('Sindh', 'Sindh'), ('Balochistan', 'Balochistan'), ('KPK', 'KPK')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='Sold',
            field=models.IntegerField(),
        ),
    ]
