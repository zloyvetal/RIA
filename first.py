"""
Пробуем создать утилиту, которая будет отслеживать уебков, которые скручивают километраж на мажинах и их перепродают

"""
import urllib3
import json

my_kay = "mnrOlvNOeTnNJHyFrkjk6RFZ0NfDkftYxlO2cD1t"


def create_json_with_data(input_url: str, api_key: str, json_name: str):
    http = urllib3.PoolManager()

    our_url = f'{input_url}'.replace('YOUR_API_KEY', api_key)

    our_url = http.request('GET', our_url)
    decode_dict = our_url.data.decode('utf-8')
    # open str to list
    data_from_api = json.loads(decode_dict)

    # add to json, mark_cars
    with open(f'{json_name}.json', 'w') as f:
        json.dump(data_from_api, f)


def url_search(search_url: str) -> str:
    # create full search line
    search_line = f"https://developers.ria.com/auto/search?api_key=YOUR_API_KEY&url_search={search_url}"
    return search_line


def find_id(json_name: str) -> tuple:
    # open json with data
    all_search_data = json.load(open(f'{json_name}'))

    # list with id's
    new_cars = all_search_data['result']['search_result']['ids']

    # list with id's cars who was used
    old_cars = all_search_data['result']['search_result_common']['data']

    list_of_used_cars = []

    for ids in old_cars:
        list_of_used_cars.append(ids['id'])

    new_and_old_cars = (new_cars, old_cars)

    return new_and_old_cars


