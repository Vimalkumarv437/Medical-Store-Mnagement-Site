# Generated by Django 4.2 on 2024-10-23 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0004_remove_medicine_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='medicalapp.customer'),
        ),
    ]
