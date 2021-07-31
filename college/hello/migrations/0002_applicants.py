# Generated by Django 3.2.5 on 2021-07-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='applicants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_no', models.CharField(max_length=50)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('student_name', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('father_name', models.CharField(max_length=30)),
                ('mother_name', models.CharField(max_length=30)),
                ('caste', models.CharField(max_length=30)),
                ('rd_number', models.CharField(max_length=10)),
                ('institute_type', models.CharField(max_length=20)),
                ('institute_name', models.CharField(max_length=100)),
                ('institute_address', models.CharField(max_length=255)),
                ('inst_street_address1', models.CharField(max_length=255)),
                ('inst_street_address2', models.CharField(max_length=255)),
                ('inst_city', models.CharField(max_length=20)),
                ('inst_state', models.CharField(max_length=20)),
                ('inst_postal_code', models.IntegerField()),
                ('student_address', models.CharField(max_length=255)),
                ('stud_street_address1', models.CharField(max_length=255)),
                ('stud_street_address2', models.CharField(max_length=255)),
                ('stud_city', models.CharField(max_length=20)),
                ('stud_state', models.CharField(max_length=20)),
                ('stud_postal_code', models.IntegerField()),
                ('course', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=10)),
                ('semester', models.CharField(max_length=20)),
                ('adhar_number', models.CharField(max_length=12)),
                ('college_fee_amt', models.CharField(max_length=10)),
                ('from_stop', models.CharField(max_length=50)),
                ('to_stop', models.CharField(max_length=50)),
                ('via_1', models.CharField(max_length=50)),
                ('passport_size_image', models.ImageField(upload_to='photos')),
                ('college_fees_image', models.ImageField(upload_to='photos')),
                ('adhar_image', models.ImageField(upload_to='photos')),
                ('study_certificate_image', models.ImageField(upload_to='photos')),
                ('previous_marks_image', models.ImageField(upload_to='photos')),
                ('terms_cond', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Application List',
                'db_table': 'application_db',
            },
        ),
    ]