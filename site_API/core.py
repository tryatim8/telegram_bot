from pprint import pprint

from config import ConfigSettings
from site_API.utils.site_api_handler import SiteApiInterface

config = ConfigSettings()


headers = {
    'X-RapidAPI-Key': config.api_key.get_secret_value(),
    'X-RapidAPI-Host': config.host_api,
}

url = ''.join(('https://', config.host_api))
query_params = {'country': 'DE'}

site_api = SiteApiInterface()

if __name__ == '__main__':
    amazon_search = site_api.search_products()
    response = amazon_search(url, 'iphone', headers, query_params)
    pprint(sorted(
        response.json()['result'],
        key=lambda elem: elem['price']['current_price'],
        reverse=True,
    ))

    amazon_info = site_api.product_details()
    response = amazon_info(url, 'B093X64R9H', headers, query_params)
    pprint(response.json())
