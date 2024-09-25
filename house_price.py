import requests

json_data = {
    'city_ids': [
        '6',
    ],
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
    },
}

response = requests.post('https://api.divar.ir/v8/postlist/w/search', json=json_data)

data = response.json()

list_of_tokens = []

count = 0
while True:
    last_post_date = data['pagination']['data']['last_post_date']
    layer_page = data['pagination']['data']['layer_page']
    page = data['pagination']['data']['page']
    search_uid = data['pagination']['data']['search_uid']

    json = {
        'city_ids': [
            '6',
        ],
        'pagination_data': {
            '@type': 'type.googleapis.com/post_list.PaginationData',
            'last_post_date': last_post_date,
            'page': page,
            'layer_page': layer_page,
            'search_uid': search_uid,
        },
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

    tokens = data['action_log']['server_side_info']['info']['tokens']
    for token in tokens:
        list_of_tokens.append(token)

        count += 1
    if count >= 1000:
        break

txt_file = open('tokens.txt', 'w', encoding='utf8')
txt_file.write(','.join(list_of_tokens))
txt_file.close()
