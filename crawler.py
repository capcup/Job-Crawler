
class JobCrawler: 

    jobs = {}
    file = ''
    url = ''

    def __init__(self):
        pass 

    def crawl_data(self):
        # switch case for searched site OR all at once in different files
        pass
    
    def write_file(self):
        # add date to filename
        pass 
    


'''
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
        price = self.get_price(soup)
        name = self.get_name(soup)
        time = self.get_time()
'''