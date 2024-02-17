"""
This file contains the configuration for the app
"""


from dataclasses import dataclass


@dataclass
class Config:
    """
    A dataclass representing the configuration of the app
    """
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    URL: str
