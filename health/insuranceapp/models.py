from django.db import models
#from utils import all_states

class HealthcarePlan(models.Model):
    BRONZE = 'Bronze'
    SILVER = 'Silver'
    GOLD = 'Gold'
    PLATINUM = 'Platinum'
    CATASTROPHIC = 'Catastrophic'

    TYPE_CHOICES = (
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
        (PLATINUM, 'Platinum'),
        (CATASTROPHIC, 'Catastrophic')
    )
    medal = models.CharField(choices=TYPE_CHOICES,
                            default=BRONZE,
                            max_length=20)
    provider = models.ForeignKey('Provider')
    areas = models.ManyToManyField('GeographicArea')
    age = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

class Provider(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

class GeographicArea(models.Model):
    rating_area = models.IntegerField()
    zip_code = models.IntegerField(max_length=5, unique=True)
    state = models.CharField(max_length=2) #choices=all_states().keys())
    county = models.CharField(max_length=50)
    def __unicode__(self):
        return self.zip_code