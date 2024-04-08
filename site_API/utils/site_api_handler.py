import requests
from typing import Dict


def _make_response(url: str, search_query: str,
                   headers: Dict, params: Dict,
                   timeout: int = 10, success=200):

    total_url = '{0}/{1}'.format(url, search_query)
    response = requests.get(
        total_url,
        headers=headers,
        params=params,
        timeout=timeout
    )
    status_code = response
    if status_code == success:
        return response
    return status_code


class SiteApiInterface:

    @classmethod
    def make_response(cls):
        return _make_response
