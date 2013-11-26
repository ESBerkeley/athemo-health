__author__ = 'ericxiao'
from insuranceapp.models import GeographicArea, HealthcarePlan, Provider
from insuranceapp.AthemoParserXML import *

def importZipCodes():
    zip_codes = get_all_zipcodes()
    for zip_code in zip_codes:
        if type(zip_code) == int:
            try:
                zip_info = get_zip_code_info(zip_code)
                state = zip_info[0].value
                rating_area = int(zip_info[4].value.split(' ')[-1])
                county = zip_info[2].value
                area = GeographicArea(rating_area=rating_area, 
                                      county=county,
                                      state=state,
                                      zip_code=zip_code)
                area.save()
            except:
                continue

def importSutter():
    medals = ['bronze', 'silver', 'gold', 'platinum']
    sutter_provider, created = Provider.objects.get_or_create(name='Sutter Health Plan', 
                                                              url='http://www.sutterhealth.org/')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in [1, 2, 3, 10]:
            #try:
            str_premium = getSutterHealthPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.get_or_create(medal=medal.capitalize(),
                                    age=age,
                                    price=premium,
                                    provider=sutter_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)
            #except:
            #    continue

def importVentura():
    medals = ['bronze', 'silver', 'gold', 'platinum']
    sutter_provider, created = Provider.objects.get_or_create(name='Ventura Health Plan',
                                                              url='http://www.vchca.org/')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
            #try:
            str_premium = getVenturaHealthPlan(medal, age)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(state='CA')
            plan, created = HealthcarePlan.get_or_create(medal=medal.capitalize(),
                                  age=age,
                                  price=premium,
                                  provider=sutter_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)
#except:
#    continue

def importVallet():
    medals = ['bronze', 'silver', 'gold', 'platinum']
    sutter_provider, created = Provider.objects.get_or_create(name='Vallet Health Plan',
                                                              url='http://www.valleyhealthplan.org/')
    for medal in medals:
        age = 21
            #For Sutter Health Plans
            #try:
            str_premium = getValletHealthPlan(medal, age)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(state='CA')
            plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
                                  age=age,
                                  price=premium,
                                  provider=sutter_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)
#except:
#    continue




def importContra():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    sutter_provider, created = Provider.objects.get_or_create(name='Contra Health Plan', url='http://cchealth.org/healthplan/')
    for medal in medals:
        age = 21
        str_premium = getContraHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(), age=age, price=premium, provider=sutter_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)

def importSharp():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    sutter_provider, created = Provider.objects.get_or_create(name='Sharp Health Plan', url='https://www.sharphealthplan.com/')
    for medal in medals:
        age = 21
        str_premium = getSharpHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(), age=age, price=premium, provider=sutter_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)

def importNetHealth():
    medals = ['silver', 'gold', 'platinum']
    sutter_provider, created = Provider.objects.get_or_create(name='Net Health Plan', url='https://www.healthnet.com/portal/home.ndo')
    for medal in medals:
        age = 21
        str_premium = getCaNetHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(), age=age, price=premium, provider=sutter_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)


def importChinese():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    sutter_provider, created = Provider.objects.get_or_create(name='Chinese Health Plan',
                                                              url='http://www.cchphmo.com/')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in [4, 8]:
            #try:
            str_premium = getChineseHealthPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.get_or_create(medal=medal.capitalize(),
                                    age=age,
                                    price=premium,
                                    provider=sutter_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)
            #except:
            #    continue

def importMolina():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    sutter_provider, created = Provider.objects.get_or_create(name='Molina Health Plan', url='www.molinahealthcare.com/‎')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in [15,16,17,19]:
            #try:
            str_premium = getMolinaHealthPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.get_or_create(medal=medal.capitalize(),
                                    age=age,
                                    price=premium,
                                    provider=sutter_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)

def importBlue():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    sutter_provider, created = Provider.objects.get_or_create(name='Blue Health Plan', url='http://www.bcbs.com/')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in range(1,19):
            #try:
            str_premium = getBlueHealthPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.get_or_create(medal=medal.capitalize(),
                                    age=age,
                                    price=premium,
                                    provider=sutter_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)


def all_states():
    ALL_STATES = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
    }
    return ALL_STATES