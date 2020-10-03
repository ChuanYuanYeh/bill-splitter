import os
import sys
import math
import pandas as pd
import numpy as np

PATH_PREFIX = 'bills/'

def execute(filename):
    try:
        data = pd.read_excel(os.path.join(PATH_PREFIX, '{}.xls'.format(filename)))
    except Exception:
        print('Unable to read file or file does not exist.')
        return

    priceToPay = {}
    for col in data:
        if col not in ['Items','Price']:
            priceToPay[col]=0

    for idx,row in data.iterrows():
        print('Calculating item: {}'.format(row['Items']))
        total=row['Price']
        denom=0
        print('People responsible:')
        for idx, ate in enumerate(row[2:]):
            if ate != 'x':
                print(row[2:].index[idx])
                denom += 1
        pricePerPerson = total/denom
        print('Price per person responsible: {}\n'.format(pricePerPerson))
        for idx, ate in enumerate(row[2:]):
            if ate != 'x':
                priceToPay[row[2:].index[idx]] += pricePerPerson

    print('FINAL CALCULATION:')
    for key,value in priceToPay.items():
        print('{}: {} B'.format(key, round(math.floor(value), -1)))


if __name__ == "__main__":
    filename = input('Name of excel sheet with file extension:')
    execute(filename)