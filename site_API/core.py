from pprint import pprint

from config import ConfigSettings
from site_API.utils.site_api_handler import SiteApiInterface

config = ConfigSettings()


headers = {
    'X-RapidAPI-Key': config.api_key.get_secret_value(),
    'X-RapidAPI-Host': config.host_api
}

url = 'https://' + config.host_api
params = {"page": "1", "country": "russia", "country_code": "ru"}

site_api = SiteApiInterface()

search = site_api.make_response()
response = search(url, 'iphone', headers, params)
pprint(sorted(response.json()['products'], key=lambda x: x['price']['value']))

if __name__ == '__main__':
    site_api()
