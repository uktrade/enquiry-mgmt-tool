# Generated by Django 3.0.3 on 2020-02-21 12:49

from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields

from app.enquiries.models import Owner
import app.enquiries.ref_data as ref_data


def initial_data(apps, schema_editor):

    ist_users = [
        {
            "username": "ist-user-1",
            "first_name": "IST",
            "last_name": "User 1",
            "email": "ist.user.1@example.com",
        },
        {
            "username": "ist-user-2",
            "first_name": "IST",
            "last_name": "User 2",
            "email": "ist.user.2@example.com",
        },
        {
            "username": "ist-user-3",
            "first_name": "IST",
            "last_name": "User 3",
            "email": "ist.user.3@example.com",
        },
        {
            "username": "ist-user-4",
            "first_name": "IST",
            "last_name": "User 4",
            "email": "ist.user.4@example.com",
        },
        {
            "username": "ist-user-5",
            "first_name": "IST",
            "last_name": "User 5",
            "email": "ist.user.5@example.com",
        }
    ]
    for user in ist_users:
        Owner.objects.create(user=User.objects.create(**user))


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Enquirer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("job_title", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=255, unique=True)),
                ("phone", models.CharField(max_length=255)),
                ("email_consent", models.BooleanField(default=False)),
                ("phone_consent", models.BooleanField(default=False)),
                (
                    "request_for_call",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("YES_MORNING", "Yes - morning"),
                            ("YES_AFTERNOON", "Yes - afternoon"),
                            ("YES_OTHER", "Yes - other"),
                            ("NO", "No"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Owner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Enquiry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "company_name",
                    models.CharField(help_text="Name of the company", max_length=255),
                ),
                (
                    "enquiry_stage",
                    models.CharField(
                        choices=[
                            ("NEW", "New"),
                            ("AWAITING_RESPONSE", "Awaiting response from Investor"),
                            ("NON_RESPONSIVE", "Non-responsive"),
                            ("NON_FDI", "Non-FDI"),
                            ("ADDED_TO_DATAHUB", "Added to Data Hub"),
                            ("SENT_TO_POST", "Sent to Post"),
                            ("POST_PROGRESSING", "Post progressing"),
                        ],
                        default="NEW",
                        max_length=255,
                    ),
                ),
                ("enquiry_text", models.CharField(max_length=255)),
                (
                    "investment_readiness",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            (
                                "CONVINCED",
                                "I’m convinced and want to talk to someone about my plans",
                            ),
                            (
                                "SHORTLIST",
                                "The UK is on my shortlist. How can the Department for International Trade help me?",
                            ),
                            (
                                "EXPLORING",
                                "I’m still exploring where to expand my business and would like to know more about the UK’s offer",
                            ),
                            (
                                "NOT_READY",
                                "I’m not yet ready to invest. Keep me informed",
                            ),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "quality",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("NON_APPLICABLE", "Non-applicable"),
                            ("NON_FDI", "Non-FDI"),
                            ("POTENTIALLY_NON_FDI", "Potentially Non-FDI"),
                            ("POTENTIALLY_FDI", "Potentially FDI"),
                            ("LIKELY_FDI", "Likely to be FDI"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "google_campaign",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "marketing_channel",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("LINKEDIN", "LinkedInLeadGen"),
                            ("CHOGM", "CHOGM"),
                            ("IIGB", "IiGB"),
                            ("IIGB_LINKEDIN", "IiGB (LinkedIN)"),
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
                (
                    "how_they_heard_dit",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("PRESS_AD", "Press ad (newspapaer/trade publication"),
                            ("OUTDOOR_AD", "Outdoor ad/billboard"),
                            ("LINKEDIN", "LinkedIn"),
                            (
                                "SOCIAL_MEDIA",
                                "Other social media (e.g. Twitter/Facebook)",
                            ),
                            ("INTERNET_SEARCH", "Internet Search"),
                            ("OTHER", "Other"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                ("website", models.URLField(blank=True, max_length=255, null=True)),
                (
                    "primary_sector",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("ADVANCED_ENG", "Advanced Engineering"),
                            ("AEROSPACE", "Aerospace"),
                            (
                                "AGRICULTURE,",
                                "Agriculture, Horticulture, Fisheries and Pets",
                            ),
                            ("AIRPORTS", "Airports"),
                            ("AUTOMOTIVE", "Automotive"),
                            ("CHEMICALS", "Chemicals"),
                            ("CONSTRUCTION", "Construction"),
                            ("CONSUMER", "Consumer and Retail"),
                            ("CREATIVE", "Creative Industries"),
                            ("CYBER", "Cyber Security"),
                            ("DEFENCE", "Defence"),
                            ("EDUCATION", "Education and Training"),
                            ("ENERGY", "Energy"),
                            ("ENVIRONMENT", "Environment"),
                            ("FINANCIAL", "Financial and Professional Services"),
                            ("FOOD", "Food and Drink"),
                            ("HEALTHCARE", "Healthcare Services"),
                            ("MARITIME", "Maritime"),
                            ("MEDICAL", "Medical Devices and Equipment"),
                            ("MINING", "Mining"),
                            ("PHARMACEUTICALS", "Pharmaceuticals and Biotechnology"),
                            ("RAILWAYS", "Railways"),
                            ("SECURITY", "Security"),
                            ("SPACE", "Space"),
                            ("SPORTS", "Sports Economy"),
                            ("TECHNOLOGY", "Technology and Smart Cities"),
                            ("WATER", "Water"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "ist_sector",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("ITECH", "ITECH"),
                            ("LIFE", "Life Science"),
                            ("ENERGY", "Energy and Environment"),
                            ("BPFS", "BPFS"),
                            ("AEM", "AEM"),
                            ("UNCLASSIFIED", "Unclassified"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                ("company_hq_address", models.CharField(max_length=255)),
                (
                    "country",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("AFGHANISTAN", "Afghanistan"),
                            ("ALBANIA", "Albania"),
                            ("ALGERIA", "Algeria"),
                            ("ANDORRA", "Andorra"),
                            ("ANGOLA", "Angola"),
                            ("ANTIGUA", "Antigua and Barbuda"),
                            ("ARGENTINA", "Argentina"),
                            ("ARMENIA", "Armenia"),
                            ("AUSTRALIA", "Australia"),
                            ("AUSTRIA", "Austria"),
                            ("AZERBAIJAN", "Azerbaijan"),
                            ("BAHRAIN", "Bahrain"),
                            ("BANGLADESH", "Bangladesh"),
                            ("BARBADOS", "Barbados"),
                            ("BELARUS", "Belarus"),
                            ("BELGIUM", "Belgium"),
                            ("BELIZE", "Belize"),
                            ("BENIN", "Benin"),
                            ("BHUTAN", "Bhutan"),
                            ("BOLIVIA", "Bolivia"),
                            ("BOSNIA", "Bosnia and Herzegovina"),
                            ("BOTSWANA", "Botswana"),
                            ("BRAZIL", "Brazil"),
                            ("BRUNEI", "Brunei"),
                            ("BULGARIA", "Bulgaria"),
                            ("BURKINA", "Burkina Faso"),
                            ("BURUNDI", "Burundi"),
                            ("CAMBODIA", "Cambodia"),
                            ("CAMEROON", "Cameroon"),
                            ("CANADA", "Canada"),
                            ("CAPE", "Cape Verde"),
                            ("CENTRAL_AFRICA", "Central African Republic"),
                            ("CHAD", "Chad"),
                            ("CHILE", "Chile"),
                            ("CHINA", "China"),
                            ("COLOMBIA", "Colombia"),
                            ("COMOROS", "Comoros"),
                            ("CONGO", "Congo"),
                            ("CONGO_DR", "Congo (Democratic Republic)"),
                            ("COSTA", "Costa Rica"),
                            ("CROATIA", "Croatia"),
                            ("CUBA", "Cuba"),
                            ("CYPRUS", "Cyprus"),
                            ("CZECHIA", "Czechia"),
                            ("DENMARK", "Denmark"),
                            ("DJIBOUTI", "Djibouti"),
                            ("DOMINICA", "Dominica"),
                            ("DOMINICAN", "Dominican Republic"),
                            ("EAST_TIMOR", "East Timor"),
                            ("ECUADOR", "Ecuador"),
                            ("EGYPT", "Egypt"),
                            ("EL_SALVADOR", "El Salvador"),
                            ("EQUATORIAL_GUINEA", "Equatorial Guinea"),
                            ("ERITREA", "Eritrea"),
                            ("ESTONIA", "Estonia"),
                            ("ESWATINI", "Eswatini"),
                            ("ETHIOPIA", "Ethiopia"),
                            ("FIJI", "Fiji"),
                            ("FINLAND", "Finland"),
                            ("FRANCE", "France"),
                            ("GABON", "Gabon"),
                            ("GEORGIA", "Georgia"),
                            ("GERMANY", "Germany"),
                            ("GHANA", "Ghana"),
                            ("GREECE", "Greece"),
                            ("GRENADA", "Grenada"),
                            ("GUATEMALA", "Guatemala"),
                            ("GUINEA", "Guinea"),
                            ("GUINEA_BISSAU", "Guinea-Bissau"),
                            ("GUYANA", "Guyana"),
                            ("HAITI", "Haiti"),
                            ("HONDURAS", "Honduras"),
                            ("HUNGARY", "Hungary"),
                            ("ICELAND", "Iceland"),
                            ("INDIA", "India"),
                            ("INDONESIA", "Indonesia"),
                            ("IRAN", "Iran"),
                            ("IRAQ", "Iraq"),
                            ("IRELAND", "Ireland"),
                            ("ISRAEL", "Israel"),
                            ("ITALY", "Italy"),
                            ("IVORY", "Ivory Coast"),
                            ("JAMAICA", "Jamaica"),
                            ("JAPAN", "Japan"),
                            ("JORDAN", "Jordan"),
                            ("KAZAKHSTAN", "Kazakhstan"),
                            ("KENYA", "Kenya"),
                            ("KIRIBATI", "Kiribati"),
                            ("KOSOVO", "Kosovo"),
                            ("KUWAIT", "Kuwait"),
                            ("KYRGYZSTAN", "Kyrgyzstan"),
                            ("LAOS", "Laos"),
                            ("LATVIA", "Latvia"),
                            ("LEBANON", "Lebanon"),
                            ("LESOTHO", "Lesotho"),
                            ("LIBERIA", "Liberia"),
                            ("LIBYA", "Libya"),
                            ("LIECHTENSTEIN", "Liechtenstein"),
                            ("LITHUANIA", "Lithuania"),
                            ("LUXEMBOURG", "Luxembourg"),
                            ("MADAGASCAR", "Madagascar"),
                            ("MALAWI", "Malawi"),
                            ("MALAYSIA", "Malaysia"),
                            ("MALDIVES", "Maldives"),
                            ("MALI", "Mali"),
                            ("MALTA", "Malta"),
                            ("MARSHALL", "Marshall Islands"),
                            ("MAURITANIA", "Mauritania"),
                            ("MAURITIUS", "Mauritius"),
                            ("MEXICO", "Mexico"),
                            ("MICRONESIA", "Micronesia"),
                            ("MOLDOVA", "Moldova"),
                            ("MONACO", "Monaco"),
                            ("MONGOLIA", "Mongolia"),
                            ("MONTENEGRO", "Montenegro"),
                            ("MOROCCO", "Morocco"),
                            ("MOZAMBIQUE", "Mozambique"),
                            ("MYANMAR", "Myanmar (Burma)"),
                            ("NAMIBIA", "Namibia"),
                            ("NAURU", "Nauru"),
                            ("NEPAL", "Nepal"),
                            ("NETHERLANDS", "Netherlands"),
                            ("NEW", "New Zealand"),
                            ("NICARAGUA", "Nicaragua"),
                            ("NIGER", "Niger"),
                            ("NIGERIA", "Nigeria"),
                            ("NORTH_KOREA", "North Korea"),
                            ("NORTH_MACEDONIA", "North Macedonia"),
                            ("NORWAY", "Norway"),
                            ("OMAN", "Oman"),
                            ("PAKISTAN", "Pakistan"),
                            ("PALAU", "Palau"),
                            ("PANAMA", "Panama"),
                            ("PAPUA", "Papua New Guinea"),
                            ("PARAGUAY", "Paraguay"),
                            ("PERU", "Peru"),
                            ("PHILIPPINES", "Philippines"),
                            ("POLAND", "Poland"),
                            ("PORTUGAL", "Portugal"),
                            ("QATAR", "Qatar"),
                            ("ROMANIA", "Romania"),
                            ("RUSSIA", "Russia"),
                            ("RWANDA", "Rwanda"),
                            ("SAMOA", "Samoa"),
                            ("SAN", "San Marino"),
                            ("SAO", "Sao Tome and Principe"),
                            ("SAUDI", "Saudi Arabia"),
                            ("SENEGAL", "Senegal"),
                            ("SERBIA", "Serbia"),
                            ("SEYCHELLES", "Seychelles"),
                            ("SIERRA", "Sierra Leone"),
                            ("SINGAPORE", "Singapore"),
                            ("SLOVAKIA", "Slovakia"),
                            ("SLOVENIA", "Slovenia"),
                            ("SOLOMON", "Solomon Islands"),
                            ("SOMALIA", "Somalia"),
                            ("SOUTH_AFRICA", "South Africa"),
                            ("SOUTH_KOREA", "South Korea"),
                            ("SOUTH_SUDAN", "South Sudan"),
                            ("SPAIN", "Spain"),
                            ("SRI_LANKA", "Sri Lanka"),
                            ("STKITTS", "St Kitts and Nevis"),
                            ("STLUCIA", "St Lucia"),
                            ("STVINCENT", "St Vincent"),
                            ("SUDAN", "Sudan"),
                            ("SURINAME", "Suriname"),
                            ("SWEDEN", "Sweden"),
                            ("SWITZERLAND", "Switzerland"),
                            ("SYRIA", "Syria"),
                            ("TAJIKISTAN", "Tajikistan"),
                            ("TANZANIA", "Tanzania"),
                            ("THAILAND", "Thailand"),
                            ("BAHAMAS", "The Bahamas"),
                            ("GAMBIA", "The Gambia"),
                            ("TOGO", "Togo"),
                            ("TONGA", "Tonga"),
                            ("TRINIDAD", "Trinidad and Tobago"),
                            ("TUNISIA", "Tunisia"),
                            ("TURKEY", "Turkey"),
                            ("TURKMENISTAN", "Turkmenistan"),
                            ("TUVALU", "Tuvalu"),
                            ("UGANDA", "Uganda"),
                            ("UKRAINE", "Ukraine"),
                            ("UAE", "United Arab Emirates"),
                            ("UK", "United Kingdom"),
                            ("US", "United States"),
                            ("URUGUAY", "Uruguay"),
                            ("UZBEKISTAN", "Uzbekistan"),
                            ("VANUATU", "Vanuatu"),
                            ("VATICAN", "Vatican City"),
                            ("VENEZUELA", "Venezuela"),
                            ("VIETNAM", "Vietnam"),
                            ("YEMEN", "Yemen"),
                            ("ZAMBIA", "Zambia"),
                            ("ZIMBABWE", "Zimbabwe"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("AMERICAS", "Americas"),
                            ("APAC", "Asia Pacific"),
                            ("EMEA", "Europe and Middle East"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "first_response_channel",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("CALL", "Call"),
                            ("EMAIL", "Email"),
                            ("NOT_RESPONDED", "Not yet responded"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                ("notes", models.TextField()),
                (
                    "first_hpo_selection",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("FOOD_PRODUCTION", "Food production"),
                            ("UK_RAIL", "UK rail"),
                            ("LIGHTWEIGHT_STRUCTURES", "Lightweight structures"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "second_hpo_selection",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("FOOD_PRODUCTION", "Food production"),
                            ("UK_RAIL", "UK rail"),
                            ("LIGHTWEIGHT_STRUCTURES", "Lightweight structures"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "third_hpo_selection",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("FOOD_PRODUCTION", "Food production"),
                            ("UK_RAIL", "UK rail"),
                            ("LIGHTWEIGHT_STRUCTURES", "Lightweight structures"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "organisation_type",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("CHARITY,", "charity"),
                            ("GOVERNMENT", "gov department or other public body"),
                            ("LIMITED_COMPANY", "limited company"),
                            ("LIMITED_PARTNERSHIP", "limited partnership"),
                            ("PARTNERSHIP,", "partnership"),
                            ("SOLE_TRADER", "sole trader"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "investment_type",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("ACQUISITION", "Acquisition"),
                            ("CAPITAL_ONLY", "Capital only"),
                            ("NEW_SITE", "Creation of new site or activity"),
                            ("EXPANSION", "Expansion of existing site or activity"),
                            ("JOINT_VENTURE", "Joint venture"),
                            ("MERGER", "Merger"),
                            ("RETENTION", "Retention"),
                            ("NOT_SPECIFIED", "Not specified"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "project_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("project_description", models.TextField(blank=True, null=True)),
                (
                    "anonymised_project_description",
                    models.TextField(blank=True, null=True),
                ),
                ("estimated_land_date", models.DateField(blank=True, null=True)),
                (
                    "new_existing_investor",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("NEW,", "New Investor"),
                            ("EXISTING,", "Existing Investor"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                (
                    "investor_involvement_level",
                    models.CharField(
                        choices=[
                            ("FDI_HUB_HQ", "FDI Hub + HQ"),
                            ("FDI_HUB_HQ_LEP", "FDI Hub + HQ + LEP"),
                            ("FDI_HUB_HQ_POST_LEP", "FDI Hub + HQ + Post + LEP"),
                            ("FDI_HUB_HQ_POST_REG", "FDI Hub + HQ + Post + Reg"),
                            ("FDI_HUB_HQ_REG", "FDI Hub + HQ  + Reg"),
                            ("FDI_HUB_LEP", "FDI Hub + LEP"),
                            ("FDI_HUB_POST", "FDI Hub + Post"),
                            ("FDI_HUB_POST_HQ", "FDI Hub + Post + HQ"),
                            ("FDI_HUB_POST_LEP", "FDI Hub + Post + LEP"),
                            ("FDI_HUB_POST_REG", "FDI Hub + Post + Reg"),
                            ("FDI_HUB_REGION", "FDI Hub + Region"),
                            ("FDI_HUB_ONLY", "FDI Hub Only"),
                            ("HQ_LEP", "HQ + LEP"),
                            ("HQ_POST_LEP", "HQ + Post + LEP"),
                            ("HQ_ONLY", "HQ Only"),
                            ("HQ_POST_ONLY", "HQ and Post Only"),
                            ("HQ_REGION", "HQ and Region"),
                            ("HQ_POST_REGION,", "HQ, Post and Region"),
                            ("LEP_ONLY", "LEP Only"),
                            ("NO_INVOLVEMENT", "No involvement"),
                            ("POST_LEP", "Post + LEP"),
                            ("POST_ONLY", "Post Only"),
                            ("POST_REGION", "Post and Region"),
                            ("REGION_ONLY", "Region Only"),
                        ],
                        default="FDI_HUB_POST",
                        max_length=255,
                    ),
                ),
                (
                    "specific_investment_program",
                    models.CharField(
                        choices=[
                            ("ADVANCED_ENG", "Advanced Engineering Supply Chain"),
                            ("BUSINESS_PARTNER", "Business Partnership (Non-FDI)"),
                            ("CONTRACT_RESEARCH", "Contract Research (Non-FDI)"),
                            ("FDI_CAPITAL_ONLY", "FDI (Capital Only)"),
                            ("GREAT_INV_PROG", "GREAT Investors Programme"),
                            ("GLOBAL_ENTERP_PROG", "Global Entrepreneur Programme"),
                            ("GRADUATE_ENTERP_PROG", "Graduate Entrepreneur Programme"),
                            ("HQ_UK", "HQ-UK"),
                            ("II&I", "II&I Programme"),
                            ("INFRASTRUCTURE_GATEWAY", "Infrastructure Gateway"),
                            ("IIGB", "Invest in Great Britain"),
                            ("NO_SPECIFIC_PROG", "No Specific Programme"),
                            ("R&D_COLLAB", "R&D Collaboration (Non-FDI)"),
                            ("R&D_PARTNERSHIP", "R&D Partnership (Non-FDI)"),
                            ("R&D_PROG", "R&D Prog (Obsolete)"),
                            (
                                "REGENERATION",
                                "Regeneration Investment Organisation (RIO)",
                            ),
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
                (
                    "crm",
                    models.CharField(
                        help_text="Name of the relationship manager", max_length=255
                    ),
                ),
                (
                    "project_code",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_added_to_datahub", models.DateField(blank=True, null=True)),
                (
                    "datahub_project_status",
                    models.CharField(
                        choices=[
                            ("DEFAULT", "----"),
                            ("PROSPECT", "Prospect"),
                            ("ASSIGN", "Assign PM"),
                            ("ACTIVE", "Active"),
                            ("VERIFY", "Verify Win"),
                            ("WON", "Won"),
                            ("ABANDONED", "Abandoned"),
                            ("DELAYED", "Delayed"),
                        ],
                        default="DEFAULT",
                        max_length=255,
                    ),
                ),
                ("project_success_date", models.DateField(blank=True, null=True)),
                (
                    "enquirer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="enquirer",
                        to="enquiries.Enquirer",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="User assigned to the enquiry",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="owner",
                        to="enquiries.Owner",
                    ),
                ),
            ],
            options={"ordering": ["created"],},
        ),
        migrations.RunPython(initial_data),
    ]
