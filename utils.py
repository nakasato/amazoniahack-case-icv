import os
import pandas as pd
import psycopg2 as pg
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st


def gpt(prompt, model='gpt-4o-mini'):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[
            {'role': 'system', 
             'content': prompt}
        ]
    )
    
    return response.choices[0].message.content


def connect_db():
    # Load environment variables from .env file
    load_dotenv()

    try:
        # Establish a connection to the PostgreSQL database
        con = pg.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

        # Create a cursor object using the connection
        cur = con.cursor()

        # Execute a sample query
        cur.execute('SELECT version()')

        # Fetch and print the result
        db_version = cur.fetchone()
        print(f'Connected to PostgreSQL. Database version: {db_version}')

    except pg.Error as e:
        print(f'Error connecting to PostgreSQL: {e}')

    return con, cur


def read_sql(query):
    try:
        # Establish a connection to the PostgreSQL database
        con, _ = connect_db()

        # Use pandas to read SQL query results into a DataFrame
        df = pd.read_sql_query(query, con)

        # Close communication with the PostgreSQL database
        con.close()

    except pg.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    
    return df


def get_table_names():
    try:
        # Establish a connection to the PostgreSQL database
        con, cur = connect_db()

        # SQL query to get all table names in the 'public' schema
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """

        # Execute the query
        cur.execute(query)

        # Fetch all results and store table names in a list
        table_names = [row[0] for row in cur.fetchall()]

        # Close communication with the PostgreSQL database
        cur.close()
        con.close()

        return table_names


        # Close communication with the PostgreSQL database
        con.close()

    except pg.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    
    return df
