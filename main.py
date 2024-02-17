"""
A simple app to track a friend's flight
"""
from datetime import datetime

import schedule
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup, Tag
import smtplib
from dotenv import dotenv_values
from email.message import EmailMessage
from dataclasses import dataclass
from time import sleep


@dataclass
class Config:
    """
    A dataclass representing the configuration of the app
    """
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    URL: str


@dataclass
class State:
    """
    A dataclass representing the state of the app
    """
    FLIGHT_ARRIVAL_TIME: str


def load_config() -> Config:
    """
    Load configuration from .env file structured:
    EMAIL_ADDRESS: <EMAIL ADDRESS>
    EMAIL_PASSWORD: <PASSWORD>
    URL: <URL OF FLIGHT INFO>
    :return: Config instance
    """
    return Config(**dotenv_values(".env"))


def get_flight_page(url: str) -> str:
    """
    Get the page as a string of HTML code
    :param url:
    :return:
    """
    options = FirefoxOptions()
    options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        sleep(5)
        html = driver.page_source
    return html


def generate_email(email_text: str, email_address: str) -> EmailMessage:
    """
    Create an email
    :param email_text: content of the email
    :param email_address: address to send and receive the notification
    :return: Email message
    """
    msg: EmailMessage = EmailMessage()
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = 'Flight Notify'
    msg.set_content(email_text)
    return msg


def send_email(email_text: str, email_address: str, email_password: str) -> None:
    """
    Send an email via gmail smtp
    :param email_text: content of the email
    :param email_address: address to send and receive the notification
    :param email_password: app password to log in
    :return: None
    """
    msg: EmailMessage = generate_email(email_text, email_address)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(email_address, email_password)
        smtp_server.sendmail(email_address, email_address, msg.as_string())
    print("Message sent!")


def get_time_of_flight_arrival(html: str) -> str:
    """
    Parse html for the flight arrival time
    :param html: html of the flight page
    :return: flight arrival time
    """
    doc: BeautifulSoup = BeautifulSoup(html, "html.parser")
    destination_info: Tag = doc.find(class_="destination-summary")
    arrival_time: str = destination_info.find(class_="time-container estimated-time ac-font-bold").text
    arrival_time = arrival_time.strip()
    return arrival_time


def main_loop_job(state: State, config: Config):
    """
    Main loop of the application
    :param state:
    :param config:
    :return:
    """
    html: str = get_flight_page(config.URL)
    arrive_time: str = get_time_of_flight_arrival(html)
    if state.FLIGHT_ARRIVAL_TIME != arrive_time:
        state.FLIGHT_ARRIVAL_TIME = arrive_time
        send_email(f"Flight arrival time: {arrive_time}", config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)


if __name__ == "__main__":
    state: State = State("")
    config: Config = load_config()
    with_args = lambda: main_loop_job(state, config)

    schedule.every(1).minutes.until(datetime.fromisoformat("20240217T17")).do(with_args)
    while 1:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            sleep(n)
        schedule.run_pending()

