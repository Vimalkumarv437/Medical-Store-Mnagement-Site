# Generated by Django 4.2 on 2024-10-23 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0002_alter_customer_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stock', models.PositiveIntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicalapp.customer')),
            ],
            options={
                'ordering': ['-added_at'],
            },
        ),
    ]
