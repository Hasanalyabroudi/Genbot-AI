import concurrent
import pandas as pd
from pymongo import MongoClient
from typing import *
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class db:
    def __init__(self, CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME='page_content'):
        self.CONNECTION_STRING = CONNECTION_STRING
        self.DATABASE_NAME = DATABASE_NAME
        self.COLLECTION_NAME = COLLECTION_NAME
        self.content = {}

    def connect(self):
        try:
            self.client = MongoClient(self.CONNECTION_STRING)
            self.db = self.client[self.DATABASE_NAME]
            self.collection = self.db[self.COLLECTION_NAME]
           
            ## check if the db exists
            if self.DATABASE_NAME not in self.client.list_database_names():
                print(f"Database {self.DATABASE_NAME} not found")
                raise Exception("Database not found")
            
            ## check if the collection exists
            if self.COLLECTION_NAME not in self.db.list_collection_names():
                print(f"Collection {self.COLLECTION_NAME} not found")
                raise Exception("Collection not found")

            

            print(f"Successfully connected to the database: {self.COLLECTION_NAME}")
        except Exception as e:
            
            if str(e) == "Database not found":
                print(f"Database {self.DATABASE_NAME} not found")
                self.delete_db_if_exists(self.DATABASE_NAME)
                print(f"Creating database {self.DATABASE_NAME}...")
                self.create_db(self.DATABASE_NAME)
                print(f"Database {self.DATABASE_NAME} created")
                self.create_collection(self.DATABASE_NAME,self.COLLECTION_NAME)
                print(f"Collection {self.COLLECTION_NAME} created")

            elif str(e) == "Collection not found":
                print(f"Collection {self.COLLECTION_NAME} not found")
                print(f"Creating collection {self.COLLECTION_NAME}...")
                self.create_collection(self.DATABASE_NAME,self.COLLECTION_NAME)
                print(f"Collection {self.COLLECTION_NAME} created")

            else:

                print(f"Failed to connect to the database: {e}")
                raise e

    def close_connection(self):
        self.client.close()

    def create_db(self, name,):
        new_db = self.client[name]
        collection = new_db[name]
        collection.insert_one({"name": "test", "value": 123})
        collection.delete_many({})
        new_db.drop_collection(name)

    def delete_db_if_exists(self, name):
        ## check if the db exists
        if name not in self.client.list_database_names():
            print(f"Database {name} not found")
            return
        
        self.client.drop_database(name)
        print(f"Database {name} deleted")

    def create_collection(self,db,collection):
        new_db = self.client[db]
        new_db.create_collection(collection)
        print(f"Collection {collection} created")


    def add_element(self, element_name, element):
        self.content[element_name] = element
        return element
       
    def push_to_db(self):
        try:
            if not self.content:
                return
            self.collection.insert_one(self.content)
            self.content = {}

        except Exception as e:
            if 'E11000' in str(e):
                print(f"Element already in the collection. Updating the element ...")
                ## Delete the element from the collection
                self.collection.delete_one({"_id": self.content['_id']})

                ## Add the element again
                self.collection.insert_one(self.content)
                self.content = {}
                

    def empty_db(self):
        self.collection.delete_many({})
        print(f"All items in the collection have been deleted.")

    def query_documents(self):
        '''
        This function queries all documents in the collection

        Returns:
            Collection: A collection of all documents in the collection
        
        '''
        ## query all documents in the collection
        documents = self.collection.find()
        return documents
    
    def find_number_of_documents(self):
        ## find the number of documents in the collection
        number_of_documents = self.collection.count_documents({})
        return number_of_documents
    
    def query_document_by_id(self, id):
        ## query document by id
        document = self.collection.find_one({"_id": id})
        return document
    
    def query_document_IDxURL(self):
        ## query all documents in the collection only get id and url
        documents = self.collection.find({},{"_id":1,"url":1})
        return documents


    def update_element(self,id):
        ## add element to the db with the given id
        ## need to get the attributes and values from the class and the 

        ## find the attributes and values
        doument = self.query_document_by_id(id)
        if doument is None:
            print(f"Document with id {id} not found")
            return
        
        to_add = {**doument,**self.content}
        self.collection.update_one({"_id": id}, {"$set": to_add})
        self.content = {}
    
    def find_all_ids(self):
        ## find all ids in the collection
        ids = self.collection.distinct("_id")
        return ids

    def find_document_text_embeddings(self, id,embedder):
        ## find the document with the given id and add the embeddings
        document = self.query_document_by_id(id)
        if document is None:
            print(f"Document with id {id} not found")
            return
        original_text = document['original_content'].replace('\n',' ').replace('  ',' ')

        ## check if embeddings are already in the database
        if 'vector_embedding' in document:
            embeddings = document['vector_embedding']

        else:
        
            ## if not, generate embeddings
            print(f"Embeddings for {id} are being generated")
            embeddings = embedder.embed_documents([original_text])[0]
            self.add_element('vector_embedding',embeddings)
            self.update_element(id)
        
        return [original_text,embeddings]
        
    def get_all_dbs(self):
        '''
        This function returns all the databases available with a page_content collection
        
        Returns:
            List: A list of all databases with a page_content collection
        '''
        ## Check if connection is active
        try:
            self.client.server_info()
        except:
            self.connect()

        ## get all databases in mongo
        databases = self.client.list_database_names()
        databases_with_collection = []
        for db in databases:
            if 'page_content' in self.client[db].list_collection_names():
                databases_with_collection.append(db)
        return databases_with_collection
    
    def get_internal_links(self,ids: List) -> dict:
        '''
        This function returns all the internal links in the database
        
        Args:
            ids (List): A list of ids to get the internal links for
        
        Returns:
            List: A list of internal links
        '''
        internal_links = pd.DataFrame(columns=['id','n_internal_links'])
        def process_id(id):
            document = self.query_document_by_id(id)
            if document is None:
                print(f"Document with id {id} not found")
                return None
            if 'number_of_internal_links' in document:
                return pd.DataFrame({'n_internal_links': int(document['number_of_internal_links']),'url': [document['url']]})
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ids)/10) as executor:
            results = {executor.submit(process_id, id): id for id in ids}
            for future in tqdm(concurrent.futures.as_completed(results), total=len(results), desc="Processing IDs"):
                id = results[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f'id {id} generated an exception: {exc}')
                else:
                    if result is not None:
                        internal_links = pd.concat([internal_links, result])
        
        internal_links = internal_links[['url','n_internal_links']]
        ## format it to a dictionary {url: n_internal_links}
        internal_links = internal_links.set_index('url')['n_internal_links'].to_dict()
        return internal_links
    