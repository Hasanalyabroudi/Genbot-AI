import time
import concurrent
from langchain_openai import AzureOpenAIEmbeddings
from dbs.mongo_db.db import db as mongo_db
from dbs.qdrant_db.db import db as qdrant_db
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv
import uuid
load_dotenv()

## Load environment variables
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
EMBEDDINGS_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT_CAPSTONE')


class embedder:
    def __init__(self,mongo_db_,qdrant_db_,openai_embedder):
        self.mongo_db_ = mongo_db_
        self.qdrant_db_ = qdrant_db_
        self.openai_embedder = openai_embedder
        self.splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1500,
        chunk_overlap = 300,
        length_function=len

        )

        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on= [("#", "Header 1"),("##", "Header 2"),("###", "Header 3"),])


    def embedd_add_to_qdrant(self,document_id):
        try:
            ## Get the document
            document = self.mongo_db_.query_document_by_id(str(document_id))
            corpus = str(document['markdown'])

            ## Split the document into section using langchain document splitter
            if document['file_type'] == 'PDF':
                chunks = self.splitter.split_text(text=corpus)
            elif document['file_type'] == 'HTML':
                chunks = self.splitter.split_documents(documents=corpus)
                chunks = [chunk.page_content for chunk in chunks ]
            
            embeddings = self.openai_embedder.embed_documents(chunks)
            ## check if embeddings were generated correctly
            if len(embeddings) != len(chunks):
                print("Error in embeddings")
                print(len(embeddings))
                raise Exception("Error in embeddings")
            
            if len(embeddings[0])<750:
                print("Error in embeddings")
                print(embeddings[0])
                raise Exception("Error in embeddings")
            print(f"Embeddings generated for {document_id}")
            id = str(document['_id'])

            ## check if the document is already in the database under document_id
            elements = self.qdrant_db_.search_element_by_(term="document_id",value=id)
            ids = [element.payload['id'] for element in elements[0]]
            if ids:
                print(f"Document {id} already in the database")
                ## delete the documents
                for id in ids:
                    self.qdrant_db_.delete_element(id)

                print(f"Deleted {len(ids)} documents")

            

            ## Add embeddings to the database with progress bar
            for k in tqdm(range(len(embeddings)), desc="Adding embeddings to database"):
                self.qdrant_db_.add_vector(embeddings[k])
                self.qdrant_db_.add_element_to_payload('id', str(uuid.uuid4()))
                self.qdrant_db_.add_element_to_payload('url',document['url'])
                self.qdrant_db_.add_element_to_payload('document_id', id)
                self.qdrant_db_.add_element_to_payload('section',k)
                self.qdrant_db_.add_element_to_payload('section_text',chunks[k])
                

                self.qdrant_db_.push_to_db()
        except Exception as e:
            print(f"Error: {e}")

    def SplitText(self,Text):
        chunks = self.rec_text_splitter.split_text(Text)
        return chunks





