# Generated by Django 3.0.5 on 2020-05-13 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=20, unique=True)),
                ('brand', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Car',
            },
        ),
    ]
