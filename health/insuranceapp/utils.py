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

def importPlans():
    medals = ['bronze', 'silver', 'gold', 'platinum']
    sutter_provider, created = Provider.objects.get_or_create(name='Sutter Health Plan', 
                                                              url='http://www.sutterhealth.org/')
    for medal in medals:
        for age in range(20, 65):
            #For Sutter Health Plans
            for r_area in [1, 2, 3, 10]:
                #try:
                str_premium = getSutterHealthPlan(medal, age, r_area)
                premium = float(str_premium)
                areas = GeographicArea.objects.filter(rating_area=r_area, state='CA')
                plan = HealthcarePlan(medal=medal.capitalize(),
                                      age=age,
                                      price=premium,
                                      provider=sutter_provider)
                plan.save()
                for area in areas:
                    plan.areas.add(area)
                #except:
                #    continue


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