from pprint import pprint

from config import ConfigSettings
from site_API.utils.site_api_handler import SiteApiInterface

config = ConfigSettings()


headers = {
    'X-RapidAPI-Key': config.api_key.get_secret_value(),
    'X-RapidAPI-Host': config.host_api
}

url = 'https://' + config.host_api
params = {'country': 'DE'}

site_api = SiteApiInterface()

# amazon_search = site_api.search_products()
# response = amazon_search(url, 'iphone', headers, params)
# pprint(sorted(response.json()['result'], key=lambda x: x['price']['current_price'], reverse=True))
#
# amazon_info = site_api.product_details()
# response = amazon_info(url, 'B093X64R9H', headers, params)
# pprint(response.json())

if __name__ == '__main__':
    site_api()
