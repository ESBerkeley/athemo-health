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
        zip_code = 94704
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

        area = GeographicArea.objects.get(zip_code=zip_code)

        plans = area.plan_set.filter(age__in=ages)
        print(plans)
        plan_list = [plan for plan in plans]
        for plan in plan_list:
            plan.prescription_cost = [{'name':'prescription_cost',
                                       'value':prescription_use*500}]
            plan.doctor_cost = [{'name':'doctor_cost',
                                 'value':doctor_use*20}]
        data = serializers.serialize('json',
                                     plan_list,
                                     extras=('prescription_cost', 'doctor_cost'))
        return HttpResponse(data, 'application/javascript')


def plans(request):
    return render_to_response('plan-cols.html', context_instance=RequestContext(request))
