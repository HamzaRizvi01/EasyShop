# Generated by Django 4.0.4 on 2022-06-26 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_product_sentiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sentiment',
            field=models.CharField(default='NULL', max_length=10),
        ),
    ]
