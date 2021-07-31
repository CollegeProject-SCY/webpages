# Generated by Django 3.2.5 on 2021-07-21 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_contact_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_place', models.CharField(max_length=255)),
                ('To_place', models.CharField(max_length=255)),
                ('Timings', models.CharField(max_length=255)),
                ('Bus_Number', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Route list',
                'db_table': 'route_table',
            },
        ),
    ]