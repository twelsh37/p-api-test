# Description
# This function returns the models available to Perplexity AI. it does this by scraping the docs webpage
# https://docs.perplexity.ai/docs/model-cards
import requests
from bs4 import BeautifulSoup

def fetch_url_content(url: str) -> str:
    """
        Fetches the HTML content of a webpage given a URL.

    Args:
        url (str): The webpage URL.

    Returns:
        str: The HTML content of the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    # Deal with HTTP error
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        return ''
    # Deal with request failure
    except requests.exceptions.RequestException as err:
        print("Request Failed:", err)
        return ''

def fetch_models(url: str) -> list:
    """
    Scrapes a webpage for a table of models.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        list: The list of model names found in the webpage.
    """
    content = fetch_url_content(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('div', {'class': 'rdmd-table-inner'})

        # Extract model names
        models = [
            cell.find('code', {'tabindex': '0'}).text
            for row in table.find_all('tr')
            if (cell := row.find('td')) is not None
            and cell.find('code', {'tabindex': '0'}) is not None
        ]
        return models
    else:
        print("No content retrieved from URL.")
        return []

# Target URL
url = 'https://docs.perplexity.ai/docs/model-cards'

# Get our models
pplx_models = fetch_models(url)

# Print our models list
print(pplx_models)