# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from models import GeographicArea
from utils import get_plans_data, doctor_use_by_age, prescription_use_by_age, get_subsidy

def home(request):
    #title = request.GET['title']
    #msg = request.GET['msg']
    return render_to_response('home/home.html', context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))

def team(request):
    return render_to_response('team.html', context_instance=RequestContext(request))

def household_info(request):
    return render_to_response('household_info.html', context_instance=RequestContext(request))


def ajax_get_plans(request):
    #if request.is_ajax() and request.method == 'GET':
    if request.method == 'GET':
        zip_code = 0
        income = 30000
        #zip_code=5&income=&age=&medical_visits=&prescription_use=&medal=all
        doctor_use = 0
        prescription_use = 0
        medal = 'all'

        ages = request.GET.getlist('age')
        ages = [age for age in ages if age]
        if ages:
            ages = map(int, ages)
        else:
            ages = [21]

        if 'zip_code' in request.GET and request.GET['zip_code']:
            zip_code = int(request.GET['zip_code'])
        if 'income' in request.GET and request.GET['income']:
            income = float(request.GET['income'])
        if 'medal' in request.GET and request.GET['medal']:
            medal = request.GET['medal']
        if 'medical_visits' in request.GET and request.GET['medical_visits']:
            doctor_use = float(request.GET['medical_visits'])
        else:
            for age in ages:
                doctor_use += doctor_use_by_age(age)
        if 'prescription_use' in request.GET and request.GET['prescription_use']:
            prescription_use = float(request.GET['prescription_use'])
        else:
            for age in ages:
                prescription_use += prescription_use_by_age(age)

        try:
            area = GeographicArea.objects.select_related().get(zip_code=zip_code)
            plans = area.plan_set.filter(age=21)
        except:
            data = serializers.serialize('json', [])
            return HttpResponse(data, content_type='application/json')
        if medal != 'all':
            result_plans = plans.filter(medal=medal.capitalize()).order_by('price')[:10]
        else:
            bronze_plans = plans.filter(medal='Bronze').order_by('price')[:3]
            silver_plans = plans.filter(medal='Silver').order_by('price')[:3]
            gold_plans = plans.filter(medal='Gold').order_by('price')[:3]
            platinum_plans = plans.filter(medal='Platinum').order_by('price')[:3]

            from itertools import chain
            result_plans = list(chain(bronze_plans, silver_plans, gold_plans, platinum_plans))

        second_lowest_silver_plan = plans.filter(medal='Silver').order_by('price')[:2][1]
        second_lowest_silver_price = float(second_lowest_silver_plan.price) * 12
        yearly_subsidy = get_subsidy(ages, income, second_lowest_silver_price)
        monthly_subsidy = yearly_subsidy/12
        #result_plans.prefetch_related('provider')
        if not result_plans:
            data = serializers.serialize('json', [])
            return HttpResponse(data, content_type='application/json')
        plans = get_plans_data(result_plans, ages, prescription_use, doctor_use, monthly_subsidy)
        data = serializers.serialize('json',
                                     plans,
                                     relations=('provider',),
                                     excludes=('areas',),
                                     extras=('total_out_of_pocket_cost',
                                             'example_procedure_cost',
                                             'out_of_pocket_max',
                                             'out_of_pocket_cost_number',
                                             'deductible',
                                             'coinsurance_rate',
                                             'insurance_savings',
                                             'example_procedure_savings',
                                             'total_monthly_premium'
                                     )
        )
        return HttpResponse(data, content_type='application/json')


def plans(request):
    return render_to_response('plan-cols.html', context_instance=RequestContext(request))
