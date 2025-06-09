import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel('traffic_stops.xlsx')

df = df.dropna(axis=1, how='all')


for column in df.columns:
    if df[column].dtype in ['int64', 'float64']:
        df[column] = df[column].fillna(df[column].mean())
    else:
        df[column] = df[column].fillna(df[column].mode()[0])


df = df.drop(columns=['driver_age_raw', 'violation_raw'], errors = 'ignore')
df['stop_date'] = pd.to_datetime(df['stop_date'], errors = 'coerce')

df['stop_date'] = df['stop_date'].dt.strftime('%d-%m-%Y')

#print(df.head())

username = 'postgres'
password = 'admin123'
host = 'localhost'
port = '5432'
database = 'test'


conn_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(conn_string)
df.to_sql('traffic_stops_cleaned', con=engine, if_exists='replace', index=False)
#print("✅ Data uploaded successfully!")
print(df.head(5))