import requests
from bs4 import BeautifulSoup
import re
from .tuples import Subject, ClassData, Hours, Professor 

ciencias_url = 'http://www.fciencias.unam.mx'

def get_soup(url):
    '''Gets the BeautifulSoup object'''

    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def extract_urls(pattern, links) -> list:
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


def major_urls(semester: str = '') -> list:
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

    # This pattern recognizes:
    # http://www.fciencias.unam.mx/docencia/horarios/indiceplan/20212/2017
    pattern = r"\bindiceplan\b"
    urls = extract_urls(pattern, content.find_all('a'))
    return [ciencias_url + url for url in urls]


def subject_urls(plan_url: str) -> list:
    '''Gets the links for all the subjects for a given plan major
    
    Parameters
        plan_url (str): The url that will be scraped

    Returns
        list: A list with all the urls
    '''

    soup = get_soup(plan_url)
    content = soup.find(id = 'info-contenido')
    
    # This pattern recognizes this:
    # http://www.fciencias.unam.mx/docencia/horarios/indiceplan/20212/181
    pattern = r"\bdocencia\/horarios\/\d+\/\d+\/"
    urls = extract_urls(pattern, content.find_all('a'))
    return [ciencias_url + url for url in urls]


def class_table_data(table) -> tuple:
    '''Gets the class info from a given <table> tag. Each row have the next structure:
    ROLE | PROFESSOR_NAME | DAYS | HOURS or
    ---- | DAYS | HOURS or
    ROLE | PROFESSOR_NAME
    

    Parameters
        table: a <table> tag

    Returns
        tuple: the class data 
    '''
    
    rows = table.find_all('tr')
    professors = []
    schedule = []
    for row in rows:
        columns = row.find_all('td')
        roles = re.findall(r'Ayudante|Profesor|Ayud. Lab.', columns[0].getText())
        professor = hours = None 
        if len(roles) > 0:
            role = roles[0]
            professor_name = columns[1].getText()
            professor_link = columns[1].find('a')['href']
            id = re.search('\d+', professor_link).group()
            professor = Professor(role = role, name = professor_name, id = id)
            professors.append(professor)

            # This helps to match every case of row by having DAYS at [1] position 
            # ROLE | NAME | DAYS | HOURS
            # or EMPTY | DAYS | HOURS
            columns = columns[1:]
        if len(columns) > 1:
            start, end = re.findall(r'\d+?:\d+|\d+', columns[2].getText())
            days = re.findall(r'lu|ma|mi|ju|vi|sá', columns[1].getText())
            hours = Hours(days = days, start = start, end = end)
            schedule.append(hours)

    return (professors, schedule)


def subject_data(subject_url: str) -> tuple:
    '''Gets all the classes for a given subject url
    Parameters
        subject_url (str): The url of the subject that will be scraped

    Returns
        tuple: contains the information of the subject with the classes
            which has the following structure:
            (id name semester plan classes)
    '''
    
    soup = get_soup(subject_url)
    
    # It's to avoid the parenthesis: Actuaría (plan 2015)
    major = soup.find('h1').getText().split(' (')[0]
    
    # http://www.fciencias.unam.mx/docencia/horarios/SEMESTER/PLAN/SUBJECTID
    semester, plan, id_subject = re.findall(r'\d+', subject_url)

    # This returns something like this: 'Álgebra Superior I, Primer Semestre'
    subject_info = soup.find(text = re.compile(r'\bSemestre\b'))
    name, _ = subject_info.split(', ')
    
    # All the info are inside tables
    content = soup.find(id = 'info-contenido')
    tables = content.find_all('table')
    classes = []
    for table in tables:
        div = table.previous_sibling
        data = re.findall(r'\d+', div.getText())
        group, enrolled, quota = data
        professors, schedule = class_table_data(table)
        class_data = ClassData(group = group, cast = professors
                , enrolled = enrolled
                , quota = quota
                , schedule = schedule)
        classes.append(class_data)

    subject = {
                'id': id_subject,
                'semester': semester,
                'classes': classes,
                'plan': plan,
                'name': name
            }
    return Subject(**subject) 


