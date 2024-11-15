# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import date
from typing import Optional

import scrapy
from attr import dataclass


@dataclass
class JobVacancy:
    title: str
    company: str
    posted_date: date
    employment_type: str
    required_experience: Optional[tuple[int, Optional[int]]]
    salary_range: Optional[tuple[Optional[float], Optional[float]]]
    location: list[str]
    technologies: list[str]
    url: str
