# Generated by Django 3.2.5 on 2021-07-25 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0015_account_pass_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pass_id',
            field=models.CharField(default=0, editable=False, max_length=6, unique=True),
        ),
    ]