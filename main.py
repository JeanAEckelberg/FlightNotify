"""
A simple app to track a friend's flight
"""
from datetime import datetime
import schedule
from dotenv import dotenv_values
from time import sleep

from utils.email import send_email
from utils.web_page import get_time_of_flight_arrival
from models.config import Config
from models.state import State


def load_config() -> Config:
    """
    Load configuration from .env file structured:
    EMAIL_ADDRESS: <EMAIL ADDRESS>
    EMAIL_PASSWORD: <PASSWORD>
    URL: <URL OF FLIGHT INFO>
    :return: Config instance
    """
    return Config(**dotenv_values(".env"))


def main_loop_job(state: State, config: Config) -> None:
    """
    Main loop of the application
    :param state: the state of the application
    :param config: the configuration of the application
    :return: None
    """
    arrive_time: str = get_time_of_flight_arrival(config.URL)
    if state.FLIGHT_ARRIVAL_TIME != arrive_time:
        state.FLIGHT_ARRIVAL_TIME = arrive_time
        send_email(f"Flight arrival time: {arrive_time}", config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)


if __name__ == "__main__":
    state: State = State("")
    config: Config = load_config()
    with_args = lambda: main_loop_job(state, config)
    schedule.every(10).minutes.until(datetime.fromisoformat("20240217T17")).do(with_args)

    while 1:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            sleep(n)
        schedule.run_pending()
