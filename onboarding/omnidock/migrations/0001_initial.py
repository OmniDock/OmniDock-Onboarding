# Generated by Django 5.0.6 on 2024-06-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OmnidockOrder',
            fields=[
                ('marketplace_order_id', models.CharField(max_length=100)),
                ('omnidock_order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField()),
                ('fulfillment_status', models.CharField(max_length=100)),
                ('shipping_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OmnidockProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('product_title', models.CharField(max_length=255)),
                ('gross_income', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('units_sold', models.IntegerField(default=0)),
            ],
        ),
    ]