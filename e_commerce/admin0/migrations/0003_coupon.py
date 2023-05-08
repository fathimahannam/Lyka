# Generated by Django 4.1.6 on 2023-04-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin0', '0002_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('min_amount', models.PositiveBigIntegerField(default=15000)),
                ('discount_price', models.PositiveBigIntegerField(default=799)),
                ('is_expired', models.BooleanField(default=False)),
            ],
        ),
    ]