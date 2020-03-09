# Generated by Django 3.0.3 on 2020-03-05 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enquiries", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enquiry",
            name="how_they_heard_dit",
            field=models.CharField(
                choices=[
                    ("DEFAULT", "----"),
                    ("PRESS_AD", "Press ad (newspaper/trade publication"),
                    ("OUTDOOR_AD", "Outdoor ad/billboard"),
                    ("LINKEDIN", "LinkedIn"),
                    ("SOCIAL_MEDIA", "Other social media (e.g. Twitter/Facebook)"),
                    ("INTERNET_SEARCH", "Internet search"),
                    ("OTHER", "Other"),
                ],
                default="DEFAULT",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="enquiry",
            name="marketing_channel",
            field=models.CharField(
                choices=[
                    ("DEFAULT", "----"),
                    ("LINKEDIN", "LinkedInLeadGen"),
                    ("CHOGM", "CHOGM"),
                    ("IIGB", "IiGB"),
                    ("IIGB_LINKEDIN", "IiGB (LinkedIn)"),
                    ("HPO", "HPO"),
                    ("B2B", "B2B"),
                    ("EBOOK", "EBOOK - Worldwide"),
                    ("TRA", "TRA"),
                    ("ENCORE", "Encore"),
                    ("OTHER", "Other"),
                ],
                default="DEFAULT",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="enquiry",
            name="new_existing_investor",
            field=models.CharField(
                choices=[
                    ("DEFAULT", "----"),
                    ("NEW,", "New investor"),
                    ("EXISTING,", "Existing investor"),
                ],
                default="DEFAULT",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="enquiry",
            name="organisation_type",
            field=models.CharField(
                choices=[
                    ("DEFAULT", "----"),
                    ("CHARITY,", "Charity"),
                    ("GOVERNMENT", "Government department or other public body"),
                    ("LIMITED_COMPANY", "Limited company"),
                    ("LIMITED_PARTNERSHIP", "Limited partnership"),
                    ("PARTNERSHIP,", "Partnership"),
                    ("SOLE_TRADER", "Sole trader"),
                ],
                default="DEFAULT",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="enquiry",
            name="quality",
            field=models.CharField(
                choices=[
                    ("DEFAULT", "----"),
                    ("NON_APPLICABLE", "Non-applicable"),
                    ("NON_FDI", "Non-FDI"),
                    ("POTENTIALLY_NON_FDI", "Potentially Non-FDI"),
                    ("POTENTIALLY_FDI", "Potentially FDI"),
                    ("LIKELY_FDI", "FDI or likely FDI"),
                ],
                default="DEFAULT",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="enquiry",
            name="region",
            field=models.CharField(
                choices=[
                    ("DEFAULT", "----"),
                    ("AMERICAS", "Americas"),
                    ("APAC", "Asia-Pacific"),
                    ("EMEA", "EMEA"),
                ],
                default="DEFAULT",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="enquiry",
            name="specific_investment_programme",
            field=models.CharField(
                choices=[
                    ("ADVANCED_ENG", "Advanced Engineering Supply Chain"),
                    ("BUSINESS_PARTNER", "Business Partnership (Non-FDI)"),
                    ("CONTRACT_RESEARCH", "Contract Research (Non-FDI)"),
                    ("FDI_CAPITAL_ONLY", "FDI (Capital Only)"),
                    ("GREAT_INV_PROG", "GREAT Investors Programme"),
                    ("GLOBAL_ENTREP_PROG", "Global Entrepreneur Programme"),
                    ("GRADUATE_ENTREP_PROG", "Graduate Entrepreneur Programme"),
                    ("HQ_UK", "HQ-UK"),
                    ("II&I", "II&I Programme"),
                    ("INFRASTRUCTURE_GATEWAY", "Infrastructure Gateway"),
                    ("IIGB", "Invest in Great Britain"),
                    ("NO_SPECIFIC_PROG", "No Specific Programme"),
                    ("R&D_COLLAB", "R&D Collaboration (Non-FDI)"),
                    ("R&D_PARTNERSHIP", "R&D Partnership (Non-FDI)"),
                    ("R&D_PROG", "R&D Prog (Obsolete)"),
                    ("REGENERATION", "Regeneration Investment Organisation (RIO)"),
                    ("SRM", "SRM Programme"),
                    ("SCREEN", "Screen Production Investment"),
                    ("SIRIUS", "Sirius (Graduate Entrepreneurs)"),
                    ("SPACE", "Space"),
                    ("UNIVERSITY_COLLAB", "University Collaboration (Non-FDI)"),
                    ("VENTURE_CAPITAL", "Venture / Equity Captial"),
                ],
                default="IIGB",
                max_length=255,
            ),
        ),
    ]
