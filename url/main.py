import markdown
from bs4 import BeautifulSoup
from url.url import url
from text_processing.TextProcessing import TextProcessing
from services.save_in_dbs import save_to_db


url_ = url('https://www.uottawa.ca/study/sites/g/files/bhrskd296/files/2024-09/uOttawa-Viewbook-2025.pdf')

save_to_db_ = save_to_db()
save_to_db_.save_to_dbs(url_)

# text_processing = TextProcessing()
# text_processing.set_text(url_.text)
# print(text_processing.language)




# content = text_processing.process_text()


# print(content)