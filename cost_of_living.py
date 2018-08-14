from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
from selenium.common.exceptions import NoSuchElementException
from typing import List, Tuple, Dict, Any, Generator, Iterable


#____________________________
# Scrape Salaries
#____________________________

# Declare cities
cities = ['Palo-Alto', 'San-Jose', 'Portland', 'Austin', 'Denver', 'San-Diego', 'Washington', 'Boston', 
                 'San-Francisco', 'Seattle', 'Atlanta', 'Los-Angeles', 'Chicago', 'New-York', 'Mountain-View',
                 'Santa-Monica', 'Cambridge', 'Salt-Lake-City', 'Raleigh', 'Nashville', 'Sunnyvale', 'Boulder',
                 'Irvine', 'Philadelphia', 'Dallas', 'Santa-Clara', 'Menlo-Park', 'Bellevue', 
                 'Charlotte', 'Cupertino', 'Plano', 'Richmond']


def browse_to_city(browser, city):
    """ Use browser to get numbeo.com cost-of-living data for each city."""
    url = 'https://www.numbeo.com/cost-of-living/in/' + city
    browser.get(url)

def get_table_rows(browser, table_selector):
    """ Use css tag 'td' to find all rows in the table."""
    rows = browser.find_elements_by_css_selector(table_selector + ' tr')
    return rows

def parse_table_rows(rows, city):
    """ If 'th' is found, add the heading to category. Otherwise, pass back
    the rows for each category and city."""
    category = None
    for row in rows:
        headings = row.find_elements_by_css_selector('th')
        if headings:
            category = headings[0].text
            continue
        yield parse_row(row, category=category, city=city)

def parse_row(row, category, city):
    """ Return a dictionary to be used later as a pandas DF."""
    return {'category': category,
            'city': city,
            'item': get_item(row),
            'price': get_price(row)}

def get_item(row):
    """ Get items, denoted by css 'td' class."""
    tds = row.find_elements_by_css_selector('td')
    if tds:
        return tds[0].text

def get_price(row):
    """ Get price, denoted by css 'td.priceValue' class."""
    tds = row.find_elements_by_css_selector('td.priceValue')
    if tds:
        return tds[0].text.strip(' $£')

def scrape_city(city):
    """ Start a browser, go to a certain city page, and scrape all categories,
    rows, and prices. Return information as a dictionary."""
    browser = Chrome()
    browse_to_city(browser, city)
    rows = get_table_rows(browser, '.data_wide_table')
    yield from parse_table_rows(rows, city)
    browser.quit()

def scrape_cities(cities):
    """ Return a dictionary of cost-of-living data for a given list
    of cities."""
    for city in cities:
        yield from scrape_city(city)

# Get a list of dictionaries for each city of interest
#city_data = list(scrape_cities(cities))

#____________________________
# Scrape Salaries
#____________________________

def get_city_urls(): 
    """ Return a list of urls for each city in payscale's database."""   
    browser = Chrome()
    url = 'https://www.payscale.com/research/US/Job=Data_Scientist%2c_IT/City'
    browser.get(url)
    links = browser.find_elements_by_css_selector('a')
    link = links[0]
    all_urls = [link.get_attribute('href') for link in links]
    valid_urls = [url for url in all_urls if url and 'http' in url]
    city_urls = [url for url in valid_urls if 'research/US/Job=Data_Scientist%2c_IT/Salary/' in url]
    browser.quit()
    return city_urls

# Get all city urls
#city_urls = [url for url in get_city_urls() 
#             if any(city in url for city in cities)]

# Note -- this may be an old function and no longer needed.
def browse_to_salary(browser, city):
    """ Write function to get the salary page for each city."""
    url = 'https://www.payscale.com/research/US/Job=Data_Scientist%2c_IT/Salary/06f59d2a/' + city
    browser.get(url)

def parse_salary_range(salary_range: str) -> Tuple[int, int]:
    """ Parse and return salary into a tuple of min, max salaries."""
    min_salary, max_salary = [salary.strip().strip('$').strip('£') for salary in salary_range.split('-')]
    return min_salary, max_salary


def get_salaries(city_urls: List[str]) -> Iterable[Dict[str, Any]]:
    """ Write function to start browser, and scrape salary data for each city. """
    browser = Chrome()
    sel_title = 'td.bar-chart-bootstrap-range-label'
    for url in city_urls:
        browser.get(url)
        salary_range = browser.find_element_by_css_selector(sel_title).text
        min_salary, max_salary = parse_salary_range(salary_range)
        result = {'city': city,
                  'min_salary': min_salary,
                  'max_salary': max_salary}
        yield result
    browser.quit()

def get_all_salaries(city_urls, cities: List[str]) -> Iterable[Dict[str, Any]]:
    """ Return a dict of city, avg_salary, and, if available, min/max salaries per city."""
    browser = Chrome()
    for url, city in zip(city_urls, cities):
        print(url)
        browser.get(url)
        try:
            sel_title = 'td.bar-chart-bootstrap-range-label'
            sel_title2 = 'div.pay-spotlight__pay-value'
            avg_salary = browser.find_element_by_css_selector(sel_title2).text.strip().strip('$').replace(',','')
            salary_range = browser.find_element_by_css_selector(sel_title).text
            min_salary, max_salary = parse_salary_range(salary_range)
            result = {'city': city,
                      'avg_salary': avg_salary,
                      'min_salary': min_salary,
                      'max_salary': max_salary}
            yield result
        except NoSuchElementException:
            sel_title = 'div.pay-spotlight__pay-value'
            avg_salary = browser.find_element_by_css_selector(sel_title).text.strip().strip('$')
            result = {'city': city,
                      'avg_salary': avg_salary}
            yield result

def get_avg_salaries(city_urls, cities: List[str]) -> Iterable[Dict[str, Any]]:
    """ Return a dict of average salaries. This, also, may be a relic of past work and may need to be deleted."""
    browser = Chrome()
    sel_title = 'div.pay-spotlight__pay-value'
    for url, city in zip(city_urls, cities):
        browser.get(url)
        avg_salary = browser.find_element_by_css_selector(sel_title).text.strip().strip('$')
        result = {'city': city,
                  'avg_salary': avg_salary}
        yield result
    browser.quit()
