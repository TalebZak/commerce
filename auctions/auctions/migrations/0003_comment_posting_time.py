# Generated by Django 3.0.3 on 2020-08-31 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_comment_product_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='posting_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
