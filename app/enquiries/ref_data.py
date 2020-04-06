from django.db import models
from django.utils.translation import gettext_lazy as _


class EnquiryStage(models.TextChoices):
    NEW = "NEW", _("New")
    AWAITING_RESPONSE = "AWAITING_RESPONSE", _("Awaiting response from Investor")
    ENGAGED = "ENGAGED", _("Engaged in dialogue")
    NON_RESPONSIVE = "NON_RESPONSIVE", _("Non-responsive")
    NON_FDI = "NON_FDI", _("Non-FDI")
    ADDED_TO_DATAHUB = "ADDED_TO_DATAHUB", _("Added to Data Hub")
    SENT_TO_POST = "SENT_TO_POST", _("Sent to Post")
    POST_PROGRESSING = "POST_PROGRESSING", _("Post progressing")


class InvestmentReadiness(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    CONVINCED = (
        "CONVINCED",
        _("I’m convinced and want to talk to someone about my plans"),
    )
    SHORTLIST = (
        "SHORTLIST",
        _(
            "The UK is on my shortlist. How can the Department for International Trade help me?"
        ),
    )
    EXPLORING = (
        "EXPLORING",
        _(
            "I’m still exploring where to expand my business and would like to know more about the UK’s offer"
        ),
    )
    NOT_READY = "NOT_READY", _("I’m not yet ready to invest. Keep me informed")


class Quality(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    NON_APPLICABLE = "NON_APPLICABLE", _("Non-applicable")
    NON_FDI = "NON_FDI", _("Non-FDI")
    POTENTIALLY_NON_FDI = "POTENTIALLY_NON_FDI", _("Potentially Non-FDI")
    POTENTIALLY_FDI = "POTENTIALLY_FDI", _("Potentially FDI")
    LIKELY_FDI = "LIKELY_FDI", _("FDI or likely FDI")


class MarketingChannel(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    LINKEDIN = "LINKEDIN", _("LinkedInLeadGen")
    CHOGM = "CHOGM", _("CHOGM")
    IIGB = "IIGB", _("IiGB")
    IIGB_LINKEDIN = "IIGB_LINKEDIN", _("IiGB (LinkedIn)")
    HPO = "HPO", _("HPO")
    B2B = "B2B", _("B2B")
    EBOOK = "EBOOK", _("EBOOK - Worldwide")
    TRA = "TRA", _("TRA")
    ENCORE = "ENCORE", _("Encore")
    OTHER = "OTHER", _("Other")


class HowDidTheyHear(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    PRESS_AD = "PRESS_AD", _("Press ad (newspaper/trade publication")
    OUTDOOR_AD = "OUTDOOR_AD", _("Outdoor ad/billboard")
    LINKEDIN = "LINKEDIN", _("LinkedIn")
    SOCIAL_MEDIA = "SOCIAL_MEDIA", _("Other social media (e.g. Twitter/Facebook)")
    INTERNET_SEARCH = "INTERNET_SEARCH", _("Internet search")
    OTHER = "OTHER", _("Other")


class PrimarySector(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    ADVANCED_ENG = "ADVANCED_ENG", _("Advanced Engineering")
    AEROSPACE = "AEROSPACE", _("Aerospace")
    AGRICULTURE = "AGRICULTURE", _("Agriculture, Horticulture, Fisheries and Pets")
    AIRPORTS = "AIRPORTS", _("Airports")
    AUTOMOTIVE = "AUTOMOTIVE", _("Automotive")
    CHEMICALS = "CHEMICALS", _("Chemicals")
    CONSTRUCTION = "CONSTRUCTION", _("Construction")
    CONSUMER = "CONSUMER", _("Consumer and Retail")
    CREATIVE = "CREATIVE", _("Creative Industries")
    CYBER = "CYBER", _("Cyber Security")
    DEFENCE = "DEFENCE", _("Defence")
    EDUCATION = "EDUCATION", _("Education and Training")
    ENERGY = "ENERGY", _("Energy")
    ENVIRONMENT = "ENVIRONMENT", _("Environment")
    FINANCIAL = "FINANCIAL", _("Financial and Professional Services")
    FOOD = "FOOD", _("Food and Drink")
    HEALTHCARE = "HEALTHCARE", _("Healthcare Services")
    MARITIME = "MARITIME", _("Maritime")
    MEDICAL = "MEDICAL", _("Medical Devices and Equipment")
    MINING = "MINING", _("Mining")
    PHARMACEUTICALS = "PHARMACEUTICALS", _("Pharmaceuticals and Biotechnology")
    RAILWAYS = "RAILWAYS", _("Railways")
    SECURITY = "SECURITY", _("Security")
    SPACE = "SPACE", _("Space")
    SPORTS = "SPORTS", _("Sports Economy")
    TECHNOLOGY = "TECHNOLOGY", _("Technology and Smart Cities")
    WATER = "WATER", _("Water")


class IstSector(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    ITECH = "ITECH", _("ITECH")
    LIFE = "LIFE", _("Life Science")
    ENERGY = "ENERGY", _("Energy and Environment")
    BPFS = "BPFS", _("BPFS")
    AEM = "AEM", _("AEM")
    UNCLASSIFIED = "UNCLASSIFIED", _("Unclassified")


class Country(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    AFGHANISTAN = "AFGHANISTAN", _("Afghanistan")
    ALBANIA = "ALBANIA", _("Albania")
    ALGERIA = "ALGERIA", _("Algeria")
    ANDORRA = "ANDORRA", _("Andorra")
    ANGOLA = "ANGOLA", _("Angola")
    ANTIGUA = "ANTIGUA", _("Antigua and Barbuda")
    ARGENTINA = "ARGENTINA", _("Argentina")
    ARMENIA = "ARMENIA", _("Armenia")
    AUSTRALIA = "AUSTRALIA", _("Australia")
    AUSTRIA = "AUSTRIA", _("Austria")
    AZERBAIJAN = "AZERBAIJAN", _("Azerbaijan")
    BAHRAIN = "BAHRAIN", _("Bahrain")
    BANGLADESH = "BANGLADESH", _("Bangladesh")
    BARBADOS = "BARBADOS", _("Barbados")
    BELARUS = "BELARUS", _("Belarus")
    BELGIUM = "BELGIUM", _("Belgium")
    BELIZE = "BELIZE", _("Belize")
    BENIN = "BENIN", _("Benin")
    BHUTAN = "BHUTAN", _("Bhutan")
    BOLIVIA = "BOLIVIA", _("Bolivia")
    BOSNIA = "BOSNIA", _("Bosnia and Herzegovina")
    BOTSWANA = "BOTSWANA", _("Botswana")
    BRAZIL = "BRAZIL", _("Brazil")
    BRUNEI = "BRUNEI", _("Brunei")
    BULGARIA = "BULGARIA", _("Bulgaria")
    BURKINA = "BURKINA", _("Burkina Faso")
    BURUNDI = "BURUNDI", _("Burundi")
    CAMBODIA = "CAMBODIA", _("Cambodia")
    CAMEROON = "CAMEROON", _("Cameroon")
    CANADA = "CANADA", _("Canada")
    CAPE = "CAPE", _("Cape Verde")
    CENTRAL_AFRICA = "CENTRAL_AFRICA", _("Central African Republic")
    CHAD = "CHAD", _("Chad")
    CHILE = "CHILE", _("Chile")
    CHINA = "CHINA", _("China")
    COLOMBIA = "COLOMBIA", _("Colombia")
    COMOROS = "COMOROS", _("Comoros")
    CONGO = "CONGO", _("Congo")
    CONGO_DR = "CONGO_DR", _("Congo (Democratic Republic)")
    COSTA = "COSTA", _("Costa Rica")
    CROATIA = "CROATIA", _("Croatia")
    CUBA = "CUBA", _("Cuba")
    CYPRUS = "CYPRUS", _("Cyprus")
    CZECHIA = "CZECHIA", _("Czechia")
    DENMARK = "DENMARK", _("Denmark")
    DJIBOUTI = "DJIBOUTI", _("Djibouti")
    DOMINICA = "DOMINICA", _("Dominica")
    DOMINICAN = "DOMINICAN", _("Dominican Republic")
    EAST_TIMOR = "EAST_TIMOR", _("East Timor")
    ECUADOR = "ECUADOR", _("Ecuador")
    EGYPT = "EGYPT", _("Egypt")
    EL_SALVADOR = "EL_SALVADOR", _("El Salvador")
    EQUATORIAL_GUINEA = "EQUATORIAL_GUINEA", _("Equatorial Guinea")
    ERITREA = "ERITREA", _("Eritrea")
    ESTONIA = "ESTONIA", _("Estonia")
    ESWATINI = "ESWATINI", _("Eswatini")
    ETHIOPIA = "ETHIOPIA", _("Ethiopia")
    FIJI = "FIJI", _("Fiji")
    FINLAND = "FINLAND", _("Finland")
    FRANCE = "FRANCE", _("France")
    GABON = "GABON", _("Gabon")
    GEORGIA = "GEORGIA", _("Georgia")
    GERMANY = "GERMANY", _("Germany")
    GHANA = "GHANA", _("Ghana")
    GREECE = "GREECE", _("Greece")
    GRENADA = "GRENADA", _("Grenada")
    GUATEMALA = "GUATEMALA", _("Guatemala")
    GUINEA = "GUINEA", _("Guinea")
    GUINEA_BISSAU = "GUINEA_BISSAU", _("Guinea-Bissau")
    GUYANA = "GUYANA", _("Guyana")
    HAITI = "HAITI", _("Haiti")
    HONDURAS = "HONDURAS", _("Honduras")
    HUNGARY = "HUNGARY", _("Hungary")
    ICELAND = "ICELAND", _("Iceland")
    INDIA = "INDIA", _("India")
    INDONESIA = "INDONESIA", _("Indonesia")
    IRAN = "IRAN", _("Iran")
    IRAQ = "IRAQ", _("Iraq")
    IRELAND = "IRELAND", _("Ireland")
    ISRAEL = "ISRAEL", _("Israel")
    ITALY = "ITALY", _("Italy")
    IVORY = "IVORY", _("Ivory Coast")
    JAMAICA = "JAMAICA", _("Jamaica")
    JAPAN = "JAPAN", _("Japan")
    JORDAN = "JORDAN", _("Jordan")
    KAZAKHSTAN = "KAZAKHSTAN", _("Kazakhstan")
    KENYA = "KENYA", _("Kenya")
    KIRIBATI = "KIRIBATI", _("Kiribati")
    KOSOVO = "KOSOVO", _("Kosovo")
    KUWAIT = "KUWAIT", _("Kuwait")
    KYRGYZSTAN = "KYRGYZSTAN", _("Kyrgyzstan")
    LAOS = "LAOS", _("Laos")
    LATVIA = "LATVIA", _("Latvia")
    LEBANON = "LEBANON", _("Lebanon")
    LESOTHO = "LESOTHO", _("Lesotho")
    LIBERIA = "LIBERIA", _("Liberia")
    LIBYA = "LIBYA", _("Libya")
    LIECHTENSTEIN = "LIECHTENSTEIN", _("Liechtenstein")
    LITHUANIA = "LITHUANIA", _("Lithuania")
    LUXEMBOURG = "LUXEMBOURG", _("Luxembourg")
    MADAGASCAR = "MADAGASCAR", _("Madagascar")
    MALAWI = "MALAWI", _("Malawi")
    MALAYSIA = "MALAYSIA", _("Malaysia")
    MALDIVES = "MALDIVES", _("Maldives")
    MALI = "MALI", _("Mali")
    MALTA = "MALTA", _("Malta")
    MARSHALL = "MARSHALL", _("Marshall Islands")
    MAURITANIA = "MAURITANIA", _("Mauritania")
    MAURITIUS = "MAURITIUS", _("Mauritius")
    MEXICO = "MEXICO", _("Mexico")
    MICRONESIA = "MICRONESIA", _("Micronesia")
    MOLDOVA = "MOLDOVA", _("Moldova")
    MONACO = "MONACO", _("Monaco")
    MONGOLIA = "MONGOLIA", _("Mongolia")
    MONTENEGRO = "MONTENEGRO", _("Montenegro")
    MOROCCO = "MOROCCO", _("Morocco")
    MOZAMBIQUE = "MOZAMBIQUE", _("Mozambique")
    MYANMAR = "MYANMAR", _("Myanmar (Burma)")
    NAMIBIA = "NAMIBIA", _("Namibia")
    NAURU = "NAURU", _("Nauru")
    NEPAL = "NEPAL", _("Nepal")
    NETHERLANDS = "NETHERLANDS", _("Netherlands")
    NEW = "NEW", _("New Zealand")
    NICARAGUA = "NICARAGUA", _("Nicaragua")
    NIGER = "NIGER", _("Niger")
    NIGERIA = "NIGERIA", _("Nigeria")
    NORTH_KOREA = "NORTH_KOREA", _("North Korea")
    NORTH_MACEDONIA = "NORTH_MACEDONIA", _("North Macedonia")
    NORWAY = "NORWAY", _("Norway")
    OMAN = "OMAN", _("Oman")
    PAKISTAN = "PAKISTAN", _("Pakistan")
    PALAU = "PALAU", _("Palau")
    PANAMA = "PANAMA", _("Panama")
    PAPUA = "PAPUA", _("Papua New Guinea")
    PARAGUAY = "PARAGUAY", _("Paraguay")
    PERU = "PERU", _("Peru")
    PHILIPPINES = "PHILIPPINES", _("Philippines")
    POLAND = "POLAND", _("Poland")
    PORTUGAL = "PORTUGAL", _("Portugal")
    QATAR = "QATAR", _("Qatar")
    ROMANIA = "ROMANIA", _("Romania")
    RUSSIA = "RUSSIA", _("Russia")
    RWANDA = "RWANDA", _("Rwanda")
    SAMOA = "SAMOA", _("Samoa")
    SAN = "SAN", _("San Marino")
    SAO = "SAO", _("Sao Tome and Principe")
    SAUDI = "SAUDI", _("Saudi Arabia")
    SENEGAL = "SENEGAL", _("Senegal")
    SERBIA = "SERBIA", _("Serbia")
    SEYCHELLES = "SEYCHELLES", _("Seychelles")
    SIERRA = "SIERRA", _("Sierra Leone")
    SINGAPORE = "SINGAPORE", _("Singapore")
    SLOVAKIA = "SLOVAKIA", _("Slovakia")
    SLOVENIA = "SLOVENIA", _("Slovenia")
    SOLOMON = "SOLOMON", _("Solomon Islands")
    SOMALIA = "SOMALIA", _("Somalia")
    SOUTH_AFRICA = "SOUTH_AFRICA", _("South Africa")
    SOUTH_KOREA = "SOUTH_KOREA", _("South Korea")
    SOUTH_SUDAN = "SOUTH_SUDAN", _("South Sudan")
    SPAIN = "SPAIN", _("Spain")
    SRI_LANKA = "SRI_LANKA", _("Sri Lanka")
    STKITTS = "STKITTS", _("St Kitts and Nevis")
    STLUCIA = "STLUCIA", _("St Lucia")
    STVINCENT = "STVINCENT", _("St Vincent")
    SUDAN = "SUDAN", _("Sudan")
    SURINAME = "SURINAME", _("Suriname")
    SWEDEN = "SWEDEN", _("Sweden")
    SWITZERLAND = "SWITZERLAND", _("Switzerland")
    SYRIA = "SYRIA", _("Syria")
    TAJIKISTAN = "TAJIKISTAN", _("Tajikistan")
    TANZANIA = "TANZANIA", _("Tanzania")
    THAILAND = "THAILAND", _("Thailand")
    BAHAMAS = "BAHAMAS", _("The Bahamas")
    GAMBIA = "GAMBIA", _("The Gambia")
    TOGO = "TOGO", _("Togo")
    TONGA = "TONGA", _("Tonga")
    TRINIDAD = "TRINIDAD", _("Trinidad and Tobago")
    TUNISIA = "TUNISIA", _("Tunisia")
    TURKEY = "TURKEY", _("Turkey")
    TURKMENISTAN = "TURKMENISTAN", _("Turkmenistan")
    TUVALU = "TUVALU", _("Tuvalu")
    UGANDA = "UGANDA", _("Uganda")
    UKRAINE = "UKRAINE", _("Ukraine")
    UAE = "UAE", _("United Arab Emirates")
    UK = "UK", _("United Kingdom")
    US = "US", _("United States")
    URUGUAY = "URUGUAY", _("Uruguay")
    UZBEKISTAN = "UZBEKISTAN", _("Uzbekistan")
    VANUATU = "VANUATU", _("Vanuatu")
    VATICAN = "VATICAN", _("Vatican City")
    VENEZUELA = "VENEZUELA", _("Venezuela")
    VIETNAM = "VIETNAM", _("Vietnam")
    YEMEN = "YEMEN", _("Yemen")
    ZAMBIA = "ZAMBIA", _("Zambia")
    ZIMBABWE = "ZIMBABWE", _("Zimbabwe")


class Region(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    AMERICAS = "AMERICAS", _("Americas")
    APAC = "APAC", _("Asia-Pacific")
    EMEA = "EMEA", _("EMEA")


class RequestForCall(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    YES_MORNING = "YES_MORNING", _("Yes - morning")
    YES_AFTERNOON = "YES_AFTERNOON", _("Yes - afternoon")
    YES_OTHER = "YES_OTHER", _("Yes - other")
    NO = "NO", _("No")


class FirstResponseChannel(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    CALL = "CALL", _("Call")
    EMAIL = "EMAIL", _("Email")
    NOT_RESPONDED = "NOT_RESPONDED", _("Not yet responded")


class HpoSelection(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    FOOD_PRODUCTION = "FOOD_PRODUCTION", _("Food production")
    UK_RAIL = "UK_RAIL", _("UK rail")
    LIGHTWEIGHT_STRUCTURES = "LIGHTWEIGHT_STRUCTURES", _("Lightweight structures")


class OrganisationType(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    CHARITY = "CHARITY,", _("Charity")
    GOVERNMENT = "GOVERNMENT", _("Government department or other public body")
    LIMITED_COMPANY = "LIMITED_COMPANY", _("Limited company")
    LIMITED_PARTNERSHIP = "LIMITED_PARTNERSHIP", _("Limited partnership")
    PARTNERSHIP = "PARTNERSHIP,", _("Partnership")
    SOLE_TRADER = "SOLE_TRADER", _("Sole trader")


class InvestmentType(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    ACQUISITION = "ACQUISITION", _("Acquisition")
    CAPITAL_ONLY = "CAPITAL_ONLY", _("Capital only")
    NEW_SITE = "NEW_SITE", _("Creation of new site or activity")
    EXPANSION = "EXPANSION", _("Expansion of existing site or activity")
    JOINT_VENTURE = "JOINT_VENTURE", _("Joint venture")
    MERGER = "MERGER", _("Merger")
    RETENTION = "RETENTION", _("Retention")
    NOT_SPECIFIED = "NOT_SPECIFIED", _("Not specified")


class NewExistingInvestor(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    NEW = "NEW", _("New investor")
    EXISTING = "EXISTING", _("Existing investor")


class InvestorInvolvement(models.TextChoices):
    FDI_HUB_HQ = "FDI_HUB_HQ", _("FDI Hub + HQ")
    FDI_HUB_HQ_LEP = "FDI_HUB_HQ_LEP", _("FDI Hub + HQ + LEP")
    FDI_HUB_HQ_POST_LEP = "FDI_HUB_HQ_POST_LEP", _("FDI Hub + HQ + Post + LEP")
    FDI_HUB_HQ_POST_REG = "FDI_HUB_HQ_POST_REG", _("FDI Hub + HQ + Post + Reg")
    FDI_HUB_HQ_REG = "FDI_HUB_HQ_REG", _("FDI Hub + HQ  + Reg")
    FDI_HUB_LEP = "FDI_HUB_LEP", _("FDI Hub + LEP")
    FDI_HUB_POST = "FDI_HUB_POST", _("FDI Hub + Post")
    FDI_HUB_POST_HQ = "FDI_HUB_POST_HQ", _("FDI Hub + Post + HQ")
    FDI_HUB_POST_LEP = "FDI_HUB_POST_LEP", _("FDI Hub + Post + LEP")
    FDI_HUB_POST_REG = "FDI_HUB_POST_REG", _("FDI Hub + Post + Reg")
    FDI_HUB_REGION = "FDI_HUB_REGION", _("FDI Hub + Region")
    FDI_HUB_ONLY = "FDI_HUB_ONLY", _("FDI Hub Only")
    HQ_LEP = "HQ_LEP", _("HQ + LEP")
    HQ_POST_LEP = "HQ_POST_LEP", _("HQ + Post + LEP")
    HQ_ONLY = "HQ_ONLY", _("HQ Only")
    HQ_POST_ONLY = "HQ_POST_ONLY", _("HQ and Post Only")
    HQ_REGION = "HQ_REGION", _("HQ and Region")
    HQ_POST_REGION = "HQ_POST_REGION,", _("HQ, Post and Region")
    LEP_ONLY = "LEP_ONLY", _("LEP Only")
    NO_INVOLVEMENT = "NO_INVOLVEMENT", _("No involvement")
    POST_LEP = "POST_LEP", _("Post + LEP")
    POST_ONLY = "POST_ONLY", _("Post Only")
    POST_REGION = "POST_REGION", _("Post and Region")
    REGION_ONLY = "REGION_ONLY", _("Region Only")


class InvestmentProgramme(models.TextChoices):
    ADVANCED_ENG = "ADVANCED_ENG", _("Advanced Engineering Supply Chain")
    BUSINESS_PARTNER = "BUSINESS_PARTNER", _("Business Partnership (Non-FDI)")
    CONTRACT_RESEARCH = "CONTRACT_RESEARCH", _("Contract Research (Non-FDI)")
    FDI_CAPITAL_ONLY = "FDI_CAPITAL_ONLY", _("FDI (Capital Only)")
    GREAT_INV_PROG = "GREAT_INV_PROG", _("GREAT Investors Programme")
    GLOBAL_ENTREP_PROG = "GLOBAL_ENTREP_PROG", _("Global Entrepreneur Programme")
    GRADUATE_ENTREP_PROG = "GRADUATE_ENTREP_PROG", _("Graduate Entrepreneur Programme")
    HQ_UK = "HQ_UK", _("HQ-UK")
    II_AND_I = "II&I", _("II&I Programme")
    INFRASTRUCTURE_GATEWAY = "INFRASTRUCTURE_GATEWAY", _("Infrastructure Gateway")
    IIGB = "IIGB", _("Invest in Great Britain")
    NO_SPECIFIC_PROG = "NO_SPECIFIC_PROG", _("No Specific Programme")
    RD_COLLAB = "R&D_COLLAB", _("R&D Collaboration (Non-FDI)")
    RD_PARTNERSHIP = "R&D_PARTNERSHIP", _("R&D Partnership (Non-FDI)")
    RD_PROG = "R&D_PROG", _("R&D Prog (Obsolete)")
    REGENERATION = "REGENERATION", _("Regeneration Investment Organisation (RIO)")
    SRM = "SRM", _("SRM Programme")
    SCREEN = "SCREEN", _("Screen Production Investment")
    SIRIUS = "SIRIUS", _("Sirius (Graduate Entrepreneurs)")
    SPACE = "SPACE", _("Space")
    UNIVERSITY_COLLAB = "UNIVERSITY_COLLAB", _("University Collaboration (Non-FDI)")
    VENTURE_CAPITAL = "VENTURE_CAPITAL", _("Venture / Equity Captial")


class DatahubProjectStatus(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    PROSPECT = "PROSPECT", _("Prospect")
    ASSIGN = "ASSIGN", _("Assign PM")
    ACTIVE = "ACTIVE", _("Active")
    VERIFY = "VERIFY", _("Verify Win")
    WON = "WON", _("Won")
    ABANDONED = "ABANDONED", _("Abandoned")
    DELAYED = "DELAYED", _("Delayed")


IMPORT_COL_NAMES = [
    "enquirer_first_name",
    "enquirer_last_name",
    "enquirer_job_title",
    "enquirer_email",
    "enquirer_phone",
    "enquirer_request_for_call",
    "country",
    "company_name",
    "primary_sector",
    "company_hq_address",
    "website",
    "investment_readiness",
    "enquiry_text",
    "notes",
]

MAP_ENQUIRY_FIELD_TO_REF_DATA = {
    "enquiry_stage": EnquiryStage,
    "investment_readiness": InvestmentReadiness,
    "quality": Quality,
    "marketing_channel": MarketingChannel,
    "how_they_heard_dit": HowDidTheyHear,
    "primary_sector": PrimarySector,
    "country": Country,
    "first_response_channel": FirstResponseChannel,
    "ist_sector": IstSector,
    "first_hpo_selection": HpoSelection,
    "region": Region,
    "second_hpo_selection": HpoSelection,
    "third_hpo_selection": HpoSelection,
    "organisation_type": OrganisationType,
    "investment_type": InvestmentType,
    "new_existing_investor": NewExistingInvestor,
    "investor_involvement_level": InvestorInvolvement,
    "specific_investment_programme": InvestmentProgramme,
    "datahub_project_status": DatahubProjectStatus,
}
