# Generated by Django 2.1.4 on 2019-01-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_services_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]