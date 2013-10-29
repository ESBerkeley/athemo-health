from django.db import models

# Create your models here.

class HealthcarePlan(models.Model):
    '''
    BRONZE = 'BR'
    SILVER = 'SI'
    GOLD = 'GO'
    CATASTROPHIC = 'CA'

    TYPE_CHOICES = (
        (BRONZE, 'BR'),
        (SILVER, 'SI'),
        (GOLD, 'GO'),
        (CATASTROPHIC, 'CA')
    )'''
    type = models.ForeignKey('InsuranceType')
    area = models.ForeignKey('GeographicArea')
    price = models.DecimalField(max_digits=8, decimal_places=2)


class InsuranceType(models.Model):
    BRONZE = 'Bronze'
    SILVER = 'Silver'
    GOLD = 'Gold'
    CATASTROPHIC = 'Catastrophic'

    TYPE_CHOICES = (
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
        (CATASTROPHIC, 'Catastrophic')
    )
    name = models.CharField(choices=TYPE_CHOICES,
                            default=BRONZE)
    description = models.BodyField()

class GeographicArea(models.Model):
    rating_area = models.IntegerField()
    zipcode = models.IntegerField(min_length=5, max_length=5)

    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
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
        'MP': 'Northern Mariana Islands',
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
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
