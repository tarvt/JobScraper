import requests
from bs4 import BeautifulSoup

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
                #location = job.find('span', class_='c-jobListView__metaItem', string=lambda x: 'تهران' in x or 'اصفهان' in x).get_text(strip=True)
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
                for job in jobs:
                    print(f"Title: {job['title']}")
                    print(f"Company: {job['company']}")
                    #print(f"Location: {job['location']}")
                    print(f"Link: {job['link']}")
                    print(f"Posted: {job['date_posted']}")
                    print('-' * 40)
        else:
            return None  # Handle errors appropriately


class jobvisionSearcher(JobSearcher):

    def search_jobs(self, keywords, locations=None, categories=None):
        # Implement the API call and response handling specific to this job board
        pass