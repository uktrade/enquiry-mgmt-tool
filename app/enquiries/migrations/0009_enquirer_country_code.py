# Generated by Django 3.0.3 on 2020-04-01 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiries', '0008_merge_20200401_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquirer',
            name='country_code',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Country code'),
        ),
    ]
