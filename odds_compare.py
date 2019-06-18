import re

def pred_to_list(pred_string):
    rows = pred_string.split('\n')
    empties = ['', ' ']
    new = []
    for row in rows:
        new_row = re.split('(-?\d+(?:\.\d+)?)', row)
        new_row = [item for item in new_row if item not in empties]
        new.append(new_row)
    return new
