# Generated by Django 4.2.4 on 2023-09-30 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_companyaccount_id_alter_companyaccount_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rake',
            name='destination',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rake',
            name='source',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]