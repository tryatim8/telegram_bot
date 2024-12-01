import copy
from typing import Dict

import requests


def _search_products(
    url: str,
    product_name: str,
    headers: Dict,
    query_params: Dict,
    timeout: int = 10,
) -> requests.Response:
    """Обработчик SiteAPI. Возвращает информацию по product_name."""
    total_params = copy.deepcopy(query_params)
    total_params['query'] = product_name
    total_url = '{0}/product-search'.format(url)
    return requests.get(
        total_url,
        headers=headers,
        params=total_params,
        timeout=timeout,
    )


def _product_details(
    url: str,
    product_asin: str,
    headers: Dict,
    query_params: Dict,
    timeout: int = 10,
) -> requests.Response:
    """Обработчик SiteAPI. Возвращает информацию по product_asin."""
    total_params = copy.deepcopy(query_params)
    total_params['asin'] = product_asin
    total_url = '{0}/product-details'.format(url)
    return requests.get(
        total_url,
        headers=headers,
        params=total_params,
        timeout=timeout,
    )


class SiteApiInterface:
    """API-интерфейса сайта."""

    @classmethod
    def search_products(cls):
        """Метод API-интерфейса сайта. Возвращает информацию по product_name."""
        return _search_products

    @classmethod
    def product_details(cls):
        """Метод API-интерфейса сайта. Возвращает информацию по product_asin."""
        return _product_details
