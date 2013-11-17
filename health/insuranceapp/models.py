from django.db import models
from health.insuranceapp.utils import ALL_STATES

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
    individual_deductable = models.IntegerField()
    primary_copay = models.IntegerField()
    preventative_copay = models.IntegerField()
    max_out_of_pocket = models.IntegerField()

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
    state = models.CharField(choices=ALL_STATES.keys())


