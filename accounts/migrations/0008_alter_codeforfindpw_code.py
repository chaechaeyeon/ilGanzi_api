# Generated by Django 4.2.7 on 2023-11-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_codeforfindpw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeforfindpw',
            name='code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
