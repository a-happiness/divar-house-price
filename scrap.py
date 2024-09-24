import requests
from bs4 import BeautifulSoup
import csv

# from houses_price.house_price import response

with open('./tokens.txt', 'r') as file:
    tokens = file.readline().split(',')
print(tokens)

data = []

for token in tokens:
    url = f'https://divar.ir/v/-/{token}'
    print(url)
    response = requests.get(url)
    print(f'{response=}')
    # if response.status_code != 200:
    #     print('###############')
    #     i = 0
    #     while i<10:
    #
    #         response = requests.get(url)
    #         if response.status_code == 200:
    #             break
    #         i+=1
    #         print('****')
    # else:
    #     print(f'Failed to retrieve data for token :{token}')


    # print(f'{response=}')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        information = soup.select('tr td.kt-group-row-item__value')
        if information:
            area = int(information[0].get_text(strip=True))
            # print('area')
            construction = int(information[1].get_text(strip=True))
            rooms = int(information[2].get_text(strip=True))
            elevator = False if 'ندارد' in information[3].get_text(strip=True) else True
            parking = False if 'ندارد' in information[4].get_text(strip=True) else True
            warehouse = False if 'ندارد' in information[5].get_text(strip=True) else True

            price = soup.select_one('div p.kt-unexpandable-row__value').get_text(strip=True)
            address = soup.select_one('div div.kt-page-title__subtitle--responsive-sized').get_text(strip=True)

            data.append([token, area, construction, rooms, elevator, parking, warehouse, price, address])
        print(f'{data=}')
    else:
        print(f'Failed to retrieve data for tokennn :{token}')


print(len(data))
