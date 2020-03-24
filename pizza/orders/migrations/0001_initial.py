# Generated by Django 3.0.4 on 2020-03-23 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('size', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
    ]