# Generated by Django 4.0.5 on 2022-06-28 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorteam',
            name='name',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
