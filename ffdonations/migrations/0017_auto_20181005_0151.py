# Generated by Django 2.1.2 on 2018-10-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ffdonations', '0016_auto_20181005_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationmodel',
            name='displayName',
            field=models.CharField(default='', max_length=8192, verbose_name='Donor Name'),
        ),
    ]
