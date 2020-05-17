"""
Пробуем создать утилиту, которая будет отслеживать уебков, которые скручивают километраж на мажинах и их перепродают

"""
import urllib3
import json

my_kay = "mnrOlvNOeTnNJHyFrkjk6RFZ0NfDkftYxlO2cD1t"


def create_json_with_data(input_url: str, api_key: str, json_name: str):
    """
    This function for download data from API and save it in .json file.
    :param input_url:
    :param api_key:
    :param json_name:
    :return:
    """
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


def find_id(json_name: str) -> list:
    # open json with data
    all_search_data = json.load(open(f'{json_name}'))

    # list with id's
    new_cars = all_search_data['result']['search_result']['ids']

    # list with id's cars who was used
    old_cars = all_search_data['result']['search_result_common']['data']

    list_of_used_cars = []

    for ids in old_cars:
        list_of_used_cars.append(ids['id'])

    output_cars = []
    for i in new_cars:
        output_cars.append(i)
    for i in list_of_used_cars:
        output_cars.append(i)

    return output_cars


def read_from_id(list_with_ids: list):
    for ids in list_with_ids:
        create_json_with_data(f'https://developers.ria.com/auto/info?api_key=YOUR_API_KEY&auto_id={ids}', my_kay,
                              f'{ids}.json')


lets_try = find_id('bmwX6.json')

read_from_id(lets_try)
