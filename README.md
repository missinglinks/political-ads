# Political Ads Datasets

Provides scripts to build datasets of political ads on Facebook and Google services for specific countries.


## Facebook dataset

Create `config.yaml`file:

```yaml
access_token: <Facebook app token>
out_dir: data
countries:
  - AT
```

Run `facebook_ads.py`

```zsh
python facebook_ads.py
```

This creates a new dataset and saves it as a .csv and .json file:  
* `facebook_ads_COUNTRY_TIMESTAMP.csv
* `facebook_ads_COUNTRY_TIMESTAMP.json