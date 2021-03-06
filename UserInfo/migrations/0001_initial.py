# Generated by Django 3.2.8 on 2021-10-31 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LDSportInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserID', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('weekLdrunTime', models.CharField(max_length=256)),
                ('weekLdrunNum', models.CharField(max_length=256)),
                ('weekLdrunDistance', models.CharField(max_length=256)),
                ('weekLdrunPace', models.CharField(max_length=256)),
                ('termLdrunDistance', models.CharField(max_length=256)),
                ('reachLdrunTargetNum', models.CharField(max_length=256)),
                ('reachLdrunScore', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='MrSportInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserID', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('weekMrunTime', models.CharField(max_length=256)),
                ('weekMrunNum', models.CharField(max_length=256)),
                ('weekMrunDistance', models.CharField(max_length=256)),
                ('weekMrunPace', models.CharField(max_length=256)),
                ('termMrunDistance', models.CharField(max_length=256)),
                ('reachMrunTargetNum', models.CharField(max_length=256)),
                ('reachMrunScore', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=256)),
                ('token', models.CharField(max_length=256)),
            ],
        ),
    ]
