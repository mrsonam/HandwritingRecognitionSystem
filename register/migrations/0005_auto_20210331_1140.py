# Generated by Django 3.1.7 on 2021-03-31 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_inputpic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputpic',
            name='image',
            field=models.ImageField(upload_to='form'),
        ),
    ]