# Generated by Django 3.0.3 on 2020-09-08 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='images/no-image.png', null=True, upload_to='images/%Y/%m/%D/'),
        ),
    ]
