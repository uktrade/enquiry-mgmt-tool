# Generated by Django 3.0.3 on 2020-03-09 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enquiries', '0002_auto_20200305_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquirer',
            name='email',
            field=models.EmailField(blank=True, max_length=255, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='enquirer',
            name='email_consent',
            field=models.BooleanField(default=False, verbose_name='Email consent'),
        ),
        migrations.AlterField(
            model_name='enquirer',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='enquirer',
            name='job_title',
            field=models.CharField(max_length=255, verbose_name='Job title'),
        ),
        migrations.AlterField(
            model_name='enquirer',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='enquirer',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='enquirer',
            name='phone_consent',
            field=models.BooleanField(default=False, verbose_name='Phone consent'),
        ),
        migrations.AlterField(
            model_name='enquirer',
            name='request_for_call',
            field=models.CharField(choices=[('DEFAULT', '----'), ('YES_MORNING', 'Yes - morning'), ('YES_AFTERNOON', 'Yes - afternoon'), ('YES_OTHER', 'Yes - other'), ('NO', 'No')], default='DEFAULT', max_length=255, verbose_name='Call requested'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='anonymised_project_description',
            field=models.TextField(blank=True, null=True, verbose_name='Anonymised project description'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='company_hq_address',
            field=models.CharField(max_length=255, verbose_name='Company HQ address'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='company_name',
            field=models.CharField(help_text='Name of the company', max_length=255, verbose_name='Company name'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='country',
            field=models.CharField(choices=[('DEFAULT', '----'), ('AFGHANISTAN', 'Afghanistan'), ('ALBANIA', 'Albania'), ('ALGERIA', 'Algeria'), ('ANDORRA', 'Andorra'), ('ANGOLA', 'Angola'), ('ANTIGUA', 'Antigua and Barbuda'), ('ARGENTINA', 'Argentina'), ('ARMENIA', 'Armenia'), ('AUSTRALIA', 'Australia'), ('AUSTRIA', 'Austria'), ('AZERBAIJAN', 'Azerbaijan'), ('BAHRAIN', 'Bahrain'), ('BANGLADESH', 'Bangladesh'), ('BARBADOS', 'Barbados'), ('BELARUS', 'Belarus'), ('BELGIUM', 'Belgium'), ('BELIZE', 'Belize'), ('BENIN', 'Benin'), ('BHUTAN', 'Bhutan'), ('BOLIVIA', 'Bolivia'), ('BOSNIA', 'Bosnia and Herzegovina'), ('BOTSWANA', 'Botswana'), ('BRAZIL', 'Brazil'), ('BRUNEI', 'Brunei'), ('BULGARIA', 'Bulgaria'), ('BURKINA', 'Burkina Faso'), ('BURUNDI', 'Burundi'), ('CAMBODIA', 'Cambodia'), ('CAMEROON', 'Cameroon'), ('CANADA', 'Canada'), ('CAPE', 'Cape Verde'), ('CENTRAL_AFRICA', 'Central African Republic'), ('CHAD', 'Chad'), ('CHILE', 'Chile'), ('CHINA', 'China'), ('COLOMBIA', 'Colombia'), ('COMOROS', 'Comoros'), ('CONGO', 'Congo'), ('CONGO_DR', 'Congo (Democratic Republic)'), ('COSTA', 'Costa Rica'), ('CROATIA', 'Croatia'), ('CUBA', 'Cuba'), ('CYPRUS', 'Cyprus'), ('CZECHIA', 'Czechia'), ('DENMARK', 'Denmark'), ('DJIBOUTI', 'Djibouti'), ('DOMINICA', 'Dominica'), ('DOMINICAN', 'Dominican Republic'), ('EAST_TIMOR', 'East Timor'), ('ECUADOR', 'Ecuador'), ('EGYPT', 'Egypt'), ('EL_SALVADOR', 'El Salvador'), ('EQUATORIAL_GUINEA', 'Equatorial Guinea'), ('ERITREA', 'Eritrea'), ('ESTONIA', 'Estonia'), ('ESWATINI', 'Eswatini'), ('ETHIOPIA', 'Ethiopia'), ('FIJI', 'Fiji'), ('FINLAND', 'Finland'), ('FRANCE', 'France'), ('GABON', 'Gabon'), ('GEORGIA', 'Georgia'), ('GERMANY', 'Germany'), ('GHANA', 'Ghana'), ('GREECE', 'Greece'), ('GRENADA', 'Grenada'), ('GUATEMALA', 'Guatemala'), ('GUINEA', 'Guinea'), ('GUINEA_BISSAU', 'Guinea-Bissau'), ('GUYANA', 'Guyana'), ('HAITI', 'Haiti'), ('HONDURAS', 'Honduras'), ('HUNGARY', 'Hungary'), ('ICELAND', 'Iceland'), ('INDIA', 'India'), ('INDONESIA', 'Indonesia'), ('IRAN', 'Iran'), ('IRAQ', 'Iraq'), ('IRELAND', 'Ireland'), ('ISRAEL', 'Israel'), ('ITALY', 'Italy'), ('IVORY', 'Ivory Coast'), ('JAMAICA', 'Jamaica'), ('JAPAN', 'Japan'), ('JORDAN', 'Jordan'), ('KAZAKHSTAN', 'Kazakhstan'), ('KENYA', 'Kenya'), ('KIRIBATI', 'Kiribati'), ('KOSOVO', 'Kosovo'), ('KUWAIT', 'Kuwait'), ('KYRGYZSTAN', 'Kyrgyzstan'), ('LAOS', 'Laos'), ('LATVIA', 'Latvia'), ('LEBANON', 'Lebanon'), ('LESOTHO', 'Lesotho'), ('LIBERIA', 'Liberia'), ('LIBYA', 'Libya'), ('LIECHTENSTEIN', 'Liechtenstein'), ('LITHUANIA', 'Lithuania'), ('LUXEMBOURG', 'Luxembourg'), ('MADAGASCAR', 'Madagascar'), ('MALAWI', 'Malawi'), ('MALAYSIA', 'Malaysia'), ('MALDIVES', 'Maldives'), ('MALI', 'Mali'), ('MALTA', 'Malta'), ('MARSHALL', 'Marshall Islands'), ('MAURITANIA', 'Mauritania'), ('MAURITIUS', 'Mauritius'), ('MEXICO', 'Mexico'), ('MICRONESIA', 'Micronesia'), ('MOLDOVA', 'Moldova'), ('MONACO', 'Monaco'), ('MONGOLIA', 'Mongolia'), ('MONTENEGRO', 'Montenegro'), ('MOROCCO', 'Morocco'), ('MOZAMBIQUE', 'Mozambique'), ('MYANMAR', 'Myanmar (Burma)'), ('NAMIBIA', 'Namibia'), ('NAURU', 'Nauru'), ('NEPAL', 'Nepal'), ('NETHERLANDS', 'Netherlands'), ('NEW', 'New Zealand'), ('NICARAGUA', 'Nicaragua'), ('NIGER', 'Niger'), ('NIGERIA', 'Nigeria'), ('NORTH_KOREA', 'North Korea'), ('NORTH_MACEDONIA', 'North Macedonia'), ('NORWAY', 'Norway'), ('OMAN', 'Oman'), ('PAKISTAN', 'Pakistan'), ('PALAU', 'Palau'), ('PANAMA', 'Panama'), ('PAPUA', 'Papua New Guinea'), ('PARAGUAY', 'Paraguay'), ('PERU', 'Peru'), ('PHILIPPINES', 'Philippines'), ('POLAND', 'Poland'), ('PORTUGAL', 'Portugal'), ('QATAR', 'Qatar'), ('ROMANIA', 'Romania'), ('RUSSIA', 'Russia'), ('RWANDA', 'Rwanda'), ('SAMOA', 'Samoa'), ('SAN', 'San Marino'), ('SAO', 'Sao Tome and Principe'), ('SAUDI', 'Saudi Arabia'), ('SENEGAL', 'Senegal'), ('SERBIA', 'Serbia'), ('SEYCHELLES', 'Seychelles'), ('SIERRA', 'Sierra Leone'), ('SINGAPORE', 'Singapore'), ('SLOVAKIA', 'Slovakia'), ('SLOVENIA', 'Slovenia'), ('SOLOMON', 'Solomon Islands'), ('SOMALIA', 'Somalia'), ('SOUTH_AFRICA', 'South Africa'), ('SOUTH_KOREA', 'South Korea'), ('SOUTH_SUDAN', 'South Sudan'), ('SPAIN', 'Spain'), ('SRI_LANKA', 'Sri Lanka'), ('STKITTS', 'St Kitts and Nevis'), ('STLUCIA', 'St Lucia'), ('STVINCENT', 'St Vincent'), ('SUDAN', 'Sudan'), ('SURINAME', 'Suriname'), ('SWEDEN', 'Sweden'), ('SWITZERLAND', 'Switzerland'), ('SYRIA', 'Syria'), ('TAJIKISTAN', 'Tajikistan'), ('TANZANIA', 'Tanzania'), ('THAILAND', 'Thailand'), ('BAHAMAS', 'The Bahamas'), ('GAMBIA', 'The Gambia'), ('TOGO', 'Togo'), ('TONGA', 'Tonga'), ('TRINIDAD', 'Trinidad and Tobago'), ('TUNISIA', 'Tunisia'), ('TURKEY', 'Turkey'), ('TURKMENISTAN', 'Turkmenistan'), ('TUVALU', 'Tuvalu'), ('UGANDA', 'Uganda'), ('UKRAINE', 'Ukraine'), ('UAE', 'United Arab Emirates'), ('UK', 'United Kingdom'), ('US', 'United States'), ('URUGUAY', 'Uruguay'), ('UZBEKISTAN', 'Uzbekistan'), ('VANUATU', 'Vanuatu'), ('VATICAN', 'Vatican City'), ('VENEZUELA', 'Venezuela'), ('VIETNAM', 'Vietnam'), ('YEMEN', 'Yemen'), ('ZAMBIA', 'Zambia'), ('ZIMBABWE', 'Zimbabwe')], default='DEFAULT', max_length=255, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='crm',
            field=models.CharField(help_text='Name of the relationship manager', max_length=255, verbose_name='CRM'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='datahub_project_status',
            field=models.CharField(choices=[('DEFAULT', '----'), ('PROSPECT', 'Prospect'), ('ASSIGN', 'Assign PM'), ('ACTIVE', 'Active'), ('VERIFY', 'Verify Win'), ('WON', 'Won'), ('ABANDONED', 'Abandoned'), ('DELAYED', 'Delayed')], default='DEFAULT', max_length=255, verbose_name='Data Hub project status'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='date_added_to_datahub',
            field=models.DateField(blank=True, null=True, verbose_name='Date added to Data Hub'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquirer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enquirer', to='enquiries.Enquirer', verbose_name='Enquirer'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquiry_stage',
            field=models.CharField(choices=[('NEW', 'New'), ('AWAITING_RESPONSE', 'Awaiting response from Investor'), ('NON_RESPONSIVE', 'Non-responsive'), ('NON_FDI', 'Non-FDI'), ('ADDED_TO_DATAHUB', 'Added to Data Hub'), ('SENT_TO_POST', 'Sent to Post'), ('POST_PROGRESSING', 'Post progressing')], default='NEW', max_length=255, verbose_name='Enquiry stage'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquiry_text',
            field=models.CharField(max_length=255, verbose_name='Enquiry text'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='estimated_land_date',
            field=models.DateField(blank=True, null=True, verbose_name='Estimated land date'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='first_hpo_selection',
            field=models.CharField(choices=[('DEFAULT', '----'), ('FOOD_PRODUCTION', 'Food production'), ('UK_RAIL', 'UK rail'), ('LIGHTWEIGHT_STRUCTURES', 'Lightweight structures')], default='DEFAULT', max_length=255, verbose_name='First HPO selection'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='first_response_channel',
            field=models.CharField(choices=[('DEFAULT', '----'), ('CALL', 'Call'), ('EMAIL', 'Email'), ('NOT_RESPONDED', 'Not yet responded')], default='DEFAULT', max_length=255, verbose_name='First response channel'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='google_campaign',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Google campaign'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='how_they_heard_dit',
            field=models.CharField(choices=[('DEFAULT', '----'), ('PRESS_AD', 'Press ad (newspaper/trade publication'), ('OUTDOOR_AD', 'Outdoor ad/billboard'), ('LINKEDIN', 'LinkedIn'), ('SOCIAL_MEDIA', 'Other social media (e.g. Twitter/Facebook)'), ('INTERNET_SEARCH', 'Internet search'), ('OTHER', 'Other')], default='DEFAULT', max_length=255, verbose_name='How did they hear about DIT?'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='investment_readiness',
            field=models.CharField(choices=[('DEFAULT', '----'), ('CONVINCED', 'I’m convinced and want to talk to someone about my plans'), ('SHORTLIST', 'The UK is on my shortlist. How can the Department for International Trade help me?'), ('EXPLORING', 'I’m still exploring where to expand my business and would like to know more about the UK’s offer'), ('NOT_READY', 'I’m not yet ready to invest. Keep me informed')], default='DEFAULT', max_length=255, verbose_name='Investment readiness'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='investment_type',
            field=models.CharField(choices=[('DEFAULT', '----'), ('ACQUISITION', 'Acquisition'), ('CAPITAL_ONLY', 'Capital only'), ('NEW_SITE', 'Creation of new site or activity'), ('EXPANSION', 'Expansion of existing site or activity'), ('JOINT_VENTURE', 'Joint venture'), ('MERGER', 'Merger'), ('RETENTION', 'Retention'), ('NOT_SPECIFIED', 'Not specified')], default='DEFAULT', max_length=255, verbose_name='Investment type'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='investor_involvement_level',
            field=models.CharField(choices=[('FDI_HUB_HQ', 'FDI Hub + HQ'), ('FDI_HUB_HQ_LEP', 'FDI Hub + HQ + LEP'), ('FDI_HUB_HQ_POST_LEP', 'FDI Hub + HQ + Post + LEP'), ('FDI_HUB_HQ_POST_REG', 'FDI Hub + HQ + Post + Reg'), ('FDI_HUB_HQ_REG', 'FDI Hub + HQ  + Reg'), ('FDI_HUB_LEP', 'FDI Hub + LEP'), ('FDI_HUB_POST', 'FDI Hub + Post'), ('FDI_HUB_POST_HQ', 'FDI Hub + Post + HQ'), ('FDI_HUB_POST_LEP', 'FDI Hub + Post + LEP'), ('FDI_HUB_POST_REG', 'FDI Hub + Post + Reg'), ('FDI_HUB_REGION', 'FDI Hub + Region'), ('FDI_HUB_ONLY', 'FDI Hub Only'), ('HQ_LEP', 'HQ + LEP'), ('HQ_POST_LEP', 'HQ + Post + LEP'), ('HQ_ONLY', 'HQ Only'), ('HQ_POST_ONLY', 'HQ and Post Only'), ('HQ_REGION', 'HQ and Region'), ('HQ_POST_REGION,', 'HQ, Post and Region'), ('LEP_ONLY', 'LEP Only'), ('NO_INVOLVEMENT', 'No involvement'), ('POST_LEP', 'Post + LEP'), ('POST_ONLY', 'Post Only'), ('POST_REGION', 'Post and Region'), ('REGION_ONLY', 'Region Only')], default='FDI_HUB_POST', max_length=255, verbose_name='Investor level of involvement'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='ist_sector',
            field=models.CharField(choices=[('DEFAULT', '----'), ('ITECH', 'ITECH'), ('LIFE', 'Life Science'), ('ENERGY', 'Energy and Environment'), ('BPFS', 'BPFS'), ('AEM', 'AEM'), ('UNCLASSIFIED', 'Unclassified')], default='DEFAULT', max_length=255, verbose_name='IST sector'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='marketing_channel',
            field=models.CharField(choices=[('DEFAULT', '----'), ('LINKEDIN', 'LinkedInLeadGen'), ('CHOGM', 'CHOGM'), ('IIGB', 'IiGB'), ('IIGB_LINKEDIN', 'IiGB (LinkedIn)'), ('HPO', 'HPO'), ('B2B', 'B2B'), ('EBOOK', 'EBOOK - Worldwide'), ('TRA', 'TRA'), ('ENCORE', 'Encore'), ('OTHER', 'Other')], default='DEFAULT', max_length=255, verbose_name='Marketing channel'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='new_existing_investor',
            field=models.CharField(choices=[('DEFAULT', '----'), ('NEW,', 'New investor'), ('EXISTING,', 'Existing investor')], default='DEFAULT', max_length=255, verbose_name='New or existing investor'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='notes',
            field=models.TextField(verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='organisation_type',
            field=models.CharField(choices=[('DEFAULT', '----'), ('CHARITY,', 'Charity'), ('GOVERNMENT', 'Government department or other public body'), ('LIMITED_COMPANY', 'Limited company'), ('LIMITED_PARTNERSHIP', 'Limited partnership'), ('PARTNERSHIP,', 'Partnership'), ('SOLE_TRADER', 'Sole trader')], default='DEFAULT', max_length=255, verbose_name='Organisation type'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='User assigned to the enquiry', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='owner', to='enquiries.Owner', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='primary_sector',
            field=models.CharField(choices=[('DEFAULT', '----'), ('ADVANCED_ENG', 'Advanced Engineering'), ('AEROSPACE', 'Aerospace'), ('AGRICULTURE,', 'Agriculture, Horticulture, Fisheries and Pets'), ('AIRPORTS', 'Airports'), ('AUTOMOTIVE', 'Automotive'), ('CHEMICALS', 'Chemicals'), ('CONSTRUCTION', 'Construction'), ('CONSUMER', 'Consumer and Retail'), ('CREATIVE', 'Creative Industries'), ('CYBER', 'Cyber Security'), ('DEFENCE', 'Defence'), ('EDUCATION', 'Education and Training'), ('ENERGY', 'Energy'), ('ENVIRONMENT', 'Environment'), ('FINANCIAL', 'Financial and Professional Services'), ('FOOD', 'Food and Drink'), ('HEALTHCARE', 'Healthcare Services'), ('MARITIME', 'Maritime'), ('MEDICAL', 'Medical Devices and Equipment'), ('MINING', 'Mining'), ('PHARMACEUTICALS', 'Pharmaceuticals and Biotechnology'), ('RAILWAYS', 'Railways'), ('SECURITY', 'Security'), ('SPACE', 'Space'), ('SPORTS', 'Sports Economy'), ('TECHNOLOGY', 'Technology and Smart Cities'), ('WATER', 'Water')], default='DEFAULT', max_length=255, verbose_name='Primary sector'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='project_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Project code'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='project_description',
            field=models.TextField(blank=True, null=True, verbose_name='Project description'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='project_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Project name'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='project_success_date',
            field=models.DateField(blank=True, null=True, verbose_name='Project success date'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='quality',
            field=models.CharField(choices=[('DEFAULT', '----'), ('NON_APPLICABLE', 'Non-applicable'), ('NON_FDI', 'Non-FDI'), ('POTENTIALLY_NON_FDI', 'Potentially Non-FDI'), ('POTENTIALLY_FDI', 'Potentially FDI'), ('LIKELY_FDI', 'FDI or likely FDI')], default='DEFAULT', max_length=255, verbose_name='Enquiry quality'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='region',
            field=models.CharField(choices=[('DEFAULT', '----'), ('AMERICAS', 'Americas'), ('APAC', 'Asia-Pacific'), ('EMEA', 'EMEA')], default='DEFAULT', max_length=255, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='second_hpo_selection',
            field=models.CharField(choices=[('DEFAULT', '----'), ('FOOD_PRODUCTION', 'Food production'), ('UK_RAIL', 'UK rail'), ('LIGHTWEIGHT_STRUCTURES', 'Lightweight structures')], default='DEFAULT', max_length=255, verbose_name='Second HPO selection'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='specific_investment_programme',
            field=models.CharField(choices=[('ADVANCED_ENG', 'Advanced Engineering Supply Chain'), ('BUSINESS_PARTNER', 'Business Partnership (Non-FDI)'), ('CONTRACT_RESEARCH', 'Contract Research (Non-FDI)'), ('FDI_CAPITAL_ONLY', 'FDI (Capital Only)'), ('GREAT_INV_PROG', 'GREAT Investors Programme'), ('GLOBAL_ENTREP_PROG', 'Global Entrepreneur Programme'), ('GRADUATE_ENTREP_PROG', 'Graduate Entrepreneur Programme'), ('HQ_UK', 'HQ-UK'), ('II&I', 'II&I Programme'), ('INFRASTRUCTURE_GATEWAY', 'Infrastructure Gateway'), ('IIGB', 'Invest in Great Britain'), ('NO_SPECIFIC_PROG', 'No Specific Programme'), ('R&D_COLLAB', 'R&D Collaboration (Non-FDI)'), ('R&D_PARTNERSHIP', 'R&D Partnership (Non-FDI)'), ('R&D_PROG', 'R&D Prog (Obsolete)'), ('REGENERATION', 'Regeneration Investment Organisation (RIO)'), ('SRM', 'SRM Programme'), ('SCREEN', 'Screen Production Investment'), ('SIRIUS', 'Sirius (Graduate Entrepreneurs)'), ('SPACE', 'Space'), ('UNIVERSITY_COLLAB', 'University Collaboration (Non-FDI)'), ('VENTURE_CAPITAL', 'Venture / Equity Captial')], default='IIGB', max_length=255, verbose_name='Specific investment programme'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='third_hpo_selection',
            field=models.CharField(choices=[('DEFAULT', '----'), ('FOOD_PRODUCTION', 'Food production'), ('UK_RAIL', 'UK rail'), ('LIGHTWEIGHT_STRUCTURES', 'Lightweight structures')], default='DEFAULT', max_length=255, verbose_name='Third HPO selection'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Website'),
        ),
    ]
