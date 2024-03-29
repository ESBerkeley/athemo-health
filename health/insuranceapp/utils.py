__author__ = 'ericxiao'
from models import GeographicArea, HealthcarePlan, Provider

# 58% of visits to primary care, $150 median
# 35% to specialty care
# $130 urgent care, $500 emergency care
AVG_DOCTOR_COST = .58*150 + .35*270 + .05*130 + .02*500

# GENERIC = 44.14, 78% of drugs
# BRAND_NAME = 166.01, 22% of drugs
AVG_PRESCRIPTION_COST = 44.14*.78 + 166.01*.22

# LOW-HIGH COSTS 5500-18000 for prenatal tests + live-birth
MATERNITY_COST = 10000

#AVG COST 7900, minus doctor visits?
AVG_DIABETES_COST = 6000

def get_plans_data(result_plans, ages, prescription_use, doctor_use, monthly_subsidy):
    '''
    Your premium + your deductible + any coinsurance
    you must pay (up to your out-of-pocket maximum) +
    any copayments = the most you will pay for healthcare each year (for covered services).
    '''

    total_prescription_cost = prescription_use*AVG_PRESCRIPTION_COST
    total_doctor_cost = doctor_use*AVG_DOCTOR_COST
    max_hospital_cost = 0

    for plan in result_plans:
        total_monthly_premium = 0
        for age in ages:
            max_hospital_cost = max(hospital_cost(age), max_hospital_cost)
            age = max(20,age)
            age = min(64,age)
            total_monthly_premium += float(plan.price)*AGE_RATIOS[age]
        total_monthly_premium -= monthly_subsidy
        total_monthly_premium = max(total_monthly_premium, (PERSON_TO_POVERTY_LINE[len(ages)]*.02)/12)
        plan_details = MEDAL_DETAILS[plan.medal]
        if len(ages) > 1:
            deductible = plan_details['family_deductible']
            max_out_of_pocket = plan_details['max_out_of_pocket_family']
        else:
            deductible = plan_details['individual_deductible']
            max_out_of_pocket = plan_details['max_out_of_pocket']

        if plan.medal == 'Bronze':
            # USED FOR CALCULATIONS OF COPAY FOR BRONZE
            out_of_pocket_costs = calculate_bronze_cost(deductible, prescription_use, doctor_use, plan_details)
            out_of_pocket_doctor_costs = out_of_pocket_costs[0]
            out_of_pocket_prescription_costs = out_of_pocket_costs[1]
        else:
            out_of_pocket_doctor_costs = doctor_use * plan_details['avg_doctor_copay']
            out_of_pocket_prescription_costs = prescription_use * plan_details['avg_prescription_copay']

        coinsurance_rate = plan_details['coinsurance_rate']
        maternity_cost = coinsurance_rate * MATERNITY_COST
        diabetes_cost = coinsurance_rate * AVG_DIABETES_COST
        oop_hospital_cost = coinsurance_rate * max_hospital_cost

        maternity_savings = MATERNITY_COST - maternity_cost
        diabetes_savings = AVG_DIABETES_COST - diabetes_cost
        hospital_savings = max_hospital_cost - oop_hospital_cost

        max_procedure_cost = max(maternity_cost, diabetes_cost, oop_hospital_cost)

        #total_uninsured_cost = total_prescription_cost + total_doctor_cost
        #savings = total_uninsured_cost - out_of_pocket_cost
        insurance_prescription_payment = total_prescription_cost - out_of_pocket_prescription_costs
        insurance_doctor_payment = total_doctor_cost - out_of_pocket_doctor_costs
        #insurance_payment = insurance_prescription_payment + insurance_doctor_payment
        plan.total_monthly_premium = format(total_monthly_premium, '.2f') #2 decimal places
        plan.out_of_pocket_cost_number = int(total_monthly_premium * 12 + \
                             out_of_pocket_doctor_costs + \
                             out_of_pocket_prescription_costs)

        plan.total_out_of_pocket_cost = [{'name':'annual_premium', 'value': int(total_monthly_premium*12)},
                                        {'name':'prescription_cost', 'value': int(out_of_pocket_prescription_costs)},
                                        {'name':'doctor_cost', 'value': int(out_of_pocket_doctor_costs)}]

        plan.out_of_pocket_max = int(max_out_of_pocket)
        #plan.out_of_pocket_cost_number = int(out_of_pocket_cost)
        #plan.savings = int(savings)
        plan.insurance_savings = {'prescription_savings': int(insurance_prescription_payment),
                                  'doctor_savings': int(insurance_doctor_payment)}
        plan.example_procedure_cost = {'maternity_cost': int(maternity_cost),
                                       'hospitalization_cost': int(oop_hospital_cost),
                                       'diabetes_cost': int(diabetes_cost)}
        plan.example_procedure_savings = {'maternity_savings': int(maternity_savings),
                                           'hospitalization_savings': int(hospital_savings),
                                           'diabetes_savings': int(diabetes_savings)}

        plan.deductible = deductible
        plan.coinsurance_rate = coinsurance_rate

        #plan.total_insurance_payment = [{'name':'prescription_cost', 'value': insurance_prescription_payment},
        #                                {'name':'doctor_cost', 'value': insurance_doctor_payment}]

    return sorted(result_plans, key=lambda x: x.out_of_pocket_cost_number)

