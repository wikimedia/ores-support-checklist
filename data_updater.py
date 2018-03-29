import requests
import time
import json
import os

from collections import defaultdict, Mapping


def update(d, u):
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def get_ores_data():
    r = requests.get('https://ores.wikimedia.org/v3/scores/')
    return r.json()


def get_wikilabels_data_per_wiki(base_url, wiki):
    parsed_data = {}
    valid_forms = [
        'damaging_and_goodfaith',
        'wp10',
        'draftquality',
        'edit_type'
    ]
    wiki_data = requests.get(
        base_url + wiki + '/?campaigns=stats').json()['campaigns']
    for campaign in wiki_data:
        if campaign['form'] in valid_forms:
            parsed_data[campaign['form']] = {
                'id': campaign['id'],
                'done': campaign['stats']['labels'],
                'total': campaign['stats']['tasks']
            }
    return parsed_data


def get_wikilabels_data():
    base_url = 'https://labels.wmflabs.org/campaigns/'
    wikis = requests.get(base_url).json()['wikis']
    data = defaultdict(dict)
    for wiki in wikis:
        data[wiki]['campaigns'] = get_wikilabels_data_per_wiki(base_url, wiki)
        time.sleep(1)

    return data


def main():
    data = get_ores_data()
    data = update(data, get_wikilabels_data())
    data = {'data': data, 'timestamp': time.time()}
    path = os.path.dirname(os.path.abspath(__file__)) + '/static/data.json'
    with open(path, 'w') as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    main()
