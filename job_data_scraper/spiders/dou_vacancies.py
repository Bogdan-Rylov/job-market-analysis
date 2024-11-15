import logging
import re
from typing import Any

import dateparser
import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import job_data_scraper.config as config


logging.basicConfig(level=logging.INFO)

TECHNOLOGIES = config.POPULAR_TECHNOLOGIES


class DouVacanciesSpider(scrapy.Spider):
    name = "dou_vacancies"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?category=Python"]

    def parse(self, response: Response, **kwargs) -> Any:
        experience_filters = [
            {"filter": "exp=0-1", "label": "<1"},
            {"filter": "exp=1-3", "label": "1-3"},
            {"filter": "exp=3-5", "label": "3-5"},
            {"filter": "exp=5plus", "label": "5+"},
        ]

        for experience_filter in experience_filters:
            experience_url = f"{response.url}&{experience_filter["filter"]}"
            job_vacancies_urls = self.get_job_vacancies_urls(experience_url)

            for url in job_vacancies_urls:
                yield scrapy.Request(
                    url,
                    callback=self.parse_job_vacancy,
                    meta={"experience": experience_filter["label"]}
                )

    @staticmethod
    def get_job_vacancies_urls(page_url: str) -> list[str]:
        logging.info(f"Getting vacancies urls from '{page_url}'...")

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(page_url)

            try:
                while True:
                    more_button = WebDriverWait(driver, 5).until(
                        ec.presence_of_element_located(
                            (By.CSS_SELECTOR, ".more-btn a"))
                    )

                    if not more_button or not more_button.is_displayed():
                        break

                    WebDriverWait(driver, 10).until(
                        ec.element_to_be_clickable(more_button)
                    )
                    more_button.click()
            except Exception as e:
                logging.error(
                    f"Couldn't click the 'more' button due to an error: {e}"
                )

            vacancy_elements = driver.find_elements(
                By.CSS_SELECTOR, ".title a.vt"
            )

            return [
                element.get_attribute("href")
                for element in vacancy_elements
            ]

    @staticmethod
    def parse_salary(salary_str: str | None) -> str | None:
        if not salary_str:
            return None

        salary_str = salary_str.replace(" ", "").lower()

        range_match = re.match(r"\$(\d+)[–-](\d+)", salary_str)
        if range_match:
            min_salary = float(range_match.group(1))
            max_salary = float(range_match.group(2))
            return f"{min_salary}-{max_salary}"

        from_match = re.match(r"від\$(\d+)", salary_str)
        if from_match:
            min_salary = float(from_match.group(1))
            return f">{min_salary}"

        to_match = re.match(r"до\$(\d+)", salary_str)
        if to_match:
            max_salary = float(to_match.group(1))
            return f"<{max_salary}"

        return None

    @staticmethod
    def get_technologies_from_description(description: str) -> list[str]:
        description = description.lower()
        found_technologies = []

        for tech in TECHNOLOGIES:
            if re.search(r"\b" + re.escape(tech) + r"\b", description):
                found_technologies.append(tech)

        return sorted(found_technologies)

    def parse_job_vacancy(self, response: Response) -> dict:
        title = response.css(".l-vacancy h1::text").get()
        company = (
            response.css(".b-compinfo .l-n a:first-child::text").get()
        )
        posted_date = dateparser.parse(
            response.css(".l-vacancy .date::text").get()
        )
        employment_type = None
        required_experience = response.meta["experience"]
        salary_range = self.parse_salary(response.css(".salary::text").get())
        locations = ",".join(
            re.split(
                r"\s*,\s*",
                response.css(".place::text").get().strip()
            )
        )
        technologies = ",".join(
            self.get_technologies_from_description(
                " ".join(response.css(".vacancy-section ::text").getall())
            )
        )
        url = response.url

        return {
            "title": title,
            "company": company,
            "posted_date": posted_date,
            "employment_type": employment_type,
            "required_experience": required_experience,
            "salary_range": salary_range,
            "locations": locations,
            "technologies": technologies,
            "url": url
        }
