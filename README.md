# Job Market Analysis

## Overview
This project scrapes job listings from a job portal and analyzes the data to extract insights on hiring trends, experience requirements, popular technologies, and location distribution. The project is divided into two main phases: data scraping and data analysis.

## Features
1. **Data Collection**:
- Scrapes Python-related job vacancies using Scrapy and Selenium.
- Extracts job attributes such as titles, companies, experience requirements, locations, and technologies.
- Stores the scraped data in a CSV file for further analysis.

2. **Data Analysis**:
- Analyzes the collected data using **pandas**.
- Visualizes insights such as:
- [x] Top hiring companies
- [x] Experience requirements distribution
- [x] Popular technologies
- [x] Location distribution of vacancies

## Project Structure
### Scrapy Spider:
- `dou_vacancies`: A custom Scrapy spider using Selenium for dynamic content loading.
Extracts data on job listings and handles pagination.
- 
### Data Pipeline:
- Data Pipeline: Stores the scraped data and exports it to CSV format.

### Analysis:
- A script to analyze the data using pandas and visualize trends with matplotlib.

## Setup Instructions
0. **Prerequisites**:
   - Python 3.7+
   - Dependencies listed in requirements.txt (Scrapy, Selenium, pandas, matplotlib)


1. **Installation**:
    ```shell
    git clone https://github.com/Bogdan-Rylov/job-market-analysis.git
    cd job-market-analysis
    python -m venv venv
    pip install -r requirements.txt
    ```

2. **Running the Scraper**:
    ```shell
    scrapy crawl dou_vacancies
    ```
    This command starts the scraper to collect job vacancy data and stores it in a CSV file.


3. **Running the Analysis**:
After scraping, run the analysis script `dou_vacancies.ipynb` to generate visualizations
