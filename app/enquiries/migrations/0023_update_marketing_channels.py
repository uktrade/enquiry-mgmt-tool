# Generated by Django 3.1.13 on 2021-12-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiries', '0022_remove_consent_fields_from_enquirer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='marketing_channel',
            field=models.CharField(choices=[('DEFAULT', '----'), ('LINKEDIN', 'LinkedInLeadGen'), ('IIGB', 'Website'), ('IIGB_LINKEDIN', 'Website (LinkedIn)'), ('HPO', 'HPO'), ('EBOOK', 'EBOOK'), ('TRA', 'TRA'), ('OTHER', 'Other')], default='DEFAULT', max_length=255, verbose_name='Marketing channel'),
        ),
    ]
