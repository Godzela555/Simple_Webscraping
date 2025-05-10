import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import requests


url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ['Name', 'MC_USD_Billions']
csv_path = './Largest_banks_data.csv'
db_name = 'Banks.db'
table_name = 'Largest_banks'


def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M-%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open('code_log.txt', 'a') as f:
        f.write(timestamp + ':' + message + '\n')


def extract(url, table_attribs):
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) >= 3:
            name = col[1].get_text(strip=True)
            market_cap = col[2].get_text(strip=True)
            data_dict = [{'Name': name, 'MC_USD_Billions': market_cap}]
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
    return df


def transform(df, csv_path):
    exchange_df = pd.read_csv('exchange_rate.csv')
    exchange_rate = exchange_df.set_index('Currency').to_dict()['Rate']

    df['MC_USD_Billions'] = df['MC_USD_Billions'].astype(float)

    df['MC_GBP_Billions'] = [
        np.round(x*exchange_rate['GBP'], 2)for x in df['MC_USD_Billions']]
    df['MC_EUR_Billions'] = [
        np.round(x*exchange_rate['EUR'], 2)for x in df['MC_USD_Billions']]
    df['MC_INR_Billions'] = [
        np.round(x*exchange_rate['INR'], 2)for x in df['MC_USD_Billions']]
    return df


def load_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)
    return df


def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_queries(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


# Step 1: Extract
df = extract(url, table_attribs)
log_progress("Data extracted")

# Step 2: Transform
df = transform(df, csv_path)
log_progress("Data transformed")

# Step 3: Load to CSV
load_to_csv(df, csv_path)
log_progress("Data written to CSV")

# Step 4: Load to Database
conn = sqlite3.connect(db_name)
load_to_db(df, conn, table_name)
log_progress("Data loaded to database")

# Step 5: Run Queries
run_queries("SELECT * FROM Largest_banks", conn)
run_queries("SELECT AVG(MC_GBP_Billions) FROM Largest_banks", conn)
run_queries("SELECT Name FROM Largest_banks LIMIT 5", conn)

conn.close()

log_progress("Process completed")
