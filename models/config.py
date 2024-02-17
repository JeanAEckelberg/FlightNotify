"""
This file contains the configuration for the app
"""


from dataclasses import dataclass, field

from utils.path_factory import make_path


@dataclass
class Config:
    """
    A dataclass representing the configuration of the app
    """
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    URL: str
    PATH: [str] = field(default_factory=make_path)
