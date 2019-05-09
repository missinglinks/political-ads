#!/usr/bin/env python
# coding: utf-8

import requests
import json 
import pandas as pd
import os
import yaml
from datetime import datetime

URL_SEARCH = 'https://graph.facebook.com/v3.3/ads_archive?ad_active_status={status}&fields={fields}&search_terms={q}&ad_reached_countries={countries}&access_token={token}&limit=5000'
URL_PAGE  = 'https://graph.facebook.com/v3.3/ads_archive?ad_active_status={status}&fields={fields}&search_page_ids={ids}&ad_reached_countries={countries}&access_token={token}&limit=5000'

#default values
STATUS = 'ALL'
FIELDS = 'ad_snapshot_url,currency,ad_creative_link_title,ad_creation_time,ad_creative_body,ad_creative_link_caption,ad_delivery_start_time,ad_delivery_stop_time,funding_entity,impressions,page_id,page_name,spend'
SEARCH_TERMS = '*'
COUNTRIES = [ 'AT' ]
OUT_dir = 'data'

def load_config():
    config = yaml.safe_load(open('config.yaml'))
    return config

def build_dataset(output):

    cf = load_config()
    token = cf['access_token']
    if 'countries' in cf:
        countries = cf['countries']
    else:
        countries = COUNTRIES
    if 'out_dir' in cf:
        out_dir = cf['out_dir']
    else:
        out_dir = OUT_DIR
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    url = URL_SEARCH.format(
        status=STATUS,
        fields=FIELDS,
        q=SEARCH_TERMS,
        countries=str(countries),
        token=token
    )

    dataset = {}

    while True:

        rsp = requests.get(url)
        d = rsp.json()
        data = d['data']

        if 'paging' in d:
            url = d['paging']['next']
        else:
            break

        print("fetched ads: ", len(data))

        for entry in data:
            if entry['ad_snapshot_url'] not in dataset:
                dataset[entry['ad_snapshot_url']] = entry
        
    # save datasets
    timestamp = datetime.now().isoformat()
    c = "_".join(countries)

    filename_base = 'facebook_ads_{}_{}'.format(
        c,
        timestamp
    )

    out_file_json = os.path.join(
        out_dir,
        "{}.json".format(filename_base)
    )
    out_file_csv = os.path.join(
        out_dir,
        "{}.csv".format(filename_base)
    )

    json.dump(dataset, open(out_file_json, 'w'), indent=4)


    for entry in dataset.values():

        if 'spend' in entry:
            entry['spend_lower'] = entry['spend']['lower_bound']
            entry['spend_upper'] = entry['spend']['upper_bound']
            entry['spend'] = "{}-{}".format(
                entry['spend_lower'],
                entry['spend_upper']
            )

        if 'impressions' in entry:
            entry['impressions_lower'] = entry['impressions']['lower_bound']
            entry['impressions_upper'] = entry['impressions']['upper_bound']
            entry['impressions'] = "{}-{}".format(
                entry['impressions_lower'],
                entry['impressions_upper']
            )


    df = pd.DataFrame(list(dataset.values()))
    df.to_csv(out_file_csv)


if __name__ == '__main__':
    build_dataset("tmp")