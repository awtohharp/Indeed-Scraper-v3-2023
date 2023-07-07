# -*- coding: utf-8 -*-
"""
Originally created on Mon Mar 20 20:27:50 2023 by @author: RDxR10
"""

import time
import datetime
from selenium import webdriver
import csv
import re
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

query = input("Enter job query: ")
location = input("Enter job location: ")
radius = input("Specify a range to search in miles (enter 0 for exact location): ")
remote = input("Search only remote jobs? ['y' = yes, other responses = no] ")
if remote.lower() == 'y':
    remote = '&sc=0kf%3Aattr(DSQF7)%3B'
else:
    remote = ''
age = input("Return only results in the last X days [blank/noninteger = 90 days]")
if not isinstance(age, int):
    age = 90
num_pages = int(input("Number of pages to scrape: "))
start_list = [page * 10 for page in range(num_pages)]
base_url = 'https://www.indeed.com'
#base_url = "https://www.indeed.com'

driver = webdriver.Chrome()
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

for start in start_list:
    url = base_url + f'/jobs?q={query}&l={location}{remote}&radius={radius}&start={start}&fromage={age}'
    print(f'Scraping from root URL {url}')
    driver.execute_script(f"window.open('{url}', 'tab{start}');")
    time.sleep(1)

with open(f'{query}_{location}_jobs_{timestamp}.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Job Title', 'Company', 'Location', 'Job Link', 'Salary'])
    for start in start_list:
        driver.switch_to.window(f'tab{start}')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('td', {'class': 'resultContent'})

        for job in items:
            s_link = job.find('a').get('href')
            job_title = job.find('span', title=True).text.strip()
            company = job.find('span', class_='companyName').text.strip()
            location = job.find('div', class_='companyLocation').text.strip()

            if job.find('div', class_='metadata salary-snippet-container'):
                salary_text = job.find('div', class_='metadata salary-snippet-container').text
            elif job.find('div', class_='metadata estimated-salary-container'):
                salary_text = job.find('div', class_='metadata estimated-salary-container').text
            else:
                salary_text = ""

            # Remove commas from salary_text
            salary_text = salary_text.replace(',', '')

            # Transform K to thousand
            if 'K' in salary_text:
                salary_text = salary_text.replace('K', '000')

            # Extract numerical values from the salary text
            salary_values = re.findall(r'\d+(?:\.\d+)?', salary_text)

            if salary_values:
                # Handle "Up to" case
                if 'Up to' in salary_text:
                    salary_max = float(salary_values[0])
                    salary_min = 'N/A'
                # Handle "From" case
                elif salary_text.startswith('From'):
                    salary_min = float(salary_values[0])
                    salary_max = 'N/A'
                else:
                    salary_min = float(salary_values[0])
                    salary_max = float(salary_values[1]) if len(salary_values) > 1 else salary_min

                # Determine the salary type
                if 'month' in salary_text:
                    salary_type = 'MONTHLY'
                elif 'hour' in salary_text:
                    salary_type = 'HOURLY'
                elif 'annual' in salary_text or 'year' in salary_text:
                    salary_type = 'YEARLY'
                else:
                    salary_type = ''
            else:
                salary_min = 'N/A'
                salary_max = 'N/A'
                salary_type = ''

            """
            if job.find('div', class_='metadata salary-snippet-container'):
                salary = job.find('div', class_='metadata salary-snippet-container').text
            elif job.find('div', class_='metadata estimated-salary-container'):
                salary = job.find('div', class_='metadata estimated-salary-container').text
            else:
                salary = ""
            """
            rating_element = job.find('span', class_='ratingNumber')
            if rating_element:
                rating = rating_element.span.text.strip()
            else:
                rating = 'N/A'  # Set a default value if rating is not found


            job_link = base_url + s_link

            writer.writerow([job_title, company, location, job_link, rating, salary_min, salary_max, salary_type])

        driver.close()


driver.quit()
