# Generated by Django 3.1 on 2021-09-07 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0005_child_childtypefee'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='invoicesub',
            field=models.IntegerField(default=0),
        ),
    ]