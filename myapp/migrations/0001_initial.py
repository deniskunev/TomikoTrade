# Generated by Django 5.1.4 on 2025-01-16 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='vehicles/')),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('mileage', models.IntegerField()),
                ('engine_volume', models.FloatField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transmission', models.CharField(choices=[('M', 'Manual'), ('A', 'Automatic')], max_length=1)),
                ('drive_type', models.CharField(choices=[('R', 'Rear'), ('F', 'Front'), ('A', 'All-wheel')], max_length=1)),
                ('color', models.CharField(max_length=50)),
            ],
        ),
    ]
