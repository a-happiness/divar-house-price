import requests
from bs4 import BeautifulSoup
import pandas as pd

with open('./tokens.txt', 'r') as file:
    tokens = file.readline().split(',')

l = []
column_title = ['title', 'district_persian', 'price', 'square', 'price per meter', 'url']
df = pd.DataFrame(columns=column_title)

for token in tokens:
    url = f'https://api.divar.ir/v8/posts-v2/web/{token}'
    response = requests.get(url)
    json_data = response.json()
    data = json_data['sections']
    for i in range(len(data)):
        if data[i]['section_name'] == 'LIST_DATA':
            widgets = data[i].get('widgets')
            square_widget = widgets[0].get('data').get('items')
            if square_widget:
                for k in range(len(square_widget)):
                    if square_widget[k].get('title') == 'متراژ':
                        l.append(square_widget[k]['value'])
            for j in range(1, len(widgets)):
                item = widgets[j].get('data')
                if item.get('title') == 'قیمت کل':
                    l.append(item['value'])
                if item.get('title') == 'قیمت هر متر':
                    l.append(item['value'])
    url = json_data['share']['web_url']
    info = json_data['seo']['web_info']
    title = info.get('title')
    district_persian = info.get('district_persian')
    l.append(url)
    l.append(title)
    l.append(district_persian)
print(l)