def get_subsidy(ages, income, second_lowest_plan_cost):
    '''adult_ages = [age for age in ages if age >= 21]
    num_adults = len(adult_ages)
    num_children = len(ages) - num_adults
    url = 'kff.org/interactive/subsidy-calculator/' + \
          '#state=CA&zip='+str(zip_code)+\
          '&income-type=dollars&income='+str(income)+\
          '&employer-coverage=0&people='+str(len(ages))+\
          '&alternate-plan-family=individual&adult-count='+str(num_adults)
    for age in adult_ages:
        url += '&adults%5B0%5D%5Bage%5D='+str(age)+'&adults%5B0%5D%5Btobacco%5D=0'
    url += '&child-count='+str(num_children)+'&child-tobacco=0'''''
    premium_percent = poverty_level(len(ages), income)
    income = max(PERSON_TO_POVERTY_LINE[len(ages)], income)
    max_payment = premium_percent * income
    if max_payment < second_lowest_plan_cost:
        print(second_lowest_plan_cost - max_payment)
        return second_lowest_plan_cost - max_payment
    else:
        return 0

def poverty_level(num_people, income):
    poverty_line = PERSON_TO_POVERTY_LINE[num_people]
    if income < poverty_line * 1.33:
        return 0.02
    elif income < poverty_line * 1.50:
        return 0.03 + (income/poverty_line - 1.33)/17
    elif income < poverty_line * 2:
        return 0.04 + (income/poverty_line - 1.5)/21.74
    elif income < poverty_line * 2.5:
        return 0.063 + (income/poverty_line - 2)/28.57
    elif income < poverty_line * 3:
        return 0.0805 + (income/poverty_line - 2.5)/34.483
    elif income < poverty_line * 4:
        return 0.095
    else:
        return 1

def hospital_cost(age):
    if age < 18:
        return 8200
    elif age < 45:
        return 7200
    elif age < 65:
        return 12100
    elif age < 85:
        return 12300
    elif age >= 85:
        return 9600

def doctor_use_by_age(age):
    if age < 18:
        return 3
    elif age < 44:
        return 4
    elif age < 64:
        return 6
    elif age >= 64:
        return 8

def prescription_use_by_age(age):
    if age < 18:
        return 5
    elif age < 44:
        return 9
    elif age < 64:
        return 21
    elif age >= 64:
        return 33

def calculate_bronze_cost(deductible, prescription_use, doctor_use, plan_details):
    remaining_deductible = deductible
    remaining_prescriptions = prescription_use
    remaining_doctor_visits = doctor_use
    is_doctor_cost = True

    while remaining_deductible > 0 and \
        (remaining_prescriptions > 0 or remaining_doctor_visits > 0):

        if is_doctor_cost and remaining_doctor_visits > 0:
            remaining_deductible -= AVG_DOCTOR_COST
            remaining_doctor_visits -= 1
        elif remaining_prescriptions > 0:
            remaining_deductible -= AVG_PRESCRIPTION_COST
            remaining_prescriptions -= 1

        is_doctor_cost = not is_doctor_cost
    out_of_pocket_doctor_costs = remaining_doctor_visits*plan_details['avg_doctor_copay'] + \
                              (doctor_use - remaining_doctor_visits)*AVG_DOCTOR_COST
    out_of_pocket_prescription_costs = remaining_prescriptions*plan_details['avg_prescription_copay'] + \
                                   (prescription_use - remaining_prescriptions)*AVG_PRESCRIPTION_COST
    if is_doctor_cost and remaining_deductible < 0: #LAST THING PAID FOR IS PRESCRIPTION
        out_of_pocket_prescription_costs += abs(remaining_deductible)
    elif not is_doctor_cost and remaining_deductible < 0: #LAST THING PAID FOR IS DOCTOR_VISIT
        out_of_pocket_doctor_costs += abs(remaining_deductible)
    return (out_of_pocket_doctor_costs, out_of_pocket_prescription_costs)

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
          'max_out_of_pocket_family': 12700,
          'coinsurance_rate': .30}
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
          'max_out_of_pocket_family': 12700,
          'coinsurance_rate': .20}
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
          'max_out_of_pocket_family': 12700,
          'coinsurance_rate': .20}
PLATINUM = {'primary_care_copay': 20,
          'specialty_care_copay': 40,
          'urgent_care_copay': 40,
          'emergency_room_copay': 150,
          'avg_doctor_copay': .58*20 + .35*40 + .05*40 + .02*150,
          'individual_deductible': 0,
          'family_deductible': 0,
          'generic_copay': 5,
          'preferred_brand_copay': 15,
          'avg_prescription_copay': .78*19 + .22*50,
          'max_out_of_pocket': 4000,
          'max_out_of_pocket_family': 8000,
          'coinsurance_rate': .10}
PERSON_TO_POVERTY_LINE = {1: 11490,
                         2: 15510,
                         3: 19530,
                         4: 23550,
                         5: 27570,
                         6: 31590,
                         7: 35610,
                         8: 39630}

MEDAL_DETAILS = {'Bronze': BRONZE, 'Silver': SILVER, 'Gold': GOLD, 'Platinum': PLATINUM, 'Catastrophic': BRONZE}

AGE_RATIOS = {20: 0.635, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1.004, 26: 1.024, 27: 1.048, 28: 1.087, 29: 1.119, 30: 1.135, 31: 1.159, 32: 1.183, 33: 1.198, 34: 1.214, 35: 1.222, 36: 1.23, 37: 1.238, 38: 1.246, 39: 1.262, 40: 1.278, 41: 1.302, 42: 1.325, 43: 1.357, 44: 1.397, 45: 1.444, 46: 1.5, 47: 1.563, 48: 1.635, 49: 1.706, 50: 1.786, 51: 1.865, 52: 1.952, 53: 2.04, 54: 2.135, 55: 2.23, 56: 2.333, 57: 2.437, 58: 2.548, 59: 2.603, 60: 2.714, 61: 2.81, 62: 2.873, 63: 2.952, 64: 3}
