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

        area = GeographicArea.objects.select_related().get(zip_code=zip_code)
        plans = area.plan_set.filter(age=21)

        # GENERIC = 44.14, 78% of drugs
        # BRAND_NAME = 166.01, 22% of drugs
        avg_prescription_cost = 44.14*.78 + 166.01*.22

        # 58% of visits to primary care, $150 median
        # 35% to specialty care
        # $130 urgent care, $500 emergency care
        avg_doctor_cost = .58*150 + .35*270 + .05*130 + .02*500

        total_prescription_cost = prescription_use*avg_prescription_cost
        total_doctor_cost = doctor_use*avg_doctor_cost
        #Your premium + your deductible + any coinsurance
        # you must pay (up to your out-of-pocket maximum) +
        # any copayments = the most you will pay for healthcare each year (for covered services).

        for plan in plans:
            total_monthly_premium = 0
            for age in ages:
                age = max(20,age)
                age = min(64,age)
                total_monthly_premium += float(plan.price)*AGE_RATIOS[age]
            plan_details = MEDAL_DETAILS[plan.medal]
            if len(ages) > 1:
                deductible = plan_details['family_deductible']
                max_out_of_pocket = plan_details['max_out_of_pocket_family']
            else:
                deductible = plan_details['individual_deductible']
                max_out_of_pocket = plan_details['max_out_of_pocket']

            if plan.medal == 'Bronze':
                # USED FOR CALCULATIONS OF COPAY FOR BRONZE
                remaining_deductible = deductible
                remaining_prescriptions = prescription_use
                remaining_doctor_visits = doctor_use
                is_doctor_cost = True

                while remaining_deductible > 0 and \
                    (remaining_prescriptions > 0 or remaining_doctor_visits > 0):

                    if is_doctor_cost and remaining_doctor_visits > 0:
                        remaining_deductible -= avg_doctor_cost
                        remaining_doctor_visits -= 1
                    elif remaining_prescriptions > 0:
                        remaining_deductible -= avg_prescription_cost
                        remaining_prescriptions -= 1

                    is_doctor_cost = not is_doctor_cost
                out_of_pocket_doctor_costs = remaining_doctor_visits*plan_details['avg_doctor_copay'] + \
                                          (doctor_use - remaining_doctor_visits)*avg_doctor_cost
                out_of_pocket_prescription_costs = remaining_prescriptions*plan_details['avg_prescription_copay'] + \
                                               (prescription_use - remaining_prescriptions)*avg_prescription_cost
                if is_doctor_cost and remaining_deductible < 0: #LAST THING PAID FOR IS PRESCRIPTION
                    out_of_pocket_prescription_costs += abs(remaining_deductible)
                elif not is_doctor_cost and remaining_deductible < 0: #LAST THING PAID FOR IS DOCTOR_VISIT
                    out_of_pocket_doctor_costs += abs(remaining_deductible)
            else:
                out_of_pocket_doctor_costs = doctor_use * plan_details['avg_doctor_copay']
                out_of_pocket_prescription_costs = prescription_use * plan_details['avg_prescription_copay']

            total_uninsured_cost = total_prescription_cost + total_doctor_cost
            out_of_pocket_cost = total_monthly_premium * 12 + out_of_pocket_doctor_costs + out_of_pocket_prescription_costs
            savings = total_uninsured_cost - out_of_pocket_cost
            insurance_prescription_payment = total_prescription_cost - out_of_pocket_prescription_costs
            insurance_doctor_payment = total_doctor_cost - out_of_pocket_doctor_costs
            insurance_payment = insurance_prescription_payment + insurance_doctor_payment

            plan.total_out_of_pocket_cost = [{'name':'annual_premium', 'value': total_monthly_premium*12},
                                            {'name':'prescription_cost', 'value': out_of_pocket_prescription_costs},
                                            {'name':'doctor_cost', 'value': out_of_pocket_doctor_costs}]
            plan.savings = savings
            plan.total_insurance_payment = [{'name':'prescription_cost', 'value': insurance_prescription_payment},
                                            {'name':'doctor_cost', 'value': insurance_doctor_payment}]
        data = serializers.serialize('json',
                                     plans,
                                     extras=('total_out_of_pocket_cost', 'total_insurance_payment', 'savings'))
        return HttpResponse(data, 'application/javascript')


def plans(request):
    return render_to_response('plan-cols.html', context_instance=RequestContext(request))

# tuple = (DOLLAR AMOUNT, NEEDS TO REACH DEDUCTIBLE)
BRONZE = {'primary_care_copay': 60,
          'specialty_care_copay': 70,
          'urgent_care_copay': 120,
          'emergency_room_copay': 300,
          'avg_doctor_copay': .58*60 + .35*70 + .05*120 + .02*300,
          'individual_deductible': 5000,
          'family_deductible':10000,
          'generic_copay': 19,
          'preferred_brand_copay': 50,
          'avg_prescription_copay': .78*19 + .22*50,
          'max_out_of_pocket': 6350,
          'max_out_of_pocket_family': 12700}
SILVER = {'primary_care_copay': 45,
          'specialty_care_copay': 65,
          'urgent_care_copay': 90,
          'emergency_room_copay': 250,
          'avg_doctor_copay': .58*45 + .35*65 + .05*90 + .02*250,
          'individual_deductible': 2100,
          'family_deductible': 4200,
          'generic_copay': 19,
          'preferred_brand_copay': 50,
          'avg_prescription_copay': .78*19 + .22*50,
          'max_out_of_pocket': 6350,
          'max_out_of_pocket_family': 12700}
GOLD = {'primary_care_copay': 30,
          'specialty_care_copay': 50,
          'urgent_care_copay': 60,
          'emergency_room_copay': 250,
          'avg_doctor_copay': .58*30 + .35*50 + .05*60 + .02*250,
          'individual_deductible': 0,
          'family_deductible': 0,
          'generic_copay': 19,
          'preferred_brand_copay': 50,
          'avg_prescription_copay': .78*19 + .22*50,
          'max_out_of_pocket': 6350,
          'max_out_of_pocket_family': 12700}
PLATINUM = {'primary_care_copay': 20,
          'specialty_care_copay': 40,
          'urgent_care_copay': 40,
          'emergency_room_copay': 150,
          'avg_doctor_copay': .58*20 + .35*40 + .05*40 + .02*150,
          'individual_deductible': 2100,
          'family_deductible': 4200,
          'generic_copay': 5,
          'preferred_brand_copay': 15,
          'avg_prescription_copay': .78*19 + .22*50,
          'max_out_of_pocket': 4000,
          'max_out_of_pocket_family': 8000}
MEDAL_DETAILS = {'Bronze': BRONZE, 'Silver': SILVER, 'Gold': GOLD, 'Platinum': PLATINUM}

AGE_RATIOS = {20: 0.635, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1.004, 26: 1.024, 27: 1.048, 28: 1.087, 29: 1.119, 30: 1.135, 31: 1.159, 32: 1.183, 33: 1.198, 34: 1.214, 35: 1.222, 36: 1.23, 37: 1.238, 38: 1.246, 39: 1.262, 40: 1.278, 41: 1.302, 42: 1.325, 43: 1.357, 44: 1.397, 45: 1.444, 46: 1.5, 47: 1.563, 48: 1.635, 49: 1.706, 50: 1.786, 51: 1.865, 52: 1.952, 53: 2.04, 54: 2.135, 55: 2.23, 56: 2.333, 57: 2.437, 58: 2.548, 59: 2.603, 60: 2.714, 61: 2.81, 62: 2.873, 63: 2.952, 64: 3}