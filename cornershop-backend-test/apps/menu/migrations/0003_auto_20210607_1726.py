# Generated by Django 3.0.8 on 2021-06-07 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20210607_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='notification_sent_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='employee',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='mealoption',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
