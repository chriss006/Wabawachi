# Generated by Django 4.1.3 on 2022-11-15 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wineceller", "0002_wine_alter_wineceller_wine"),
        ("winesearch", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="Wine",),
    ]
