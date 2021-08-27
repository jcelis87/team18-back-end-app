import pickle
import os
import pandas as pd

import psycopg2
from config import config


# def load_obj (name):
#     with open(name, 'rb') as f:
#         #return pickle.load(f)
#         return pd.read_pkl(name)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'geo_database_sample_50.csv')

# geo_df = load_obj(my_file)
geo_df = pd.read_csv(my_file,  index_col=0)

# print(my_file)
print(type(geo_df))
print(list(geo_df.columns))
print(geo_df.head())
print(geo_df.iloc[1])


def create_tables():
    """ create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE IF NOT EXISTS geographicnames (
            gn_id SERIAL PRIMARY KEY,
            geographic_name VARCHAR(255),
            geometry VARCHAR(255), 
            site_type VARCHAR(255),
            date_mod VARCHAR(255),
            dictionary VARCHAR(255),
            geo_database VARCHAR(255),
            google_maps VARCHAR(255),
            open_street_maps VARCHAR(255),
            aerial_photograph VARCHAR(255),
            cartographic_sheet VARCHAR(255),
            longitude VARCHAR(255),
            latitude VARCHAR(255)
            );
        """
    )

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        print('creating tables')
        # for command in commands:
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_data(data):
    """ insert multiple vendors into the table  """
    command = (
        """
        INSERT INTO geographicnames (
            geographic_name,
            geometry, 
            site_type,
            date_mod,
            dictionary,
            geo_database,
            google_maps,
            open_street_maps,
            aerial_photograph,
            cartographic_sheet,
            longitude,
            latitude
        ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    )

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(command, data)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_all_data():
    """ Gets data from table  """

    command = (
        """
        SELECT * FROM geographicnames ORDER BY gn_id
        """
    )

    conn = None
    try:

        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command)

        rows = cur.fetchall()

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows


def get_data(gn_id):
    """ Gets data from table  """

    command = (
        """
        SELECT * FROM geographicnames WHERE gn_id = %s
        """
    )

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(command, (gn_id, ))
        row = cur.fetchone()

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return row


# def get_columns_names():
#     """ Gets data from table  """

#     command = (
#         """
#         SELECT *
#         FROM INFORMATION_SCHEMA.COLUMNS
#         WHERE table_name = geographicnames
#         """
#     )

#     conn = None
#     try:
#         # read database configuration
#         params = config()
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(**params)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(command)
#         row_names = cur.fetchall()

#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

#     return row_names


data = [
    (
        'La Florida',
        'POINT Z (4710736.633 1978740.3454 0)',
        '',
        '2016-08-30T00:00:00+00:00',
        'False',
        'True',
        'False',
        'False',
        'False',
        'False',
        '75.6053837189674',
        '3.80363851526759'
    ),
    (
        'Puesto de Salud',
        'POINT Z (4710736.633 1978740.3454 0)',
        '',
        '2016-08-30T00:00:00+00:00',
        'False',
        'True',
        'False',
        'False',
        'False',
        'False',
        '75.3331601576004',
        '3.8118313115418'
    ),
]

# create_tables()
insert_data(data)
# get_data()
get_columns_names()
