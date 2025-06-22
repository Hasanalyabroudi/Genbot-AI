import io
import re
from urllib.parse import urlparse 
import PyPDF2
from bs4 import BeautifulSoup
import markdown
import markdownify 
import requests
import requests.compat

class url:
    def __init__(self,url):
        self.url = url
        if not check_url_syntax(self.url):
            print("Invalid URL")
            self.url = None
            self.domain = None
            self.content = None
            self.internal_links = []
            self.page_type = None
            
        else:
            self.url = url
            self.domain = get_domain_name(self.url)
            self.content = self.get_content()
            self.markdown = self.get_markdown()
            self.text = self.get_text()
            self.internal_links = self.get_internal_links()




    
    
    
    def get_content(self):
        
        try:
            response = requests.get(self.url,timeout=5)
            print(f" {self.url} -> Status code: ",response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error: ",e)
            self.page_type = None
            return None
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            if 'application/pdf' in content_type:
                ## read the pdf
                file = io.BytesIO(response.content)  
                pdf = PyPDF2.PdfReader(file)  
        
                content = ""  
                for page in range(len(pdf.pages)):  
                    content += pdf.pages[page].extract_text()  
                self.page_type = 'PDF'
                return content
                
            else:
                ## read the html
                self.raw_html = response.text
                soup = BeautifulSoup(response.text, 'html.parser')
                self.page_type = 'HTML'
                 # Extract the body
                body = soup

                for each in ['header', 'footer', 'nav', 'aside', 'script', 'style', 'noscript', 'iframe', 'form', 'input', 'button']:
                    s = body.find(each)
                    if s:
                        s.extract()
                        
                return body
        else:
            print("Error: ",response.status_code)
            self.page_type = None
            return None
        
    def get_markdown(self):
        if self.page_type == 'HTML' and self.raw_html:
            markdown = markdownify.markdownify(self.raw_html)
            return markdown
        return None
    
    def get_text(self):
        if self.page_type == 'HTML':
            return md_to_text(self.markdown)
        elif self.page_type == 'PDF':
            return self.content
        return None
        

    
    def get_internal_links(self):
        if self.page_type == 'HTML':
            internal_links = []
            for link in self.content.find_all('a'):

                link_url = link.get('href')
                
                if is_partial_url(link_url):
                    # print(f"Partial URL: {link_url}")
                    link_url = requests.compat.urljoin(self.url,link_url)
                    link_domain = get_domain_name(link_url)
                
                else:
                    link_domain = get_domain_name(link_url)

                if link_domain is None:
                    continue 
                    
                if link_domain == self.domain or self.domain in link_domain:
                    internal_links.append(link_url)
                
            return internal_links
        return []
    

## Helper functions

def is_partial_url(url):
    if url is None:
        return False
    if url.startswith('/'):
        return True
    return False

def check_url_syntax(url):
    if re.match(r'^https?://(www\.)?w?[a-vx-z][\w%\+-\.]+\.[a-zA-Z]{2,}', url):
        return True
    # print("Invalid URL")
    return False

def get_domain_name(url):
    if not url:
        return None

    # Parse the URL to extract the netloc (domain with subdomain)
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc if parsed_url.netloc else url  # Handle raw URLs without scheme

    # Extract the second-level and top-level domain (SLD + TLD)
    match = re.search(r"([a-zA-Z0-9-]+\.[a-zA-Z]{2,})$", hostname)


    return match.group(1) if match else None
        

def md_to_text(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()




    
