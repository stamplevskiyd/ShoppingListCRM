# Generated by Django 4.1.7 on 2023-02-26 21:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_rename_name_person_first_name_person_middle_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('register_date', models.DateField(default=datetime.date(2023, 2, 26), verbose_name='Дата регистрации')),
            ],
        ),
        migrations.AlterField(
            model_name='purchase',
            name='payer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shopping.user', verbose_name='Кто платил'),
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]