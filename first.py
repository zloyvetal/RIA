"""
Пробуем создать утилиту, которая будет отслеживать редисок, которые скручивают километраж на мажинах и их перепродают

"""
import urllib3
import json
import requests

my_kay = "mnrOlvNOeTnNJHyFrkjk6RFZ0NfDkftYxlO2cD1t"


def url_search(search_url: str) -> str:
    # берет строку с функции take_search_string и добавляет ее в полную строку для запроса
    search_line = f"https://developers.ria.com/auto/search?api_key=YOUR_API_KEY&{search_url}"
    return search_line


def take_search_string(url_from_site: str, key: str) -> str:
    # берет поисковую строку с сайта и превращает ее в поисковую строку для апи
    r = requests.get(f'https://developers.ria.com/new_to_old?api_key={key}&{url_from_site}')
    data = json.loads(r.text)
    return data['string']


def create_json_with_data(input_url: str, api_key: str, json_name: str):
    """
    принимает готовую поисковую строку с функции - url_search и отправляет запрос к АП
    после ответа - сохраняет данные в файл с названием json_name которое тоже передается в эту функцию
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


def find_id(json_name: str) -> list:
    """
    Принимается имя файла который должен быть уже создан на пк, с данными от АПИ и достаются от туда все айдишники
    объявлений

    """

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
                              f'{ids}')


def main():

    create_json_with_data(
        url_search(take_search_string('categories.main.id=1&indexName=auto&brand.id[0]=47&model.id[0]=393', my_kay)),
        my_kay, 'Mazda6')
    read_from_id(find_id('Mazda6.json'))


if __name__ == main():
    main()
