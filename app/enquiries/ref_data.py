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
    NON_APPLICABLE = "NON_APPLICABLE", _("Non-applicable")
    NURTURE_AWAITING_RESPONSE = "NURTURE_AWAITING_RESPONSE", _(
        "Nurture awaiting response"
    )


class InvestmentReadiness(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    CONVINCED = (
        "CONVINCED",
        _("I’m convinced and want to talk to someone about my plans"),
    )
    SHORTLIST = (
        "SHORTLIST",
        _(
            "The UK is on my shortlist. How can the Department for Business and Trade help me?"
        ),
    )
    EXPLORING = (
        "EXPLORING",
        _(
            "I’m still exploring where to expand my business and would like to know more about the\
 UK’s offer"
        ),
    )
    NOT_READY = "NOT_READY", _("I’m not yet ready to invest. Keep me informed")
    NOT_INTERESTED_IN_UK = "NOT_INTERESTED_IN_UK", _(
        "I’m not interested in setting up in the UK"
    )


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
    IIGB = "IIGB", _("Website")
    IIGB_LINKEDIN = "IIGB_LINKEDIN", _("Website (LinkedIn)")
    HPO = "HPO", _("HPO")
    EBOOK = "EBOOK", _("EBOOK")
    TRA = "TRA", _("TRA")
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
    ADVANCED_ENG = "ADVANCED_ENG", _("Advanced engineering")
    AEROSPACE = "AEROSPACE", _("Aerospace")
    AGRICULTURE = "AGRICULTURE", _("Agriculture, horticulture, fisheries and pets")
    AIRPORTS = "AIRPORTS", _("Airports")
    AUTOMOTIVE = "AUTOMOTIVE", _("Automotive")
    CHEMICALS = "CHEMICALS", _("Chemicals")
    CONSTRUCTION = "CONSTRUCTION", _("Construction")
    CONSUMER = "CONSUMER", _("Consumer and retail")
    CREATIVE = "CREATIVE", _("Creative industries")
    DEFENCE = "DEFENCE", _("Defence")
    EDUCATION = "EDUCATION", _("Education and training")
    ENERGY = "ENERGY", _("Energy")
    ENVIRONMENT = "ENVIRONMENT", _("Environment")
    FINANCIAL = "FINANCIAL", _("Financial and professional services")
    FOOD = "FOOD", _("Food and drink")
    HEALTHCARE = "HEALTHCARE", _("Healthcare services")
    MARITIME = "MARITIME", _("Maritime")
    MEDICAL = "MEDICAL", _("Medical devices and equipment")
    MINING = "MINING", _("Mining")
    PHARMACEUTICALS = "PHARMACEUTICALS", _("Pharmaceuticals and biotechnology")
    RAILWAYS = "RAILWAYS", _("Railways")
    SECURITY = "SECURITY", _("Security")
    SPACE = "SPACE", _("Space")
    SPORTS = "SPORTS", _("Sports economy")
    TECHNOLOGY = "TECHNOLOGY", _("Technology and smart cities")
    WATER = "WATER", _("Water")


class ISTSector(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    ITECH = "ITECH", _("ITECH")
    LIFE = "LIFE", _("Life Science")
    ENERGY = "ENERGY", _("Energy and Environment")
    BPFS = "BPFS", _("BPFS")
    AEM = "AEM", _("AEM")
    UNCLASSIFIED = "UNCLASSIFIED", _("Unclassified")


class Country(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    AF = "AF", _("Afghanistan")
    AL = "AL", _("Albania")
    DZ = "DZ", _("Algeria")
    AD = "AD", _("Andorra")
    AO = "AO", _("Angola")
    AI = "AI", _("Anguilla")
    AG = "AG", _("Antigua and Barbuda")
    AR = "AR", _("Argentina")
    AM = "AM", _("Armenia")
    AU = "AU", _("Australia")
    AT = "AT", _("Austria")
    AZ = "AZ", _("Azerbaijan")
    BH = "BH", _("Bahrain")
    BD = "BD", _("Bangladesh")
    BB = "BB", _("Barbados")
    BY = "BY", _("Belarus")
    BE = "BE", _("Belgium")
    BZ = "BZ", _("Belize")
    BJ = "BJ", _("Benin")
    BM = "BM", _("Bermuda")
    BT = "BT", _("Bhutan")
    BO = "BO", _("Bolivia")
    BA = "BA", _("Bosnia and Herzegovina")
    BW = "BW", _("Botswana")
    BR = "BR", _("Brazil")
    VG = "VG", _("British Virgin Islands")
    BN = "BN", _("Brunei")
    BG = "BG", _("Bulgaria")
    BF = "BF", _("Burkina Faso")
    BI = "BI", _("Burundi")
    KH = "KH", _("Cambodia")
    CM = "CM", _("Cameroon")
    CA = "CA", _("Canada")
    CV = "CV", _("Cape Verde")
    KY = "KY", _("Cayman Islands")
    CF = "CF", _("Central African Republic")
    TD = "TD", _("Chad")
    CL = "CL", _("Chile")
    CN = "CN", _("China")
    CO = "CO", _("Colombia")
    KM = "KM", _("Comoros")
    CG = "CG", _("Congo")
    CD = "CD", _("Congo (Democratic Republic)")
    CR = "CR", _("Costa Rica")
    HR = "HR", _("Croatia")
    CU = "CU", _("Cuba")
    CY = "CY", _("Cyprus")
    CZ = "CZ", _("Czechia")
    DK = "DK", _("Denmark")
    DJ = "DJ", _("Djibouti")
    DM = "DM", _("Dominica")
    DO = "DO", _("Dominican Republic")
    TL = "TL", _("East Timor")
    EC = "EC", _("Ecuador")
    EG = "EG", _("Egypt")
    SV = "SV", _("El Salvador")
    GQ = "GQ", _("Equatorial Guinea")
    ER = "ER", _("Eritrea")
    EE = "EE", _("Estonia")
    SZ = "SZ", _("Eswatini")
    ET = "ET", _("Ethiopia")
    FK = "FK", _("Falkland Islands")
    FO = "FO", _("Faroe Islands")
    FJ = "FJ", _("Fiji")
    FI = "FI", _("Finland")
    FR = "FR", _("France")
    GA = "GA", _("Gabon")
    GE = "GE", _("Georgia")
    DE = "DE", _("Germany")
    GH = "GH", _("Ghana")
    GI = "GI", _("Gibraltar")
    GR = "GR", _("Greece")
    GL = "GL", _("Greenland")
    GD = "GD", _("Grenada")
    GT = "GT", _("Guatemala")
    GG = "GG", _("Guernsey")
    GN = "GN", _("Guinea")
    GW = "GW", _("Guinea-Bissau")
    GY = "GY", _("Guyana")
    HT = "HT", _("Haiti")
    HN = "HN", _("Honduras")
    HK = "HK", _("Hong Kong")
    HU = "HU", _("Hungary")
    IS = "IS", _("Iceland")
    IN = "IN", _("India")
    ID = "ID", _("Indonesia")
    IR = "IR", _("Iran")
    IQ = "IQ", _("Iraq")
    IE = "IE", _("Ireland")
    IM = "IM", _("Isle of Man")
    IL = "IL", _("Israel")
    IT = "IT", _("Italy")
    CI = "CI", _("Ivory Coast")
    JM = "JM", _("Jamaica")
    JP = "JP", _("Japan")
    JE = "JE", _("Jersey")
    JO = "JO", _("Jordan")
    KZ = "KZ", _("Kazakhstan")
    KE = "KE", _("Kenya")
    KI = "KI", _("Kiribati")
    XK = "XK", _("Kosovo")
    KW = "KW", _("Kuwait")
    KG = "KG", _("Kyrgyzstan")
    LA = "LA", _("Laos")
    LV = "LV", _("Latvia")
    LB = "LB", _("Lebanon")
    LS = "LS", _("Lesotho")
    LR = "LR", _("Liberia")
    LY = "LY", _("Libya")
    LI = "LI", _("Liechtenstein")
    LT = "LT", _("Lithuania")
    LU = "LU", _("Luxembourg")
    MO = "MO", _("Macao")
    MG = "MG", _("Madagascar")
    MW = "MW", _("Malawi")
    MY = "MY", _("Malaysia")
    MV = "MV", _("Maldives")
    ML = "ML", _("Mali")
    MT = "MT", _("Malta")
    MH = "MH", _("Marshall Islands")
    MR = "MR", _("Mauritania")
    MU = "MU", _("Mauritius")
    MX = "MX", _("Mexico")
    FM = "FM", _("Micronesia")
    MD = "MD", _("Moldova")
    MC = "MC", _("Monaco")
    MN = "MN", _("Mongolia")
    ME = "ME", _("Montenegro")
    MS = "MS", _("Montserrat")
    MA = "MA", _("Morocco")
    MZ = "MZ", _("Mozambique")
    MM = "MM", _("Myanmar (Burma)")
    NA = "NA", _("Namibia")
    NR = "NR", _("Nauru")
    NP = "NP", _("Nepal")
    NL = "NL", _("Netherlands")
    NZ = "NZ", _("New Zealand")
    NI = "NI", _("Nicaragua")
    NE = "NE", _("Niger")
    NG = "NG", _("Nigeria")
    KP = "KP", _("North Korea")
    MK = "MK", _("North Macedonia")
    NO = "NO", _("Norway")
    PS = "PS", _("Occupied Palestinian Territories")
    OM = "OM", _("Oman")
    PK = "PK", _("Pakistan")
    PW = "PW", _("Palau")
    PA = "PA", _("Panama")
    PG = "PG", _("Papua New Guinea")
    PY = "PY", _("Paraguay")
    PE = "PE", _("Peru")
    PH = "PH", _("Philippines")
    PL = "PL", _("Poland")
    PT = "PT", _("Portugal")
    PR = "PR", _("Puerto Rico")
    QA = "QA", _("Qatar")
    RO = "RO", _("Romania")
    RU = "RU", _("Russia")
    RW = "RW", _("Rwanda")
    WS = "WS", _("Samoa")
    SM = "SM", _("San Marino")
    ST = "ST", _("Sao Tome and Principe")
    SA = "SA", _("Saudi Arabia")
    SN = "SN", _("Senegal")
    RS = "RS", _("Serbia")
    SC = "SC", _("Seychelles")
    SL = "SL", _("Sierra Leone")
    SG = "SG", _("Singapore")
    SK = "SK", _("Slovakia")
    SI = "SI", _("Slovenia")
    SB = "SB", _("Solomon Islands")
    SO = "SO", _("Somalia")
    ZA = "ZA", _("South Africa")
    KR = "KR", _("South Korea")
    SS = "SS", _("South Sudan")
    ES = "ES", _("Spain")
    LK = "LK", _("Sri Lanka")
    KN = "KN", _("St Kitts and Nevis")
    LC = "LC", _("St Lucia")
    MF = "MF", _("St Martin")
    VC = "VC", _("St Vincent")
    SD = "SD", _("Sudan")
    SR = "SR", _("Suriname")
    SE = "SE", _("Sweden")
    CH = "CH", _("Switzerland")
    SY = "SY", _("Syria")
    TW = "TW", _("Taiwan")
    TJ = "TJ", _("Tajikistan")
    TZ = "TZ", _("Tanzania")
    TH = "TH", _("Thailand")
    BS = "BS", _("The Bahamas")
    GM = "GM", _("The Gambia")
    TG = "TG", _("Togo")
    TO = "TO", _("Tonga")
    TT = "TT", _("Trinidad and Tobago")
    TN = "TN", _("Tunisia")
    TR = "TR", _("Turkey")
    TM = "TM", _("Turkmenistan")
    TC = "TC", _("Turks and Caicos Islands")
    TV = "TV", _("Tuvalu")
    UG = "UG", _("Uganda")
    UA = "UA", _("Ukraine")
    AE = "AE", _("United Arab Emirates")
    GB = "GB", _("United Kingdom")
    US = "US", _("United States")
    VI = "VI", _("United States Virgin Islands")
    UY = "UY", _("Uruguay")
    UZ = "UZ", _("Uzbekistan")
    VU = "VU", _("Vanuatu")
    VA = "VA", _("Vatican City")
    VE = "VE", _("Venezuela")
    VN = "VN", _("Vietnam")
    YE = "YE", _("Yemen")
    ZM = "ZM", _("Zambia")
    ZW = "ZW", _("Zimbabwe")


class Region(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    AMERICAS = "AMERICAS", _("Americas")
    APAC = "APAC", _("Asia-Pacific")
    EMEA = "EMEA", _("EMEA")
    UK = "UK", _("UK")


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


class NewExistingInvestor(models.TextChoices):
    DEFAULT = "DEFAULT", _("----")
    NEW = "NEW", _("New Investor")
    EXISTING = "EXISTING", _("Existing Investor")


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
    NO_INVOLVEMENT = "NO_INVOLVEMENT", _("No Involvement")
    POST_LEP = "POST_LEP", _("Post + LEP")
    POST_ONLY = "POST_ONLY", _("Post Only")
    POST_REGION = "POST_REGION", _("Post and Region")
    REGION_ONLY = "REGION_ONLY", _("Region Only")


class InvestmentProgramme(models.TextChoices):
    ADVANCED_ENG = "ADVANCED_ENG", _("Advanced Engineering Supply Chain")
    BUSINESS_PARTNER = "BUSINESS_PARTNER", _("Business Partnership (Non-FDI)")
    CONTRACT_RESEARCH = "CONTRACT_RESEARCH", _("Contract Research (Non-FDI)")
    EMERGING_MARKETS_GULF = "EMERGING_MARKETS_GULF", _(
        "Emerging Markets Contract (Gulf)"
    )
    EMERGING_MARKETS_RUSSIA = "EMERGING_MARKETS_RUSSIA", _(
        "Emerging Markets Contract (Russia)"
    )
    FDI_CAPITAL_ONLY = "FDI_CAPITAL_ONLY", _("FDI (Capital Only)")
    GLOBAL_ENTREP_PROG = "GLOBAL_ENTREP_PROG", _("Global Entrepreneur Programme")
    GRADUATE_ENTREP_PROG = "GRADUATE_ENTREP_PROG", _("Graduate Entrepreneur Programme")
    GREAT_INV_PROG = "GREAT_INV_PROG", _("GREAT Investors Programme")
    HQ_UK = "HQ_UK", _("HQ-UK")
    II_AND_I = "II&I", _("II&I Programme")
    INFRASTRUCTURE_INVESTMENT = "INFRASTRUCTURE_INVESTMENT", _(
        "Infrastructure Investment"
    )
    INNOVATION_GATEWAY = "INNOVATION_GATEWAY", _("Innovation Gateway")
    IIGB = "IIGB", _("Invest in GREAT Britain")
    NO_SPECIFIC_PROG = "NO_SPECIFIC_PROG", _("No Specific Programme")
    RD_COLLAB = "R&D_COLLAB", _("R&D Collaboration (Non-FDI)")
    RD_PARTNERSHIP = "R&D_PARTNERSHIP", _("R&D Partnership (Non-FDI)")
    RD_PROG = "R&D_PROG", _("R&D Prog (Obsolete)")
    REGENERATION = "REGENERATION", _("Regeneration Investment Organisation (RIO)")
    SCREEN = "SCREEN", _("Screen Production Investment")
    SIRIUS = "SIRIUS", _("Sirius (Graduate Entrepreneurs)")
    SPACE = "SPACE", _("Space")
    SRM = "SRM", _("SRM Programme")
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


# Data Hub metadata
DATA_HUB_BUSINESS_ACTIVITIES_SERVICES = "2f51ea6a-ca2f-466a-87fd-5f79ebfec125"
DATA_HUB_INVESTMENT_TYPE_FDI = "FDI"
DATA_HUB_PROJECT_STAGE_PROSPECT = "Prospect"
DATA_HUB_REFERRAL_SOURCE_ACTIVITY_WEBSITE = "Website"
DATA_HUB_REFERRAL_SOURCE_WEBSITE = "Invest in GREAT Britain"


IMPORT_COL_NAMES = [
    "enquirer_first_name",
    "enquirer_last_name",
    "enquirer_job_title",
    "enquirer_email",
    "enquirer_phone_country_code",
    "enquirer_phone",
    "enquirer_request_for_call",
    "country",
    "company_name",
    "ist_sector",
    "company_hq_address",
    "website",
    "investment_readiness",
    "enquiry_stage",
    "enquiry_text",
    "notes",
    "google_campaign",
    "marketing_channel",
    "date_received",
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
    "ist_sector": ISTSector,
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
