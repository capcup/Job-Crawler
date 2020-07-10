import requests
from app import Jobs as Jobs
from bs4 import BeautifulSoup

class JobCrawler: 

    jobs = {}
    file = ''
    url = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%5D&companyID=0&cityID=0&sourceOfTheSearchField=resultlistpage%3Ageneral&searchOrigin=Resultlist_top-search&ke=Junior-Softwareentwickler%2Fin&ws=Weinheim&ra=30'
    url2 = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=%5B%5D&ke=Junior-Softwareentwickler%2Fin&ws=Frankfurt&ra=30&suid=7e813f1f-841f-4390-aad1-b40ad8cd5bb4&of=25&action=paging_next'
    url3 = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=%5B%5D&ke=Junior-Softwareentwickler%2Fin&ws=Frankfurt&ra=30&suid=7e813f1f-841f-4390-aad1-b40ad8cd5bb4&of=50&action=paging_next'
    url4 = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=%5B%5D&ke=Junior-Softwareentwickler%2Fin&ws=Frankfurt&ra=30&suid=7e813f1f-841f-4390-aad1-b40ad8cd5bb4&of=75&action=paging_next'

    def __init__(self):
        pass 

    def crawl_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept-Language': 'de-DE,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
            
        try:
            source_code = requests.get(self.url, headers=headers).text
            soup = BeautifulSoup(source_code, 'lxml')
        except:
            print('URL error')        

        title = soup.findAll('h2', {"class": 'TitleWrapper-sc-7z1cau-1 cEDrrn'})

        for i in title:
            # print(i.text.strip())
            print(i.text)

    def write_file(self):
        # add date to filename
        pass 



'''
def addJobs():
    title = 'Junior Softwareentwickler'
    new_jobs = Jobs(title=title)
    try:
        db.session.add(new_jobs)
        db.session.commit()
        return redirect('/')
    except: 
        return 'There was an issue adding a job'

'''

if __name__ == "__main__":
    jc = JobCrawler()
    jc.crawl_data()


'''

'''

''' TITLE
class="TitleWrapper-sc-7z1cau-1 cEDrrn",
class="TitleWrapper-sc-7z1cau-1 cEDrrn"

'''