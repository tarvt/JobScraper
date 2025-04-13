import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
class JobSearcher:
    def __init__(self, base_url):
        self.base_url = base_url

    def search_jobs(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")


class JobinjaSearcher(JobSearcher):
    def search_jobs(self, keywords, locations=None, categories=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        params = {
            'filters[keywords][0]': keywords,
            'filters[job_categories][]': categories if categories else '',
            'filters[locations][]': locations if locations else '',
            'preferred_before': '1744182688',  # Example timestamp
            'sort_by': 'relevance_desc'
        }
        response = requests.get(self.base_url, params=params, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            job_items = soup.find_all('li', class_='o-listView__item')
            jobs = []
            for job in job_items:
                title = job.find('h2', class_='o-listView__itemTitle').get_text(strip=True)
                company = job.find('span', string=lambda x: '|' in x).get_text(strip=True)
                link = job.find('a', class_='c-jobListView__titleLink')['href']
                date_posted = job.find('span', class_='c-jobListView__passedDays').get_text(strip=True)
                jobs.append({
                    'title': title,
                    'company': company,
                    #'location': location,
                    'link': link,
                    'date_posted': date_posted,
                })
                # Printing the extracted job listings
            return jobs
        else:
            return None  # Handle errors appropriately


class JobVisionSearcher:

    BASE_URL = "https://jobvision.ir/jobs"

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless Chrome
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


    def search_jobs(self, search_field, job_type="remote", page=1, sort=1):
        url = f"{self.BASE_URL}/keyword/{search_field}/type/{job_type}?page={page}&sort={sort}"
        self.driver.get(url)


        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-list.row.rounded.no-border-radius-left job-card-list job-card"))
            )

        except Exception as e:
            print("An unexpected error occurred:", e)

        html = self.driver.page_source
        return self.parse_job_results(html)



    def parse_job_results(self, html):
        soup = BeautifulSoup(html, "html.parser")
        job_cards = soup.select("div.jobs-list.row.rounded.no-border-radius-left job-card-list job-card")
        jobs = []

        for job in job_cards:
            print(job)
            job_title = soup.select_one('.job-card-title').get_text(strip=True)
            company_name_element = soup.select_one('.company-brand + a')
            company_name = company_name_element.get_text(strip=True) if company_name_element else 'N/A'
            job_link = soup.select_one('a[aria-label][href]')['href']
            jobs.append({
                    'title': job_title,
                    'company': company_name,
                    #'location': location,
                    'link': job_link,
                    #'date_posted': date_posted,
                })


        return jobs 


    def close(self):

        self.driver.quit()