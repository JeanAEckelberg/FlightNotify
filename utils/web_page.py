"""
Web page utilities file
"""

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from time import sleep


def get_flight_page(url: str) -> str:
    """
    Get the page as a string of HTML code
    :param url: url to visit
    :return: html as string
    """
    options = FirefoxOptions()
    options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        sleep(5)
        html = driver.page_source
    return html


def get_time_of_flight_arrival(url: str) -> str:
    """
    Parse html for the flight arrival time
    :param url: url of the flight page
    :return: flight arrival time
    """
    html = get_flight_page(url)
    doc: BeautifulSoup = BeautifulSoup(html, "html.parser")
    destination_info: Tag = doc.find(class_="destination-summary")
    arrival_time: str = destination_info.find(class_="time-container estimated-time ac-font-bold").text
    arrival_time = arrival_time.strip()
    return arrival_time
