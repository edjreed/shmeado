import os
import json

def get_constants(page):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    constants_dir = os.path.abspath(os.path.join(current_dir, 'constants', f'{page}.json'))
    
    with open(constants_dir, encoding='utf-8') as constants_json:
        return json.load(constants_json)