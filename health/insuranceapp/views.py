# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from models import HealthcarePlan, GeographicArea

def home(request):
    #title = request.GET['title']
    #msg = request.GET['msg']
    return render_to_response('home/home.html', context_instance=RequestContext(request))

def household_info(request):
    return render_to_response('household_info.html',context_instance=RequestContext(request))


def ajax_get_plans(request):
    #if request.is_ajax() and request.method == 'GET':
    if request.method == 'GET':
        zip_code = 95388
        income = 30000
        doctor_use = 1
        prescription_use = 5
        #zip_code=5&income=&age=&medical_visits=&prescription_use=&medal=all
        if 'zip_code' in request.GET:
            zip_code = int(request.GET['zip_code'])
        if 'income' in request.GET:
            income = float(request.GET['income'])
        if 'medical_visits' in request.GET:
            doctor_use = float(request.GET['medical_visits'])
        if 'prescription_use' in request.GET:
            prescription_use = float(request.GET['prescription_use'])
        ages = request.GET.getlist('age')
        ages = map(int, ages)
        if not ages:
            ages = [21]

        area = GeographicArea.objects.get(zip_code=zip_code).select_related('HealthcarePlan')
        plans = area.plan_set.filter(age=21)

        # GENERIC = 44.14, 78% of drugs
        # BRAND_NAME = 166.01, 22% of drugs
        avg_prescription_cost = 44.14*.78 + 166.01*.22

        # 58% of visits to primary care, $150 median
        # 35% to specialty care
        # $130 urgent care, $500 emergency care
        avg_doctor_cost = .58*150 + .35*270 + .05*130 + .02*500

        for plan in plans:
            total_monthly_premium = 0
            for age in ages:
                age = max(20,age)
                age = min(64,age)
                total_monthly_premium += plan.price*AGE_RATIOS[age]
            total_prescription_cost = prescription_use*avg_prescription_cost
            total_doctor_cost = doctor_use*avg_doctor_cost

            plan.prescription_cost = [{'name':'prescription_cost',
                                       'value':total_prescription_cost}]
            plan.doctor_cost = [{'name':'doctor_cost',
                                 'value':total_doctor_cost}]
            plan.total_monthly_premium = [{'name':'total_monthly_premium',
                                            'value':total_monthly_premium}]
            total_costs = total_doctor_cost + total_prescription_cost + total_monthly_premium
            #primary_care_copay = primary_care_copay_by_medal(plan.medal)


        data = serializers.serialize('json',
                                     [plan for plan in plans],
                                     extras=('prescription_cost', 'doctor_cost'))
        return HttpResponse(data, 'application/javascript')


def plans(request):
    return render_to_response('plan-cols.html', context_instance=RequestContext(request))

BRONZE = {'primary_care_copay': 60,
          'specialty_care_copay': 70,
          'urgent_care_copay': 120,
          'emergency_room_copay':300,
          'individual_deductible':5000,
          'family_deductible':10000,
          'generic_copay':19,
          'preferred_brand_copay':50,
          'avg_prescription_copay': .78*19 + .22*50}
SILVER = {'primary_care_copay': 45,
          'specialty_care_copay': 65,
          'urgent_care_copay': 90,
          'emergency_room_copay':250,
          'individual_deductible':2100,
          'family_deductible':4200,
          'generic_copay':19,
          'preferred_brand_copay':50,
          'avg_prescription_copay': .78*19 + .22*50}
GOLD = {'primary_care_copay': 60,
          'specialty_care_copay': 70,
          'urgent_care_copay': 120,
          'emergency_room_copay':300,
          'individual_deductible':5000,
          'family_deductible':10000,
          'generic_copay':19,
          'preferred_brand_copay':50,
          'avg_prescription_copay': .78*19 + .22*50}
PLATINUM = {'primary_care_copay': 60,
          'specialty_care_copay': 70,
          'urgent_care_copay': 120,
          'emergency_room_copay':300,
          'individual_deductible':5000,
          'family_deductible':10000,
          'generic_copay':19,
          'preferred_brand_copay':50,
          'avg_prescription_copay': .78*19 + .22*50}
AGE_RATIOS = {20: 0.635, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1.004, 26: 1.024, 27: 1.048, 28: 1.087, 29: 1.119, 30: 1.135, 31: 1.159, 32: 1.183, 33: 1.198, 34: 1.214, 35: 1.222, 36: 1.23, 37: 1.238, 38: 1.246, 39: 1.262, 40: 1.278, 41: 1.302, 42: 1.325, 43: 1.357, 44: 1.397, 45: 1.444, 46: 1.5, 47: 1.563, 48: 1.635, 49: 1.706, 50: 1.786, 51: 1.865, 52: 1.952, 53: 2.04, 54: 2.135, 55: 2.23, 56: 2.333, 57: 2.437, 58: 2.548, 59: 2.603, 60: 2.714, 61: 2.81, 62: 2.873, 63: 2.952, 64: 3}