# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from utils import get_plans_data

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

        income = 0
        doctor_use = 0
        prescription_use = 0

        if 'zip_code' in request.GET and request.GET['zip_code']:
            zip_code = int(request.GET['zip_code'])
        if 'income' in request.GET and request.GET['income']:
            income = float(request.GET['income'])
        if 'medical_visits' in request.GET and request.GET['medical_visits']:
            doctor_use = float(request.GET['medical_visits'])
        if 'prescription_use' in request.GET and request.GET['prescription_use']:
            prescription_use = float(request.GET['prescription_use'])

        if request.GET.getlist('age') and request.GET['age']:
            ages = request.GET.getlist('age')
            ages = map(int, ages)
        else:
            ages = [21]

        plans = get_plans_data(ages, zip_code, income, prescription_use, doctor_use)
        data = serializers.serialize('json',
                                     plans,
                                     relations=('provider',),
                                     extras=('total_out_of_pocket_cost', 'total_insurance_payment', 'savings',
                                     'out_of_pocket_cost_number'))
        return HttpResponse(data, mimetype='application/json')


def plans(request):
    return render_to_response('plan-cols.html', context_instance=RequestContext(request))
