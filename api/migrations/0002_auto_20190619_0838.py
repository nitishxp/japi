# Generated by Django 2.2.2 on 2019-06-19 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(help_text='Name of company', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='building_number',
            field=models.CharField(help_text='Building number eg. 10/12', max_length=30),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='city',
            field=models.CharField(help_text='name of city', max_length=30),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='company',
            field=models.ForeignKey(help_text='company pk value', on_delete=django.db.models.deletion.CASCADE, to='api.Company'),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='locality',
            field=models.CharField(help_text='Locality', max_length=30),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='postal_code',
            field=models.IntegerField(help_text='6 Digit postal code'),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='state',
            field=models.CharField(help_text='name of state', max_length=30),
        ),
    ]
