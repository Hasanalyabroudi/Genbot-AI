import PyPDF2  
import uuid
import os 
import io  


class save_to_db():
    def __init__(self,sql_db,mongo_db,embbeder,text_procesing):
        self.sql_db = sql_db
        self.mongo_db = mongo_db
        self.text_procesing = text_procesing
        self.embedder = embbeder

        ## Initialize the SQL database
        # self.sql_db.connect()
        # self.sql_db.initialize_check()
        # self.sql_db.CloseConnection()

        


    def save_html_to_dbs(self,url):
        try:

            self.sql_db.connect()
            self.embedder.qdrant_db_.connect()


            html = url.content
            original_text = url.text 
            markdown = url.markdown
            internal_link = url.internal_links
            url = url.url
            

            ## detecting the language
            self.text_procesing.set_text(original_text)
            language = self.text_procesing.language

            ## Cleaning the text
            content = self.text_procesing.process_text()
            WordMatrix = self.text_procesing.CreateWordFrequencyMatrix()


            ## Saving the html to the URL + ID to the SQL database
            internal_link_plus_url = internal_link.copy()
            internal_link_plus_url.append(url)

            ## URL Frequency
            url_freq = {}
            for link in set(internal_link):
                url_freq[link] = internal_link.count(link)

            ## Saving Internal Links and URL to the SQL database
            try:
                self.sql_db.InsertIntoIDxURL(internal_link_plus_url)
            except Exception as e:
                print(f"Failed Inserting into IDxURL: {e}")

            ## Saving the WordMatrix to the SQL database
            try:
                self.sql_db.InsertIntoIDxWord(WordMatrix['words'])
            except Exception as e:
                print(f"Failed Inserting into IDxWORDS: {e}")

            ## Saving into the WORDxURLxFreq
            try:
                self.sql_db.InsertIntoWORDxURLxFreq(url,WordMatrix)
            except Exception as e:
                print(f"Failed Inserting into WORDxURLxFreq: {e}")

                ## Saving into URLxFreq
                # try:
                #     self.sql_db.InsertIntoURLxFreq(url_freq)
                # except Exception as e:
                #     print(f"Failed Inserting into URLxFreq: {e}")

            ## getting current url id
            ID = self.sql_db.cursor.execute(f"""SELECT ID FROM IDxURL WHERE URL = '{url}'""")
            ID = self.sql_db.cursor.fetchone()[0]
            

            
            self.sql_db.CloseConnection()

            self.mongo_db.connect()


            ## Saving the html content to the SQL database
            self.mongo_db.add_element('_id', str(ID))
            self.mongo_db.add_element('url', str(url))
            self.mongo_db.add_element('html', str(html))
            self.mongo_db.add_element('original_content', str(original_text))
            self.mongo_db.add_element('cleaned_content', str(content.text))
            self.mongo_db.add_element('markdown', str(markdown))
            self.mongo_db.add_element('number_of_internal_links', len(internal_link))
            self.mongo_db.add_element('internal_links', (internal_link))
            self.mongo_db.add_element('file_type', 'HTML')
            self.mongo_db.add_element('language', str(language))
            

            self.mongo_db.push_to_db()

            ## Disconnecting from the databases
            self.mongo_db.close_connection()

            ## Embedding the content
            self.embedder.mongo_db_.connect()
            self.embedder.embedd_add_to_qdrant(ID)
            self.embedder.mongo_db_.close_connection()
            self.embedder.qdrant_db_.close_connection()



            return True
        except Exception as e:  
            print(f"Error: {e}")
            raise e
    
    def save_pdf_to_dbs(self,url):
        try:
            self.sql_db.connect()
            self.embedder.qdrant_db_.connect()

        
            print(f"Saving {url} to the databases")

            ## getting the text
            original_text = url.content
            internal_link = url.internal_links
            url = url.url



            ## detecting the language
            self.text_procesing.set_text(original_text)
            language = self.text_procesing.language

            ## Cleaning the text
            content = self.text_procesing.process_text()
            WordMatrix = self.text_procesing.CreateWordFrequencyMatrix()


            ## Saving the html to the URL + ID to the SQL database
            internal_link_plus_url = internal_link.copy()
            internal_link_plus_url.append(url)

            ## URL Frequency
            url_freq = {}
            for link in set(internal_link):
                url_freq[link] = internal_link.count(link)

            ## Saving Internal Links and URL to the SQL database
            try:
                self.sql_db.InsertIntoIDxURL(internal_link_plus_url)
            except Exception as e:
                print(f"Failed Inserting into IDxURL: {e}")

            ## Saving the WordMatrix to the SQL database
            try:
                self.sql_db.InsertIntoIDxWord(WordMatrix['words'])
            except Exception as e:
                print(f"Failed Inserting into IDxWORDS: {e}")

            ## Saving into the WORDxURLxFreq
            try:
                self.sql_db.InsertIntoWORDxURLxFreq(url,WordMatrix)
            except Exception as e:
                print(f"Failed Inserting into WORDxURLxFreq: {e}")

            ## Saving into URLxFreq
            # try:
            #     self.sql_db.InsertIntoURLxFreq(url_freq)
            # except Exception as e:
            #     print(f"Failed Inserting into URLxFreq: {e}")

            ## getting current url id
            ID = self.sql_db.cursor.execute(f"""SELECT ID FROM IDxURL WHERE URL = '{url}'""")
            ID = self.sql_db.cursor.fetchone()[0]
            

            
            self.sql_db.CloseConnection()

            self.mongo_db.connect()


            ## Saving the html content to the SQL database
            self.mongo_db.add_element('_id', str(ID))
            self.mongo_db.add_element('url', str(url))
            self.mongo_db.add_element('original_content', str(original_text))
            self.mongo_db.add_element('cleaned_content', str(content.text))

            ## in lack of a real readme we will save a duplicate of the original content
            self.mongo_db.add_element('markdown', str(original_text))

            self.mongo_db.add_element('number_of_internal_links', len(internal_link))
            self.mongo_db.add_element('internal_links', (internal_link))
            self.mongo_db.add_element('file_type', 'PDF')
            self.mongo_db.add_element('language', str(language))

            self.mongo_db.push_to_db()

            ## Disconnecting from the databases
            self.mongo_db.close_connection()

            ## Embedding the content
            self.embedder.mongo_db_.connect()
            self.embedder.embedd_add_to_qdrant(ID)
            self.embedder.mongo_db_.close_connection()
            self.embedder.qdrant_db_.close_connection()

            
            return True
    
        except Exception as e:  
            print(f"Error: {e}")
            raise e
        
        ## Write Function that can support both pdf and html
    def save_to_dbs(self,url):
        if url.page_type == 'PDF':
            self.save_pdf_to_dbs(url)
        elif url.page_type == 'HTML':
            self.save_html_to_dbs(url)
        else:
            print(f"Unknown page type: {url}")
            return False
        return True

        

