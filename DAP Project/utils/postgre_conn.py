import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import logging
logging.basicConfig(filename='./logs/drugs_errors.log', level=logging.INFO)

class PostgresConnect():
    def __init__(self, connection_dict):
        '''INPUTS:
            connection_dict: Containing following key values
            user: Name of the user
            password: User's password to connect user to the service
            host: IP address of the host
            port: port number of postgres service
            db_name: Name of the database to be created, if it does not exits.'''
        self.connection_dict = connection_dict


    def createDB_table(self, table_name, df_to_dump):
        '''The fucntion creates databse and table and inserts data in table.
        INPUTS:
            table_name: Name of the Table to be created.
            df_to_dump: Dataframe to be dumped in Postgres
        CREDITS:
        This function was created with reference to script taken from https://cyruslab.net/2020/07/16/pythoncreate-database-if-not-exists-with-sqlalchemy/
        '''
        try:
            engine = create_engine(URL(**self.connection_dict))
            if not database_exists(engine.url):
                #print('Database does not exists! Creating Database.')
                create_database(engine.url)
                #print('Database created successfully!')
            else:
                # Connect the database if exists.
                # #print('Database Exists! Connecting...')
                engine.connect()
                # #print('Connection Successfull!')
            #print('Creating Table...')
            df_to_dump.to_sql(table_name, con=engine, index=False, if_exists='replace')#Insert Data in table
            #print('Table Created Successfully')
        except OperationalError:
            #print('Operational Error! check logs for info!')
            logging.error("Exception occurred at createDB_table", exc_info=True)
        except Exception as e:
            #print('Something went wrong! check logs for more info!')
            logging.error("Exception occurred at createDB_table", exc_info=True)
        finally:
            if engine:
                engine.dispose()

    def get_data(self, query):
        '''The fucntion creates databse and table and inserts data in table.
        INPUTS:
        query: An SQL query which will be executed on table created in db.
        OUTPUT:
        df: Pandas DataFrame holding the output of executed query.
        '''
        try:
            engine = create_engine(URL(**self.connection_dict))
            if not database_exists(engine.url):
                #print('Database does not exists!, check connection string!')
                return None
            else:
                # Connect the database if exists.
                #print('Database Exists! Connecting...')
                engine.connect()
                #print('Connection Successfull!')
            #print('Executing Query!')
            df = pd.read_sql_query(query, engine)
            if engine:
                engine.dispose()
            #print('Query executed Successfully.')
            return df
        except Exception as e:
            #print('Something went wrong! check logs for more info!')
            logging.error("Exception occurred at createDB_table", exc_info=True)

        
    