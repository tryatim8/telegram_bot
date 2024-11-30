import copy

import requests
from typing import Dict


def _search_products(url: str, product_name: str,
                     headers: Dict, params: Dict,
                     timeout: int = 10, success=200):
    """Обработчик SiteAPI. Возвращает поисковый запрос по названию товара - product_name"""
    total_params = copy.deepcopy(params)
    total_params['query'] = product_name
    total_url = '{}/product-search'.format(url)
    response = requests.get(
        total_url,
        headers=headers,
        params=total_params,
        timeout=timeout
    )
    return response


def _product_details(url: str, product_asin: str,
                     headers: Dict, params: Dict,
                     timeout: int = 10, success=200):
    """Обработчик SiteAPI. Возвращает информацию о товаре по коду товара - product_asin"""
    total_params = copy.deepcopy(params)
    total_params['asin'] = product_asin
    total_url = '{}/product-details'.format(url)
    response = requests.get(
        total_url,
        headers=headers,
        params=total_params,
        timeout=timeout
    )
    return response


class SiteApiInterface:
    @classmethod
    def search_products(cls):
        return _search_products

    @classmethod
    def product_details(cls):
        return _product_details
