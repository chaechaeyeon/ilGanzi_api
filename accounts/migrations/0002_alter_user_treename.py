# Generated by Django 4.2.7 on 2023-11-04 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='treename',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]