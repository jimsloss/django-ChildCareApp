# Generated by Django 3.1 on 2021-09-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_invoice_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricing',
            name='afterschool',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='eveningcare',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='fullday',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='halfday',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='latepayment',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='parttime',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='retainer',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='saturdaycreche',
            field=models.IntegerField(default=0),
        ),
    ]