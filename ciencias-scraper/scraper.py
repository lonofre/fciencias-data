import requests
from bs4 import BeautifulSoup
import re

ciencias_url = 'http://www.fciencias.unam.mx'

def get_soup(url):
    '''Gets the BeautifulSoup object'''

    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def extract_urls(links, pattern) -> list:
    '''Extracts the url from html <a> tag
    Parameters
        links (list): A list of <a> tags
        pattern: Regular expression to filter the url
    
    Returns
        list: a list of str with the urls
    '''

    urls = [link['href'] for link in links] 
    cleaned_urls = [url for url in urls if re.search(pattern, url)]
    return cleaned_urls

def majors_url(semester: str = '') -> list:
    '''Gets the links of the pages where there are all the classes
    for a major in a given semester

    Parameters
        semester (str): The semester that will be scraped, for instance: 20201,
        20202.

    Returns
        list: A list with all the urls
    '''

    schedules_url = '/docencia/horarios/Indice/'
    soup = get_soup(ciencias_url + schedules_url + semester)
    content = soup.find(id = 'info-contenido')
    urls = extract_urls(content.find_all('a'), r"\bindiceplan\b")
    return [ciencias_url + url for url in urls]

def classes_url(plan_url: str) -> list:
    '''Gets the links for all the clases for a given plan major
    
    Parameters
        plan_url (str): The url that will be scraped

    Returns
        list: A list with all the urls
    '''
    soup = get_soup(plan_url)
    content = soup.find(id = 'info-contenido')
    urls = extract_urls(content.find_all('a'), r"\bdocencia\b")
    return [ciencias_url + url for url in urls]
