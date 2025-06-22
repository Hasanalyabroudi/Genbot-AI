import uuid

class dblogg:
    def __init__(self,sql_db):
        self.sql_db = sql_db

        
    def create_database_log_table(self):
        '''
            This function creates the tables necessary for the database logging

            Tables:
            1- database_name : ID | name 
            2- database_details : ID | total pages | domain | system prompt | model_id | temperature 
            3- models : ID | name | endpoint
        '''
        self.sql_db.connect()
        # Get a cursor FROM THE CONNECTION (self.sql_db should be a connection object)
        self.sql_db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                ID UUID PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                ENDPOINT VARCHAR(255) NOT NULL
            );
        ''')
        
        self.sql_db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS database_name (
                ID UUID PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL
            );
        ''')

        self.sql_db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS database_details (
                ID UUID PRIMARY KEY,
                total_pages INTEGER,
                domain VARCHAR(255),
                system_prompt TEXT,
                model_id UUID REFERENCES models(ID),
                temperature REAL
            );
        ''')
        self.sql_db.conn.commit()
        self.sql_db.CloseConnection()
        print("Database log tables created successfully.")

        

        
    def insert_database_name(self, name):
        '''
            This function inserts the database name into the database_name table

            Parameters:
            name (str): The name of the database to be inserted
        '''
        self.sql_db.connect()
        ## check if the name already exists in the table
        self.sql_db.cursor.execute('''
            SELECT ID FROM database_name WHERE NAME = %s
        ''', (name,))
        result = self.sql_db.cursor.fetchone()
        if result:
            print(f"Database name '{name}' already exists.")
            return result[0]
        # Generate a new UUID for the ID column

        id = (uuid.uuid4())
        self.sql_db.cursor.execute('''
            INSERT INTO database_name (ID, NAME)
            VALUES (%s, %s)
        ''', (id, name))
        self.sql_db.conn.commit()
        self.sql_db.CloseConnection()
        print(f"Database name '{name}' inserted successfully.")
        return id
        

    def insert_database_details(self, db_id, total_pages, domain, system_prompt, model_id, temperature):
        '''
            This function inserts the database details into the database_details table

            Parameters:
            total_pages (int): The total number of pages in the database
            domain (str): The domain of the database
            system_prompt (str): The system prompt used for the database
            model_id (UUID): The ID of the model used for the database
            temperature (float): The temperature used for the database
        '''
        self.sql_db.connect()
        # Check if the database ID already exists in the table
        self.sql_db.cursor.execute('''
            SELECT ID FROM database_details WHERE ID = %s
        ''', (db_id,))
        result = self.sql_db.cursor.fetchone()
        if result:
            print(f"Database details for ID '{db_id}' already exist. Updating...")
            ## update by deleting the old entry and inserting a new one
            self.sql_db.cursor.execute('''
                DELETE FROM database_details WHERE ID = %s
            ''', (db_id,))
            self.sql_db.conn.commit()
        
        self.sql_db.cursor.execute('''
            INSERT INTO database_details (ID, total_pages, domain, system_prompt, model_id, temperature)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (db_id, total_pages, domain, system_prompt, model_id, temperature))
        self.sql_db.conn.commit()
        self.sql_db.CloseConnection()
        print(f"Database details inserted successfully.")
    
        return id
    
    def insert_model(self, name, endpoint):
        '''
            This function inserts the model into the models table

            Parameters:
            name (str): The name of the model to be inserted
            endpoint (str): The endpoint of the model to be inserted
        '''
        self.sql_db.connect()
        #Check endpoint if it already exists in the table
        self.sql_db.cursor.execute('''
            SELECT ID FROM models WHERE ENDPOINT = %s
        ''', (endpoint,))
        result = self.sql_db.cursor.fetchone()
        if result:
            print(f"Model with endpoint '{endpoint}' already exists.")
            return result[0]
        
        # Generate a new UUID for the ID column
        id = uuid.uuid4()
        
        self.sql_db.cursor.execute('''
            INSERT INTO models (ID, NAME, ENDPOINT)
            VALUES (%s, %s, %s)
        ''', (id, name, endpoint))
        self.sql_db.conn.commit()
        self.sql_db.CloseConnection()
        print(f"Model '{name}' inserted successfully.")
        return id
    
    def add_default_models(self):
        '''
            This function adds default models to the models table
            gpt-4o : 'https://genbotai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview'
        '''
        self.insert_model(
            name='gpt-4o',endpoint='https://genbotai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview'
        )
        print("Default models added successfully.")
    
    def get_db_details(self, db_id):
        '''
            This function retrieves the database details from the database_details table

            Parameters:
            db_id (UUID): The ID of the database to be retrieved
        '''
        self.sql_db.connect()
        self.sql_db.cursor.execute('''
            SELECT * FROM database_details WHERE ID = %s
        ''', (db_id,))
        result = self.sql_db.cursor.fetchone()
        self.sql_db.CloseConnection()
        if result:
            columns = [desc[0] for desc in self.sql_db.cursor.description]
            return dict(zip(columns, result))
        else:
            print(f"No database details found for ID '{db_id}'.")
            return None
        
    def get_model_details(self, model_name):
        '''
            This function retrieves the model details from the models table

            Parameters:
            model_name (str): The name of the model to be retrieved
        '''
        self.sql_db.connect()
        self.sql_db.cursor.execute('''
            SELECT * FROM models WHERE NAME = %s
        ''', (model_name,))
        result = self.sql_db.cursor.fetchone()
        self.sql_db.CloseConnection()
        if result:
            columns = [desc[0] for desc in self.sql_db.cursor.description]
            details = dict(zip(columns, result))
            id = details['id']
            return id
        else:
            print(f"No model details found for name '{model_name}'.")
            return None

    
    def setup_new_db(self,domain):
        '''
            This function sets up a new database by creating the necessary tables and inserting the database name

            Parameters:
            domain (str): The domain of the database to be set up
        '''
        self.sql_db.connect()
        database_name = domain.replace('.','_')
        self.create_database_log_table()
        ## set default model to gpt-4-o
        model_id = self.get_model_details('gpt-4o')
        if model_id is None:
            self.add_default_models()
            model_id = self.get_model_details('gpt-4o')
        ## check if the database name already exists in the table
        db_id = self.insert_database_name(database_name)
        self.insert_database_details(
            db_id=db_id,
            total_pages=0,
            domain=domain,
            system_prompt=''''
                    You are an AI Tutor.
                    ''',
            model_id=model_id,
            temperature=0.7
        )
        self.sql_db.CloseConnection()
        return db_id
    
    def update_number_of_pages(self,db_id,number_of_pages):
        '''
            This function updates the number of pages in the database_details table

            Parameters:
            db_id (UUID): The ID of the database to be updated
            number_of_pages (int): The new number of pages to be updated
        '''
        self.sql_db.connect()
        self.sql_db.cursor.execute('''
            UPDATE database_details SET total_pages = %s WHERE ID = %s
        ''', (number_of_pages, db_id))
        self.sql_db.conn.commit()
        print(f"Number of pages updated successfully.")
        self.sql_db.CloseConnection()
        return True


       