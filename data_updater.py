import deep_merge
import requests
import time
import json
import os
import yamlconf

from collections import defaultdict


def get_ores_data(ores_host):
    r = requests.get(ores_host + '/v3/scores/')
    return r.json()


def get_wikilabels_data_per_wiki(base_url, wiki):
    parsed_data = {}
    valid_forms = [
        'damaging_and_goodfaith',
        'articlequality',
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


def get_wikilabels_data(wikilables_host):
    base_url = wikilables_host + '/campaigns/'
    wikis = requests.get(base_url).json()['wikis']
    data = defaultdict(dict)
    for wiki in wikis:
        data[wiki]['campaigns'] = get_wikilabels_data_per_wiki(base_url, wiki)
        time.sleep(1)

    return data


def main():
    config_path = os.path.dirname(os.path.abspath(__file__)) + '/config.yaml'
    with open(config_path, 'r') as f:
        config = yamlconf.load(f)
    data = get_ores_data(config['ores_host'])
    data = deep_merge.merge(
        data, get_wikilabels_data(config['wikilabels_host']))
    data = {'data': data, 'timestamp': time.time()}
    path = os.path.dirname(os.path.abspath(__file__)) + '/static/data.json'
    with open(path, 'w') as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    main()
