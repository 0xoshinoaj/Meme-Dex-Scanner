import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class BaseSecurityChecker:
    def __init__(self, name):
        self.name = name

    def check_security(self, contract_address):
        raise NotImplementedError("This method should be implemented by subclasses")

    def _get_soup(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
