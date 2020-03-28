# Generated by Django 3.0.4 on 2020-03-26 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0003_auto_20200325_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='menuItemAdditionId',
            field=models.ManyToManyField(blank=True, related_name='orderItems', to='orders.MenuItemAddition'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='menuItemId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderItems', to='orders.MenuItem'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderId', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orderItems', to='orders.Order'),
        ),
    ]
