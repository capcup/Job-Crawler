import requests
from app import Jobs, db 
from bs4 import BeautifulSoup
from configparser import ConfigParser

class Job_Crawler: 

    platform = 'stepstone'

    url = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%5D&companyID=0&cityID=0&sourceOfTheSearchField=homepagemex%3Ageneral&searchOrigin=Homepage_top-search&ke=Junior-Softwareentwickler%2Fin&ws=Weinheim&ra=30&rsearch=1'
    url3 = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=%5B%5D&ke=Junior-Softwareentwickler%2Fin&ws=Frankfurt&ra=30&suid=7e813f1f-841f-4390-aad1-b40ad8cd5bb4&of=50&action=paging_next'
    url4 = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=%5B%5D&ke=Junior-Softwareentwickler%2Fin&ws=Frankfurt&ra=30&suid=7e813f1f-841f-4390-aad1-b40ad8cd5bb4&of=75&action=paging_next'

    def __init__(self):
        self.config_object = ConfigParser()
        self.config_object.read("config.ini")

        self.title_class = ''
        self.company_class = ''
        self.link_class = ''

        '''
        - dynamische Deklaration und Initialisierung der platform-variablen 
        - 
        '''        


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

        
        title = soup.findAll('h2', {"class": self.stepstone_title_h2_class})        
        companies = soup.findAll('div', {"class": self.stepstone_company_div_class})
        job_link = soup.findAll('a', {'class': self.stepstone_link_a_class})

        job_informations = zip(title, companies, job_link)
        self.add_Jobs(job_informations)


    def add_Jobs(self, job_informations):
        job_informations = list(job_informations)
        
        for title in job_informations:
            title, company, url = title

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
            
    def extract_platform_informations(self):
        pass 
        # strip by '_'
        # e.g. title_tag & title_class

    def delete_alljobs(self):
        db.session.query(Jobs).delete()
        db.session.commit()


if __name__ == "__main__":

    # To-Do: embed config.ini - extract_platform_informations
    job_crawler = Job_Crawler()
    #job_crawler.config_object.read("config.ini")
    print(job_crawler.config_object["stepstone"]["title_h2_class"])

    title, company, link = job_crawler.config_object["stepstone"]
    # printing out the keys
    print(title, company, link)

    '''
    job_crawler.delete_alljobs()
    job_crawler.crawl_data()
    '''