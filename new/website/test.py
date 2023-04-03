# sum dicts
from collections import defaultdict
import random

def sum_dicts():
    result = defaultdict(
        lambda: {'name': '', 'description': '', 'cost': 0, 'photo':'' })

    try:
        if request.method == 'GET':
                key = '{}-{}'.format(item['CODE'], item['PRODUCT'])
                result[key]['CODE'] = item['CODE']
                result[key]['PRODUCT'] = item['PRODUCT']
                result[key]['COST'] += item['COST']
                result[key]['QUANTITY'] += item['QUANTITY']
                ord_tot = list(result.values())
                ord_pin = ''.join(random.choice(
                '$%&?qwertzuiopasdfghjklyxcvbnm1234567890') for i in range(length))
        elif request.method == 'POST':
                     
            print('wallet')
           
        else:
            print('else')
    except:
        redirect(404)