# Generated by Django 3.0.8 on 2020-07-29 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
