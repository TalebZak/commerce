# Generated by Django 3.0.3 on 2020-09-08 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200905_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%D/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('FU', 'Furniture'), ('CL', 'Clothing'), ('EN', 'Entertainment'), ('OTH', 'Other')], max_length=3),
        ),
    ]
