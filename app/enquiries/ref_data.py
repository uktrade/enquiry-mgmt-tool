<<<<<<< HEAD
from django.db import models
from django.utils.translation import gettext_lazy as _


class EnquiryStage(models.TextChoices):
    NEW = "NEW", _("New")
    AWAITING_RESPONSE = "AWAITING_RESPONSE", _("Awaiting response from Investor")
    NON_RESPONSIVE = "NON_RESPONSIVE", _("Non-responsive")
    NON_FDI = "NON_FDI", _("Non-FDI")
    ADDED_TO_DATAHUB = "ADDED_TO_DATAHUB", _("Added to Data Hub")
    SENT_TO_POST = "SENT_TO_POST", _("Sent to Post")
    POST_PROGRESSING = "POST_PROGRESSING", _("Post progressing")


class InvestmentReadiness(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    CONVINCED = "CONVINCED", _("I’m convinced and want to talk to someone about my plans")
    SHORTLIST = "SHORTLIST", _("The UK is on my shortlist. How can the Department for International Trade help me?")
    EXPLORING = "EXPLORING", _("I’m still exploring where to expand my business and would like to know more about the UK’s offer")
    NOT_READY = "NOT_READY", _("I’m not yet ready to invest. Keep me informed")


class Quality(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    NON_APPLICABLE = "NON_APPLICABLE", _("Non-applicable")
    NON_FDI = "NON_FDI", _("Non-FDI")
    POTENTIALLY_NON_FDI = "POTENTIALLY_NON_FDI", _("Potentially Non-FDI")
    POTENTIALLY_FDI = "POTENTIALLY_FDI", _("Potentially FDI")
    LIKELY_FDI = "LIKELY_FDI", _("Likely to be FDI")


class MarketingChannel(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    LINKEDIN = "LINKEDIN", _("LinkedInLeadGen")
    CHOGM = "CHOGM", _("CHOGM")
    IIGB = "IIGB", _("IiGB")
    IIGB_LINKEDIN = "IIGB_LINKEDIN", _("IiGB (LinkedIN)")
    HPO = "HPO", _("HPO")
    B2B = "B2B", _("B2B")
    EBOOK = "EBOOK", _("EBOOK - Worldwide")
    TRA = "TRA", _("TRA")
    ENCORE = "ENCORE", _("Encore")
    OTHER = "OTHER", _("Other")


class HowDidTheyHear(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    PRESS_AD = "PRESS_AD", _("Press ad (newspapaer/trade publication")
    OUTDOOR_AD = "OUTDOOR_AD", _("Outdoor ad/billboard")
    LINKEDIN = "LINKEDIN", _("LinkedIn")
    SOCIAL_MEDIA = "SOCIAL_MEDIA", _("Other social media (e.g. Twitter/Facebook)")
    INTERNET_SEARCH = "INTERNET_SEARCH", _("Internet Search")
    OTHER = "OTHER", _("Other")


class PrimarySector(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    ADVANCED_ENG = "ADVANCED_ENG", _("Advanced Engineering")
    AEROSPACE = "AEROSPACE", _("Aerospace")
    AGRICULTURE = "AGRICULTURE,", _("Agriculture, Horticulture, Fisheries and Pets")
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
    APAC = "APAC", _("Asia Pacific")
    EMEA = "EMEA", _("Europe and Middle East")


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
    CHARITY = "CHARITY,", _("charity")
    GOVERNMENT = "GOVERNMENT", _("gov department or other public body")
    LIMITED_COMPANY = "LIMITED_COMPANY", _("limited company")
    LIMITED_PARTNERSHIP = "LIMITED_PARTNERSHIP", _("limited partnership")
    PARTNERSHIP = "PARTNERSHIP,", _("partnership")
    SOLE_TRADER = "SOLE_TRADER", _("sole trader")


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
    NEW = "NEW,", _("New Investor")
    EXISTING = "EXISTING,", _("Existing Investor")


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
    GLOBAL_ENTERP_PROG = "GLOBAL_ENTERP_PROG", _("Global Entrepreneur Programme")
    GRADUATE_ENTERP_PROG = "GRADUATE_ENTERP_PROG", _("Graduate Entrepreneur Programme")
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
=======
from modelchoices import Choices


class EnquiryStage(Choices):
    NEW = ("NEW", "New")
    AWAITING_RESPONSE = ("AWAITING_RESPONSE", "Awaiting response from Investor")
    NON_RESPONSIVE = ("NON_RESPONSIVE", "Non-responsive")
    NON_FDI = ("NON_FDI", "Non-FDI")
    ADDED_TO_DATAHUB = ("ADDED_TO_DATAHUB", "Added to Data Hub")
    SENT_TO_POST = ("SENT_TO_POST", "Sent to Post")
    POST_PROGRESSING = ("POST_PROGRESSING", "Post progressing")


class InvestmentReadiness(Choices):
    DEFAULT = ("DEFAULT", "----")
    CONVINCED = (
        "CONVINCED",
        "I’m convinced and want to talk to someone about my plans",
    )
    SHORTLIST = (
        "SHORTLIST",
        "The UK is on my shortlist. How can the Department for International Trade help me?",
    )
    EXPLORING = (
        "EXPLORING",
        "I’m still exploring where to expand my business and would like to know more about the UK’s offer",
    )
    NOT_READY = ("NOT_READY", "I’m not yet ready to invest. Keep me informed")


class Quality(Choices):
    DEFAULT = ("DEFAULT", "----")
    JUNK = ("JUNK", "Junk")
    NON_FDI = ("NON_FDI", "Non-FDI / Potentially Non-FDI")
    POTENTIAL_FDI = ("POTENTIAL_FDI", "Potentially FDI")
    LIKELY_FDI = ("LIKELY_FDI", "FDI / likely FDI")


class MarketingChannel(Choices):
    DEFAULT = ("DEFAULT", "----")
    LINKEDIN = ("LINKEDIN", "LinkedInLeadGen")
    CHOGM = ("CHOGM", "CHOGM")
    IIGB = ("IIGB", "IiGB")
    IIGB_LINKEDIN = ("IIGB_LINKEDIN", "IiGB (LinkedIn)")
    HPO = ("HPO", "HPO")
    B2B = ("B2B", "B2B")
    EBOOK = ("EBOOK", "EBOOK - Worldwide")
    TRA = ("TRA", "TRA")
    ENCORE = ("ENCORE", "Encore")
    OTHER = ("OTHER", "Other")


class HowDidTheyHear(Choices):
    DEFAULT = ("DEFAULT", "----")
    PRESS_AD = ("PRESS_AD", "Press ad (newspaper/trade publication")
    OUTDOOR_AD = ("OUTDOOR_AD", "Outdoor ad/billboard")
    LINKEDIN = ("LINKEDIN", "LinkedIn")
    SOCIAL_MEDIA = ("SOCIAL_MEDIA", "Other social media (e.g. Twitter/Facebook)")
    INTERNET_SEARCH = ("INTERNET_SEARCH", "Internet search")
    OTHER = ("OTHER", "Other")


class PrimarySector(Choices):
    DEFAULT = ("DEFAULT", "----")
    ADVANCED_ENG = ("ADVANCED_ENG", "Advanced Engineering")
    AEROSPACE = ("AEROSPACE", "Aerospace")
    AGRICULTURE = ("AGRICULTURE,", "Agriculture, Horticulture, Fisheries & Pets")
    AIRPORTS = ("AIRPORTS", "Airports")
    AUTOMOTIVE = ("AUTOMOTIVE", "Automotive")
    CHEMICALS = ("CHEMICALS", "Chemicals")
    CONSTRUCTION = ("CONSTRUCTION", "Construction")
    CONSUMER = ("CONSUMER", "Consumer & Retail")
    CREATIVE = ("CREATIVE", "Creative Industries")
    CYBER = ("CYBER", "Cyber Security")
    DEFENCE = ("DEFENCE", "Defence")
    EDUCATION = ("EDUCATION", "Education & Training")
    ENERGY = ("ENERGY", "Energy")
    ENVIRONMENT = ("ENVIRONMENT", "Environment")
    FINANCIAL = ("FINANCIAL", "Financial & Professional Services")
    FOOD = ("FOOD", "Food & Drink")
    HEALTHCARE = ("HEALTHCARE", "Healthcare Services")
    MARITIME = ("MARITIME", "Maritime")
    MEDICAL = ("MEDICAL", "Medical Devices & Equipment")
    MINING = ("MINING", "Mining")
    PHARMACEUTICALS = ("PHARMACEUTICALS", "Pharmaceuticals & Biotechnology")
    RAILWAYS = ("RAILWAYS", "Railways")
    SECURITY = ("SECURITY", "Security")
    SPACE = ("SPACE", "Space")
    SPORTS = ("SPORTS", "Sports Economy")
    TECHNOLOGY = ("TECHNOLOGY", "Technology & Smart Cities")
    WATER = ("WATER", "Water")


class IstSector(Choices):
    DEFAULT = ("DEFAULT", "----")
    ITECH = ("ITECH", "ITECH")
    LIFE = ("LIFE", "Life Science")
    ENERGY = ("ENERGY", "Energy & Environment")
    BPFS = ("BPFS", "BPFS")
    AEM = ("AEM", "AEM")
    UNCLASSIFIED = ("UNCLASSIFIED", "Unclassified")


class Country(Choices):
    DEFAULT = ("DEFAULT", "----")
    AFGHANISTAN = ("AFGHANISTAN", "Afghanistan")
    ALBANIA = ("ALBANIA", "Albania")
    ALGERIA = ("ALGERIA", "Algeria")
    ANDORRA = ("ANDORRA", "Andorra")
    ANGOLA = ("ANGOLA", "Angola")
    ANTIGUA = ("ANTIGUA", "Antigua and Barbuda")
    ARGENTINA = ("ARGENTINA", "Argentina")
    ARMENIA = ("ARMENIA", "Armenia")
    AUSTRALIA = ("AUSTRALIA", "Australia")
    AUSTRIA = ("AUSTRIA", "Austria")
    AZERBAIJAN = ("AZERBAIJAN", "Azerbaijan")
    BAHRAIN = ("BAHRAIN", "Bahrain")
    BANGLADESH = ("BANGLADESH", "Bangladesh")
    BARBADOS = ("BARBADOS", "Barbados")
    BELARUS = ("BELARUS", "Belarus")
    BELGIUM = ("BELGIUM", "Belgium")
    BELIZE = ("BELIZE", "Belize")
    BENIN = ("BENIN", "Benin")
    BHUTAN = ("BHUTAN", "Bhutan")
    BOLIVIA = ("BOLIVIA", "Bolivia")
    BOSNIA = ("BOSNIA", "Bosnia and Herzegovina")
    BOTSWANA = ("BOTSWANA", "Botswana")
    BRAZIL = ("BRAZIL", "Brazil")
    BRUNEI = ("BRUNEI", "Brunei")
    BULGARIA = ("BULGARIA", "Bulgaria")
    BURKINA = ("BURKINA", "Burkina Faso")
    BURUNDI = ("BURUNDI", "Burundi")
    CAMBODIA = ("CAMBODIA", "Cambodia")
    CAMEROON = ("CAMEROON", "Cameroon")
    CANADA = ("CANADA", "Canada")
    CAPE = ("CAPE", "Cape Verde")
    CENTRAL_AFRICA = ("CENTRAL_AFRICA", "Central African Republic")
    CHAD = ("CHAD", "Chad")
    CHILE = ("CHILE", "Chile")
    CHINA = ("CHINA", "China")
    COLOMBIA = ("COLOMBIA", "Colombia")
    COMOROS = ("COMOROS", "Comoros")
    CONGO = ("CONGO", "Congo")
    CONGO = ("CONGO", "Congo (Democratic Republic)")
    COSTA = ("COSTA", "Costa Rica")
    CROATIA = ("CROATIA", "Croatia")
    CUBA = ("CUBA", "Cuba")
    CYPRUS = ("CYPRUS", "Cyprus")
    CZECHIA = ("CZECHIA", "Czechia")
    CZECHOSLOVAKIA = ("CZECHOSLOVAKIA", "Czechoslovakia")
    DENMARK = ("DENMARK", "Denmark")
    DJIBOUTI = ("DJIBOUTI", "Djibouti")
    DOMINICA = ("DOMINICA", "Dominica")
    DOMINICAN = ("DOMINICAN", "Dominican Republic")
    EAST_GERMANY = ("EAST_GERMANY", "East Germany")
    EAST_TIMOR = ("EAST_TIMOR", "East Timor")
    ECUADOR = ("ECUADOR", "Ecuador")
    EGYPT = ("EGYPT", "Egypt")
    EL_SALVADOR = ("EL_SALVADOR", "El Salvador")
    GUINEA = ("GUINEA", "Equatorial Guinea")
    ERITREA = ("ERITREA", "Eritrea")
    ESTONIA = ("ESTONIA", "Estonia")
    ESWATINI = ("ESWATINI", "Eswatini")
    ETHIOPIA = ("ETHIOPIA", "Ethiopia")
    FIJI = ("FIJI", "Fiji")
    FINLAND = ("FINLAND", "Finland")
    FRANCE = ("FRANCE", "France")
    GABON = ("GABON", "Gabon")
    GEORGIA = ("GEORGIA", "Georgia")
    GERMANY = ("GERMANY", "Germany")
    GHANA = ("GHANA", "Ghana")
    GREECE = ("GREECE", "Greece")
    GRENADA = ("GRENADA", "Grenada")
    GUATEMALA = ("GUATEMALA", "Guatemala")
    GUINEA = ("GUINEA", "Guinea")
    GUINEA_BISSAU = ("GUINEA_BISSAU", "Guinea-Bissau")
    GUYANA = ("GUYANA", "Guyana")
    HAITI = ("HAITI", "Haiti")
    HONDURAS = ("HONDURAS", "Honduras")
    HUNGARY = ("HUNGARY", "Hungary")
    ICELAND = ("ICELAND", "Iceland")
    INDIA = ("INDIA", "India")
    INDONESIA = ("INDONESIA", "Indonesia")
    IRAN = ("IRAN", "Iran")
    IRAQ = ("IRAQ", "Iraq")
    IRELAND = ("IRELAND", "Ireland")
    ISRAEL = ("ISRAEL", "Israel")
    ITALY = ("ITALY", "Italy")
    IVORY = ("IVORY", "Ivory Coast")
    JAMAICA = ("JAMAICA", "Jamaica")
    JAPAN = ("JAPAN", "Japan")
    JORDAN = ("JORDAN", "Jordan")
    KAZAKHSTAN = ("KAZAKHSTAN", "Kazakhstan")
    KENYA = ("KENYA", "Kenya")
    KIRIBATI = ("KIRIBATI", "Kiribati")
    KOSOVO = ("KOSOVO", "Kosovo")
    KUWAIT = ("KUWAIT", "Kuwait")
    KYRGYZSTAN = ("KYRGYZSTAN", "Kyrgyzstan")
    LAOS = ("LAOS", "Laos")
    LATVIA = ("LATVIA", "Latvia")
    LEBANON = ("LEBANON", "Lebanon")
    LESOTHO = ("LESOTHO", "Lesotho")
    LIBERIA = ("LIBERIA", "Liberia")
    LIBYA = ("LIBYA", "Libya")
    LIECHTENSTEIN = ("LIECHTENSTEIN", "Liechtenstein")
    LITHUANIA = ("LITHUANIA", "Lithuania")
    LUXEMBOURG = ("LUXEMBOURG", "Luxembourg")
    MADAGASCAR = ("MADAGASCAR", "Madagascar")
    MALAWI = ("MALAWI", "Malawi")
    MALAYSIA = ("MALAYSIA", "Malaysia")
    MALDIVES = ("MALDIVES", "Maldives")
    MALI = ("MALI", "Mali")
    MALTA = ("MALTA", "Malta")
    MARSHALL = ("MARSHALL", "Marshall Islands")
    MAURITANIA = ("MAURITANIA", "Mauritania")
    MAURITIUS = ("MAURITIUS", "Mauritius")
    MEXICO = ("MEXICO", "Mexico")
    MICRONESIA = ("MICRONESIA", "Micronesia")
    MOLDOVA = ("MOLDOVA", "Moldova")
    MONACO = ("MONACO", "Monaco")
    MONGOLIA = ("MONGOLIA", "Mongolia")
    MONTENEGRO = ("MONTENEGRO", "Montenegro")
    MOROCCO = ("MOROCCO", "Morocco")
    MOZAMBIQUE = ("MOZAMBIQUE", "Mozambique")
    MYANMAR = ("MYANMAR", "Myanmar (Burma)")
    NAMIBIA = ("NAMIBIA", "Namibia")
    NAURU = ("NAURU", "Nauru")
    NEPAL = ("NEPAL", "Nepal")
    NETHERLANDS = ("NETHERLANDS", "Netherlands")
    NEW = ("NEW", "New Zealand")
    NICARAGUA = ("NICARAGUA", "Nicaragua")
    NIGER = ("NIGER", "Niger")
    NIGERIA = ("NIGERIA", "Nigeria")
    NORTH = ("NORTH", "North Korea")
    NORTH = ("NORTH", "North Macedonia")
    NORWAY = ("NORWAY", "Norway")
    OMAN = ("OMAN", "Oman")
    PAKISTAN = ("PAKISTAN", "Pakistan")
    PALAU = ("PALAU", "Palau")
    PANAMA = ("PANAMA", "Panama")
    PAPUA = ("PAPUA", "Papua New Guinea")
    PARAGUAY = ("PARAGUAY", "Paraguay")
    PERU = ("PERU", "Peru")
    PHILIPPINES = ("PHILIPPINES", "Philippines")
    POLAND = ("POLAND", "Poland")
    PORTUGAL = ("PORTUGAL", "Portugal")
    QATAR = ("QATAR", "Qatar")
    ROMANIA = ("ROMANIA", "Romania")
    RUSSIA = ("RUSSIA", "Russia")
    RWANDA = ("RWANDA", "Rwanda")
    SAMOA = ("SAMOA", "Samoa")
    SAN = ("SAN", "San Marino")
    SAO = ("SAO", "Sao Tome and Principe")
    SAUDI = ("SAUDI", "Saudi Arabia")
    SENEGAL = ("SENEGAL", "Senegal")
    SERBIA = ("SERBIA", "Serbia")
    SEYCHELLES = ("SEYCHELLES", "Seychelles")
    SIERRA = ("SIERRA", "Sierra Leone")
    SINGAPORE = ("SINGAPORE", "Singapore")
    SLOVAKIA = ("SLOVAKIA", "Slovakia")
    SLOVENIA = ("SLOVENIA", "Slovenia")
    SOLOMON = ("SOLOMON", "Solomon Islands")
    SOMALIA = ("SOMALIA", "Somalia")
    SOUTH_AFRICA = ("SOUTH_AFRICA", "South Africa")
    SOUTH_KOREA = ("SOUTH_KOREA", "South Korea")
    SOUTH_SUDAN = ("SOUTH_SUDAN", "South Sudan")
    SPAIN = ("SPAIN", "Spain")
    SRI_LANKA = ("SRI_LANKA", "Sri Lanka")
    STKITTS = ("STKITTS", "St Kitts and Nevis")
    STLUCIA = ("STLUCIA", "St Lucia")
    STVINCENT = ("STVINCENT", "St Vincent")
    SUDAN = ("SUDAN", "Sudan")
    SURINAME = ("SURINAME", "Suriname")
    SWEDEN = ("SWEDEN", "Sweden")
    SWITZERLAND = ("SWITZERLAND", "Switzerland")
    SYRIA = ("SYRIA", "Syria")
    TAJIKISTAN = ("TAJIKISTAN", "Tajikistan")
    TANZANIA = ("TANZANIA", "Tanzania")
    THAILAND = ("THAILAND", "Thailand")
    BAHAMAS = ("BAHAMAS", "The Bahamas")
    GAMBIA = ("GAMBIA", "The Gambia")
    TOGO = ("TOGO", "Togo")
    TONGA = ("TONGA", "Tonga")
    TRINIDAD = ("TRINIDAD", "Trinidad and Tobago")
    TUNISIA = ("TUNISIA", "Tunisia")
    TURKEY = ("TURKEY", "Turkey")
    TURKMENISTAN = ("TURKMENISTAN", "Turkmenistan")
    TUVALU = ("TUVALU", "Tuvalu")
    UGANDA = ("UGANDA", "Uganda")
    UKRAINE = ("UKRAINE", "Ukraine")
    UAE = ("UAE", "United Arab Emirates")
    UK = ("UK", "United Kingdom")
    US = ("US", "United States")
    URUGUAY = ("URUGUAY", "Uruguay")
    USSR = ("USSR", "USSR")
    UZBEKISTAN = ("UZBEKISTAN", "Uzbekistan")
    VANUATU = ("VANUATU", "Vanuatu")
    VATICAN = ("VATICAN", "Vatican City")
    VENEZUELA = ("VENEZUELA", "Venezuela")
    VIETNAM = ("VIETNAM", "Vietnam")
    YEMEN = ("YEMEN", "Yemen")
    YUGOSLAVIA = ("YUGOSLAVIA", "Yugoslavia")
    ZAMBIA = ("ZAMBIA", "Zambia")
    ZIMBABWE = ("ZIMBABWE", "Zimbabwe")


class Region(Choices):
    DEFAULT = ("DEFAULT", "----")
    AMERICAS = ("AMERICAS", "Americas")
    APAC = ("APAC", "Asia-Pacific")
    EMEA = ("EMEA", "EMEA")


class RequestForCall(Choices):
    DEFAULT = ("DEFAULT", "----")
    YES_MORNING = ("YES_MORNING", "Yes - morning")
    YES_AFTERNOON = ("YES_AFTERNOON", "Yes - afternoon")
    YES_OTHER = ("YES_OTHER", "Yes - other")
    NO = ("NO", "No")


class FirstResponseChannel(Choices):
    DEFAULT = ("DEFAULT", "----")
    CALL = ("CALL", "Call")
    EMAIL = ("EMAIL", "Email")
    NOT_RESPONDED = ("NOT_RESPONDED", "Not yet responded")


class HpoSelection(Choices):
    DEFAULT = ("DEFAULT", "----")
    FOOD_PRODUCTION = ("FOOD_PRODUCTION", "Food Production")
    UK_RAIL = ("UK_RAIL", "UK Rail")
    LIGHTWEIGHT_STRUCTURES = ("LIGHTWEIGHT_STRUCTURES", "Lightweight Structures")


class OrganisationType(Choices):
    DEFAULT = ("DEFAULT", "----")
    CHARITY = ("CHARITY,", "Charity")
    GOVERNMENT = ("GOVERNMENT", "Government department or other public body")
    LIMITED_COMPANY = ("LIMITED_COMPANY", "Limited company")
    LIMITED_PARTNERSHIP = ("LIMITED_PARTNERSHIP", "Limited partnership")
    PARTNERSHIP = ("PARTNERSHIP,", "Partnership")
    SOLE_TRADER = ("SOLE_TRADER", "Sole trader")


class InvestmentType(Choices):
    DEFAULT = ("DEFAULT", "----")
    ACQUISITION = ("ACQUISITION", "Acquisition")
    CAPITAL_ONLY = ("CAPITAL_ONLY", "Capital only")
    NEW_SITE = ("NEW_SITE", "Creation of new site or activity")
    EXPANSION = ("EXPANSION", "Expansion of existing site or activity")
    JOINT_VENTURE = ("JOINT_VENTURE", "Joint venture")
    MERGER = ("MERGER", "Merger")
    RETENTION = ("RETENTION", "Retention")
    NOT_SPECIFIED = ("NOT_SPECIFIED", "Not specified")


class NewExistingInvestor(Choices):
    DEFAULT = ("DEFAULT", "----")
    NEW = ("NEW,", "New investor")
    EXISTING = ("EXISTING,", "Existing investor")


class InvestorInvolvement(Choices):
    FDI_HUB_HQ = ("FDI_HUB_HQ", "FDI Hub + HQ")
    FDI_HUB_HQ_LEP = ("FDI_HUB_HQ_LEP", "FDI Hub + HQ + LEP")
    FDI_HUB_POST_LEP = ("FDI_HUB_POST_LEP", "FDI Hub + HQ + Post + LEP")
    FDI_HUB_POST_REG = ("FDI_HUB_POST_REG", "FDI Hub + HQ + Post + Reg")
    FDI_HUB_HQ_REG = ("FDI_HUB_HQ_REG", "FDI Hub + HQ  + Reg")
    FDI_HUB_LEP = ("FDI_HUB_LEP", "FDI Hub + LEP")
    FDI_HUB_POST = ("FDI_HUB_POST", "FDI Hub + Post")
    FDI_HUB_POST_HQ = ("FDI_HUB_POST_HQ", "FDI Hub + Post + HQ")
    FDI_HUB_POST_LEP = ("FDI_HUB_POST_LEP", "FDI Hub + Post + LEP")
    FDI_HUB_POST_REG = ("FDI_HUB_POST_REG", "FDI Hub + Post + Reg")
    FDI_HUB_REGION = ("FDI_HUB_REGION", "FDI Hub + Region")
    FDI_HUB_ONLY = ("FDI_HUB_ONLY", "FDI Hub Only")
    HQ_LEP = ("HQ_LEP", "HQ + LEP")
    HQ_POST_LEP = ("HQ_POST_LEP", "HQ + Post + LEP")
    HQ_ONLY = ("HQ_ONLY", "HQ Only")
    HQ_POST_ONLY = ("HQ_POST_ONLY", "HQ and Post Only")
    HQ_REGION = ("HQ_REGION", "HQ and Region")
    HQ_POST_REGION = ("HQ_POST_REGION,", "HQ, Post and Region")
    LEP_ONLY = ("LEP_ONLY", "LEP Only")
    NO_INVOLVEMENT = ("NO_INVOLVEMENT", "No involvement")
    POST_LEP = ("POST_LEP", "Post + LEP")
    POST_ONLY = ("POST_ONLY", "Post Only")
    POST_REGION = ("POST_REGION", "Post and Region")
    REGION_ONLY = ("REGION_ONLY", "Region Only")


class InvestmentProgramme(Choices):
    ADVANCED_ENG = ("ADVANCED_ENG", "Advanced Engineering Supply Chain")
    BUSINESS_PARTNER = ("BUSINESS_PARTNER", "Business Partnership (Non-FDI)")
    CONTRACT_RESEARCH = ("CONTRACT_RESEARCH", "Contract Research (Non-FDI)")
    FDI_CAPITAL_ONLY = ("FDI_CAPITAL_ONLY", "FDI (Capital Only)")
    GREAT_INV_PROG = ("GREAT_INV_PROG", "GREAT Investors Programme")
    GLOBAL_ENTREP_PROG = ("GLOBAL_ENTREP_PROG", "Global Entrepreneur Programme")
    GRADUATE_ENTREP_PROG = ("GRADUATE_ENTREP_PROG", "Graduate Entrepreneur Programme")
    HQ_UK = ("HQ_UK", "HQ-UK")
    II_AND_I = ("II&I", "II&I Programme")
    INFRASTRUCTURE_GATEWAY = ("INFRASTRUCTURE_GATEWAY", "Infrastructure Gateway")
    IIGB = ("IIGB", "Invest in Great Britain")
    NO_SPECIFIC_PROG = ("NO_SPECIFIC_PROG", "No Specific Programme")
    RD_COLLAB = ("R&D_COLLAB", "R&D Collaboration (Non-FDI)")
    RD_PARTNERSHIP = ("R&D_PARTNERSHIP", "R&D Partnership (Non-FDI)")
    RD_PROG = ("R&D_PROG", "R&D Prog (Obsolete)")
    REGENERATION = ("REGENERATION", "Regeneration Investment Organisation (RIO)")
    SRM = ("SRM", "SRM Programme")
    SCREEN = ("SCREEN", "Screen Production Investment")
    SIRIUS = ("SIRIUS", "Sirius (Graduate Entrepreneurs)")
    SPACE = ("SPACE", "Space")
    UNIVERSITY_COLLAB = ("UNIVERSITY_COLLAB", "University Collaboration (Non-FDI)")
    VENTURE_CAPITAL = ("VENTURE_CAPITAL", "Venture / Equity Capital")


class DatahubProjectStatus(Choices):
    DEFAULT = ("DEFAULT", "----")
    PROSPECT = ("PROSPECT", "Prospect")
    ASSIGN = ("ASSIGN", "Assign PM")
    ACTIVE = ("ACTIVE", "Active")
    VERIFY = ("VERIFY", "Verify Win")
    WON = ("WON", "Won")
    ABANDONED = ("ABANDONED", "Abandoned")
    DELAYED = ("DELAYED", "Delayed")
>>>>>>> Update ref data to fix typos and capitalisation
