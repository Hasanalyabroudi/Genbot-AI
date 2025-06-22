from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from qdrant_client.http import models
import time



class db:
    def __init__(self,connection_url,collection_name):
        self.connection_url = connection_url
        self.collection_name = collection_name
        self.payload = {}
        self.vector= []

    def connect(self):
        try:
            self.client = QdrantClient(url=self.connection_url)
            ## Check if collection exists
            collections = self.client.get_collections()
            
            collection_names = [collection.name for collection in collections.collections]
            if self.collection_name not in collection_names:
                print(f"Qdrant: Collection {self.collection_name} not found")
                raise Exception(f"Collection {self.collection_name} not found")
            else:
                print(f"Qdrant: Connected to the {self.collection_name} collection")
        except Exception as e:
            print(f"Qdrant: Failed to connect to the database: {e}")
            if "Collection" in str(e) :
                print(f"Collection {self.collection_name} not found")
                ## Delete collection
                try:
                    self.delete_collection()
                except Exception as e:
                    pass
                try:
                    ## Create collection
                    print(f"Qdrant: Creating collection {self.collection_name} ... ")
                    self.create_collection(self.collection_name)
                    print(f"Qdrant: Collection {self.collection_name} created")
                    ## disconnect and reconnect
                    self.close_connection()
                    self.connect()
                except Exception as e:
                    print(f"Failed to create collection: {e}")
                    raise e
            else:
                print(f"Qdrant: Failed to connect to the database: {e}")
                raise e
    
    
    def close_connection(self):
        self.client.close()
        
    def create_collection(self,collection_name,vector_size=3072,distance='Cosine'):
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )
            print(f"Collection {collection_name} created")
        except Exception as e:
            print(f"Failed to create collection: {e}")
            raise e
        
    def add_element_to_payload(self,key,value):
        self.payload[key] = value
        return self.payload
    
    def add_vector(self,vector):
        self.vector = vector
        return self.vector
    
    def push_to_db(self):
        if not self.payload:
            raise Exception("Payload is empty")
        if not self.vector:
            raise Exception("Vector is empty")
        if self.payload['id'] is None:
            raise Exception("ID is empty")
        try:
            operation_info = self.client.upsert(
                collection_name=self.collection_name,
                wait=True,
                points=[
                    PointStruct(id=self.payload['id'], vector=self.vector, payload=self.payload),
                ],
            )
        except Exception as e:
            print(f"Failed to push to the database: {e}")
            raise e
        
    def find_nearest_neighbours(self,vector,limit=10):
        try:
            operation_info = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )
            return operation_info
        
        except Exception as e:
            print(f"Failed to find nearest neighbours: {e}")
            raise e
    
    def find_nearest_neighbours_within_ids(self,vector,ids,limit=10):

        if not ids:
            raise Exception("IDs are empty")
        
        # Create filter using HasIdCondition
        search_filter = models.Filter(
            must=[
            models.HasIdCondition(
                has_id=ids
            )
            ]
        )

        try:
            operation_info = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=limit,
                with_payload=True,
                with_vectors=False,
                query_filter=search_filter
            )
            return operation_info
        
        except Exception as e:
            print(f"Failed to find nearest neighbours: {e}")
            raise e
        
    def delete_element(self,id):
        try:
            self.client.delete(collection_name=self.collection_name, points_selector=[id])
            # print(f"Element with ID {id} deleted")
        except Exception as e:
            print(f"Failed to delete element: {e}")
            raise e
        
    def delete_collection(self):
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            print(f"Collection {self.collection_name} deleted")
        except Exception as e:
            print(f"Failed to delete collection: {e}")
            raise e
        

    def get_all_collections(self):

        '''
        
        This function returns all the collections in the database
        
        Returns:
            List: A list of all collections in the database

        '''

        try:
            collections = self.client.get_collections()

            return [collection.name for collection in collections.collections]
        except Exception as e:
            print(f"Failed to get all collections: {e}")
            raise e
        
    def search_element_by_(self, term, value):
        try:
            operation_info = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key=term,
                            match=models.MatchValue(value=value),
                        )
                    ]
                )
            )
            return operation_info
        except Exception as e:
            print(f"Failed to search element by term '{term}' and value '{value}': {e}")
            raise e
        
