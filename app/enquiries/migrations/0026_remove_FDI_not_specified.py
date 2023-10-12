from django.db import migrations, models

def set_not_specified_to_default(apps, schema_editor):
    Enquiry = apps.get_model('enquiries', 'Enquiry')
    Enquiry.objects.filter(investment_type='NOT_SPECIFIED').update(investment_type='DEFAULT')

class Migration(migrations.Migration):

    dependencies = [
        ('enquiries', '0025_auto_20230622_1559'),
    ]

    operations = [
        migrations.RunPython(set_not_specified_to_default, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='enquiry',
            name='investment_type',
            field=models.CharField(choices=[('DEFAULT', '----'), ('ACQUISITION', 'Acquisition'), ('CAPITAL_ONLY', 'Capital only'), ('NEW_SITE', 'Creation of new site or activity'), ('EXPANSION', 'Expansion of existing site or activity'), ('JOINT_VENTURE', 'Joint venture'), ('MERGER', 'Merger'), ('RETENTION', 'Retention')], default='DEFAULT', max_length=255, verbose_name='Investment type'),
        ),
    ]
