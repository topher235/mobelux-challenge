# Generated by Django 3.2.4 on 2021-06-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flickrapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='is_public',
            field=models.BooleanField(verbose_name='Public?'),
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Album name'),
        ),
    ]