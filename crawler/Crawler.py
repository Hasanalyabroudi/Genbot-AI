from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from dotenv import load_dotenv

executor = ThreadPoolExecutor(max_workers=10)

load_dotenv()



class Crawler:
    def __init__(self,urls=[] ):
        self.urls = urls
        self.visited = []
        self.to_visit = []
        self.IDxURL = pd.DataFrame(columns=['URL','ID'])
        
    def check_url(self,url: str) -> BeautifulSoup:
        """

        :param url: URL to check
        :return: BeautifulSoup object if the URL is valid, None otherwise

        Check if the URL is valid and return a BeautifulSoup object if it is
        
        
        """

        if url not in self.visited:
            try:
                response = requests.get(url,timeout=5)
                print(f" {url} -> Status code: ",response.status_code)
            except requests.exceptions.RequestException as e:
                print("Error: ",e)
                return None, False
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if 'application/pdf' in content_type:
                    ## read the pdf
                    print("PDF found")
                    pdf_content = response.get_text()
                    return pdf_content,True
                    
                    # executor.submit(save_pdf_to_dbs,url,response)
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                return soup,False
            else:
                print("Error: ",response.status_code)
                return None,False
            
        else:
            print("URL already visited")

        return None,False
    
    def get_domaine_name(self, url):
        domaine = re.search(r"(https?://)?((?:[a-zA-Z0-9-]+\.)+[a-z]{2,})", url)
        if domaine:
            return domaine.group(2)
        print("Domaine not found")
        return None



    
    def check_url_syntax(self,url):
        if re.match(r'^https?://(www\.)?w?[a-v|x-z][\w%\+-\.]+\.(org|ca|com|net)',url):
            return True
        # print("Invalid URL")
        return False
    
    
    def get_internal_links(self,url):
        print("Visiting: ",url)
        print("Checking URL ...")
        soup,PDF = self.check_url(url)  
        if PDF:
            return [],soup
          
        self.add_to_visited(url)
        
        internal_links = []

        if soup:
            for link in soup.find_all('a'):
                internal_url = link.get('href')
                if internal_url is None or internal_url == '' or internal_url[0] == '#':
                    continue
                if self.original_domaine in internal_url and self.check_url_syntax(internal_url):
                    self.add_url(internal_url)
                    internal_links.append(internal_url)

                elif  not self.check_url_syntax(internal_url) : # internal_url[0] == '/':
                    internal_url = requests.compat.urljoin(url, internal_url)
                    self.add_url(internal_url)
                    internal_links.append(internal_url)

        print("Finished visiting: ",url)
        return internal_links,soup
    
            

    def add_url(self,url):
        self.urls.append(url)
        if url not in self.visited and url not in self.to_visit:
            self.to_visit.append(url)

    def add_urls(self,urls): ## list of urls
        for url in urls:
            self.urls.append(url)
            if url not in self.visited and url not in self.to_visit:
                self.to_visit.append(url)

        

    def add_to_visited(self,url):
        
        self.visited.append(url)
        # self.to_visit.remove(url)
    
    def get_visited(self):
        return self.visited

    def get_urls(self):
        return self.urls
    
    def get_to_visit(self):
        return self.to_visit
    
    def set_to_visit(self,urls):
        self.to_visit = urls

    def get_all_links(self):
        return list(set(self.visited + self.to_visit))

    def set_starting_url(self,url):
        self.add_url(url)
        self.original_domaine = self.get_domaine_name(url)



# Crawler = Crawler()
# Crawler.set_starting_url("https://www.uottawa.ca")
# Crawler.run()

