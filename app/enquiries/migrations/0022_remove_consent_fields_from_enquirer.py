# Generated by Django 3.0.7 on 2021-01-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiries', '0021_enquiryactionlog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enquiry',
            options={'ordering': ['-created'], 'verbose_name_plural': 'Enquiries'},
        ),
        migrations.RemoveField(
            model_name='enquirer',
            name='email_consent',
        ),
        migrations.RemoveField(
            model_name='enquirer',
            name='phone_consent',
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquiry_stage',
            field=models.CharField(choices=[('NEW', 'New'), ('AWAITING_RESPONSE', 'Awaiting response from Investor'), ('ENGAGED', 'Engaged in dialogue'), ('NON_RESPONSIVE', 'Non-responsive'), ('NON_FDI', 'Non-FDI'), ('ADDED_TO_DATAHUB', 'Added to Data Hub'), ('SENT_TO_POST', 'Sent to Post'), ('POST_PROGRESSING', 'Post progressing'), ('NON_APPLICABLE', 'Non-applicable'), ('NURTURE_AWAITING_RESPONSE', 'Nurture awaiting response')], default='NEW', max_length=255, verbose_name='Enquiry stage'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='primary_sector',
            field=models.CharField(choices=[('DEFAULT', '----'), ('ADVANCED_ENG', 'Advanced engineering'), ('AEROSPACE', 'Aerospace'), ('AGRICULTURE', 'Agriculture, horticulture, fisheries and pets'), ('AIRPORTS', 'Airports'), ('AUTOMOTIVE', 'Automotive'), ('CHEMICALS', 'Chemicals'), ('CONSTRUCTION', 'Construction'), ('CONSUMER', 'Consumer and retail'), ('CREATIVE', 'Creative industries'), ('DEFENCE', 'Defence'), ('EDUCATION', 'Education and training'), ('ENERGY', 'Energy'), ('ENVIRONMENT', 'Environment'), ('FINANCIAL', 'Financial and professional services'), ('FOOD', 'Food and drink'), ('HEALTHCARE', 'Healthcare services'), ('MARITIME', 'Maritime'), ('MEDICAL', 'Medical devices and equipment'), ('MINING', 'Mining'), ('PHARMACEUTICALS', 'Pharmaceuticals and biotechnology'), ('RAILWAYS', 'Railways'), ('SECURITY', 'Security'), ('SPACE', 'Space'), ('SPORTS', 'Sports economy'), ('TECHNOLOGY', 'Technology and smart cities'), ('WATER', 'Water')], default='DEFAULT', max_length=255, verbose_name='Primary sector'),
        ),
        migrations.AlterField(
            model_name='enquiryactionlog',
            name='action',
            field=models.CharField(choices=[('EMAIL_CAMPAIGN_SUBSCRIBE', 'Subscribe to email campaign'), ('SECOND_QUALIFICATION_FORM', 'Second qualification form submitted'), ('MARKED_RESPONSIVE', 'Marked responsive'), ('UNSUBSCRIBED_FROM_CAMPAIGN', 'Unsubscribed from email campaign')], default='EMAIL_CAMPAIGN_SUBSCRIBE', max_length=150),
        ),
    ]
