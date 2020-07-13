import requests
from app import Jobs, db 
from bs4 import BeautifulSoup
from configparser import ConfigParser

class Job_Crawler: 

    url = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=homepagemex%3Ageneral&rsearch=1&qs=%5B%5D&ke=Junior-Softwareentwickler%2Fin&ws=Weinheim&ra=30&suid=70c82d15-19d7-419a-a3a5-1181c5825d19&of=0&action=paging_prev'


    def __init__(self):
        self.config_object = ConfigParser()
        self.config_object.read("config.ini")
        self.extract_platform()
        self.set_platform_informations()


    def crawl_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept-Language': 'de-DE,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
        try:
            source_code = requests.get(self.url, headers=headers).text
            soup = BeautifulSoup(source_code, 'lxml')
        except:
            print('URL error')        
        
        title = soup.findAll(self.title_tag, {"class": self.title_class})        
        companies = soup.findAll(self.company_tag, {"class": self.company_class})
        job_link = soup.findAll(self.link_tag, {'class': self.link_class})

        job_informations = zip(title, companies, job_link)
        self.add_Jobs(job_informations)


    def add_Jobs(self, job_informations):
        job_informations = list(job_informations)
        
        for title in job_informations:
            title, company, url = title

            if not self.filter_job(title.text):
                continue
            title = title.text
            company = company.text
            if self.platform == 'stepstone':
                url = 'https://www.stepstone.de/' + url.get('href')
            
            new_job = Jobs(title=title, company=company, url=url)
            try:
                db.session.add(new_job)
            except:
                return 'Issue by adding new jobs to the database after crawling'
        try:
            db.session.commit()
        except:
            return 'Issue by commiting the new Jobs in the database'
            
    def extract_platform(self):
        self.platforms = [x.strip() for x in self.config_object['platforms']['platforms'].split(',')]

        for platform in self.platforms:
            if platform in self.url:
                self.platform = platform
        # e.g. title_tag & title_class

    def set_platform_informations(self):
        title, company, link = self.config_object[self.platform]

        self.title_tag = title.split('_')[1]
        self.company_tag = company.split('_')[1]
        self.link_tag = link.split('_')[1]

        self.title_class = self.config_object[self.platform][title]
        self.company_class = self.config_object[self.platform][company]
        self.link_class =  self.config_object[self.platform][link]
 
        self.keywords = [x.strip().lower() for x in self.config_object['platforms']['keywords'].split(',')]

    def filter_job(self, title: str):
        for keyword in self.keywords:
            if keyword in title.lower():
                return True
        return False

    def delete_alljobs(self):
        db.session.query(Jobs).delete()
        db.session.commit()


if __name__ == "__main__":

    job_crawler = Job_Crawler()

   
    # job_crawler.delete_alljobs()
    job_crawler.crawl_data()
    