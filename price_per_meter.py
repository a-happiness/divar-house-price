import requests
import sqlite3

from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.formats.format import return_docstring

with sqlite3.connect('Divar.sqlite') as conn:
    cur = conn.cursor()
    cur.execute('''
    create table if not exists House_price (
        token text not null unique,
        price_per_meter integer,
        district text not null)
    ''')

# with sqlite3.connect('Divar.sqlite') as conn:
#     cur = conn.cursor()
#     cur.execute('drop table if exists House_price')
#     conn.commit()

def check_info_exists(token):
    with sqlite3.connect('Divar.sqlite') as conn:
        cur = conn.cursor()
        check_value = cur.execute('select token from House_price where token=?',
                                  (token,)).fetchone()
        return check_value


def insert_to_table(token, price_per_meter, district):
    with sqlite3.connect('Divar.sqlite') as conn:
        cur = conn.cursor()
        cur.execute('insert into House_price (token, price_per_meter, district) '
                    'values (?,?,?)',(token, price_per_meter, district))
        conn.commit()


with open('./tokens.txt', 'r') as file:
    tokens = file.readline().split(',')

for token in tokens:
    check_token = check_info_exists(token)
    if check_token is None:
        url = f'https://api.divar.ir/v8/posts-v2/web/{token}'
        response = requests.get(url)
        json_data = response.json()
        data = json_data['sections']
        for i in range(len(data)):
            if data[i]['section_name'] == 'LIST_DATA':
                widgets = data[i].get('widgets')
                for j in range(1, len(widgets)):
                    item = widgets[j].get('data')
                    if item.get('title') == 'قیمت هر متر':
                        a = item['value'].split()
                        price_per_meter = a[0].replace("٬", '')
                        print(int(price_per_meter))

        district = json_data.get('webengage').get('district')
        print(district)
        insert_to_table(token, int(price_per_meter), district)
    else:
        print(f'An ad with this token:{token} has already been saved')