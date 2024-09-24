import requests

json_data = {
    'city_ids': [
        '6',
    ],

    'action_log': {
        'server_side_info': {
            'info': {
                'last_post_date_epoch': '1726555761321150'
            }
        }
    },
    'source_view': 'CATEGORY',
    'search_data': {
        'form_data': {
            'data': {
                'category': {
                    'str': {
                        'value': 'residential-sell',
                    },
                },
            },
        },
        'server_payload': {
            '@type': 'type.googleapis.com/widgets.SearchData.ServerPayload',
            'additional_form_data': {
                'data': {
                    'sort': {
                        'str': {
                            'value': 'sort_date',
                        },
                    },
                },
            },
        },
    },
}

response = requests.post('https://api.divar.ir/v8/postlist/w/search', json=json_data)
# if not response:
#     print(response)
#     print(response.json())
#     raise Exception()
data = response.json()
last_post_date = data['action_log']['server_side_info']['info']['last_post_date_epoch']

list_of_tokens = []

count = 0
while True:
    json = {
        'city_ids': [
            '6',
        ],
        'action_log': {
            'server_side_info': {
                'info': {
                    'last_post_date_epoch': last_post_date
                }
            }
        },
        'source_view': 'CATEGORY',
        'search_data': {
            'form_data': {
                'data': {
                    'category': {
                        'str': {
                            'value': 'residential-sell',
                        },
                    },
                },
            },
            'server_payload': {
                '@type': 'type.googleapis.com/widgets.SearchData.ServerPayload',
                'additional_form_data': {
                    'data': {
                        'sort': {
                            'str': {
                                'value': 'sort_date',
                            },
                        },
                    },
                },
            },
        },
    }
    response = requests.post('https://api.divar.ir/v8/postlist/w/search', json=json)
    data = response.json()
    last_post_date = data['action_log']['server_side_info']['info']['last_post_date_epoch']
    # print(response.json())

    for widget in data['list_widgets']:
        token = widget['data']['action']['payload']['token']
        # print(token)
        list_of_tokens.append(token)

        count += 1

    if count >= 24:
         break
print(list_of_tokens)
print(len(list_of_tokens))
txt_file = open('tokens.txt', 'w', encoding='utf8')
txt_file.write(','.join(list_of_tokens))
txt_file.close()
