"""
This file contains the state of the app
"""

from dataclasses import dataclass


@dataclass
class State:
    """
    A dataclass representing the state of the app
    """
    FLIGHT_ARRIVAL_TIME: str
