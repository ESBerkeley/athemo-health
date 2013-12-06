__author__ = 'ericxiao'
########### IMPORT PLANS CODE ###################
from AthemoParserXML import *
from models import GeographicArea, Provider, HealthcarePlan

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

def importAll():
    importKaiser()
#     importBlue()
#     importChinese()
#     importContra()
#     importMolina()
#     importHealthNet()
#     importSharp()
#     importSutter()
#     importValley()

def importKaiser():
    medals = ['catastrophic','bronze', 'silver', 'gold', 'platinum']
    kaiser_provider, created = Provider.objects.get_or_create(name='Kaiser Permanente',
                                                              url='https://smu.kaiserpermanente.org/expressweb/user/DSTHandOffAction.action#4')
    
    for medal in medals:
        for r_area in range(1,20):
            str_premium = getKaiserHealthPlan(medal, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(state='CA')
            plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
                                                            age=21,
                                                            price=premium,
                                                            provider=kaiser_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)

def importSutter():
    medals = ['bronze', 'silver', 'gold', 'platinum']
    sutter_provider, created = Provider.objects.get_or_create(name='Sutter Health',
                                                              url='http://www.sutterhealth.org/')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in [1, 2, 3, 10]:
            #try:
            str_premium = getSutterHealthPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
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
    ventura_provider, created = Provider.objects.get_or_create(name='Ventura County Health Care',
                                                              url='http://www.vchealthcareplan.org/')
    for medal in medals:
        age = 21
        str_premium = getVenturaHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
                                age=age,
                                price=premium,
                                provider=ventura_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)

def importValley():
    medals = ['bronze', 'silver', 'gold', 'platinum']
    valley_provider, created = Provider.objects.get_or_create(name='Valley Health',
                                                              url='http://www.valleyhealthplan.org/sites/shoppers/Pages/individual.aspx')
    for medal in medals:
        age = 21
        str_premium = getValleyHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
                                age=age,
                                price=premium,
                                provider=valley_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)

def importContra():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    contra_provider, created = Provider.objects.get_or_create(name='Contra Costa Health',
                                                              url='http://cchealth.org/insurance/')
    for medal in medals:
        age = 21
        str_premium = getContraHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(), age=age, price=premium, provider=contra_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)

def importSharp():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    sharp_provider, created = Provider.objects.get_or_create(name='Sharp Health Plan',
                                                             url='https://www.sharphealthplan.com/index.php/shop-for-plans/individual-and-family-plans')
    for medal in medals:
        age = 21
        str_premium = getSharpHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(), age=age, price=premium, provider=sharp_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)

def importHealthNet():
    medals = ['silver', 'gold', 'platinum']
    health_net_provider, created = Provider.objects.get_or_create(name='Health Net',
                                                                  url='https://www.healthnet.com/portal/shopping/content/iwc/shopping/marketplace/ifp/introduction.action')
    for medal in medals:
        age = 21
        str_premium = getCaNetHealthPlan(medal, age)
        premium = float(str_premium)
        areas = GeographicArea.objects.filter(state='CA')
        plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(), age=age, price=premium, provider=health_net_provider)
        plan.save()
        for area in areas:
            plan.areas.add(area)


def importChinese():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    chinese_provider, created = Provider.objects.get_or_create(name='Chinese Community Health',
                                                              url='http://www.cchphmo.com/coverage-individual-family-plans')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in [4, 8]:
            #try:
            str_premium = getChineseHealthPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
                                    age=age,
                                    price=premium,
                                    provider=chinese_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)
            #except:
            #    continue

def importMolina():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    molina_provider, created = Provider.objects.get_or_create(name='Molina Healthcare',
                                                              url='http://www.molinahealthcare.com/members/ca/en-US/hp/marketplace/plans/Pages/allplans.aspx')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in [15,16,17,19]:
            #try:
            str_premium = getMolinaHealthPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
                                    age=age,
                                    price=premium,
                                    provider=molina_provider)
            plan.save()
            for area in areas:
                plan.areas.add(area)

def importBlue():
    medals = ['bronze', 'silver', 'gold', 'platinum', 'catastrophic']
    blue_provider, created = Provider.objects.get_or_create(name='Blue Shield',
                                                            url='https://bscapply.com/phx/action/homePageAction?marketcode=CaratOENovDec2013')
    for medal in medals:
        age = 21
        #For Sutter Health Plans
        for r_area in range(1,19):
            #try:
            str_premium = getBlueShieldPlan(medal, age, r_area)
            premium = float(str_premium)
            areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
            plan, created = HealthcarePlan.objects.get_or_create(medal=medal.capitalize(),
                                    age=age,
                                    price=premium,
                                    provider=blue_provider)
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