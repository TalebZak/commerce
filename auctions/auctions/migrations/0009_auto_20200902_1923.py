# Generated by Django 3.0.3 on 2020-09-02 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='id',
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]