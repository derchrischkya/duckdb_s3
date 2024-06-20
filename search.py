import os
import duckdb
import time
from pandas import DataFrame as df
# Connect to DuckDB
conn = duckdb.connect()

# Install and load the HTTPFS extension for DuckDB
conn.execute("""
    INSTALL httpfs;
    LOAD httpfs;
""")

# Configure DuckDB to use AWS S3
conn.execute(f"""
    SET s3_region='us-east-1';
    SET s3_url_style='path';
    SET s3_access_key_id='minio_admin';
    SET s3_secret_access_key='minio_admin';
    SET s3_endpoint='localhost:9000';
    SET s3_use_ssl=false;
""")

def human_readable(column, data) -> list:
    return [{column[i]: row[i] for i in range(len(column))} for row in data]

# get fields from the parquet file
def get_fields() -> list:
    try:
        colums = []
        conn.execute("""CREATE TABLE read_parquet AS SELECT * FROM read_parquet('s3://demo/yellow_tripdata_2021-01.parquet') LIMIT 1;""")
        print("Parquet file read successfully")
        result = conn.execute("DESCRIBE read_parquet;").fetchall()
        for row in result:
            colums.append(row[0])   
        print(f"""Fields in the parquet file: {colums}""")
        return colums 
    except Exception as e:
        print(f"An error occurred: {e}")

def get_five_example_rows() -> list:
    try:
        print("Reading the first 5 rows in the parquet file")
        result = conn.execute("""SELECT * FROM read_parquet('s3://demo/yellow_tripdata_2021-01.parquet') LIMIT 5;""").fetchall()
        return result
    except Exception as e:
        print(f"An error occurred: {e}")

def get_data(sql) -> list:
    try:
        print(f"Reading the data from the parquet file with filter: {filter}")
        result = conn.execute(f"""{sql}""").df()
        return result
    except Exception as e:
        print(f"An error occurred: {e}")        
try:
    # Fetch the fields in the parquet file
    # colums = get_fields()
    # Fetch five example rows
    # data = get_five_example_rows()
    
    # Convert the data to human readable format
    # human_readable_list = human_readable(column=colums, data=data)
    # print(human_readable_list)
    
    # Run sql against the parquet files
    start = time.time()   
    sql_query = """
    select 
        period,
        count(*) as num_rides,
        round(avg(trip_duration), 2) as avg_trip_duration,
        round(avg(trip_distance), 2) as avg_trip_distance,
        round(sum(trip_distance), 2) as total_trip_distance,
        round(avg(total_amount), 2) as avg_trip_price,
        round(sum(total_amount), 2) as total_trip_price,
        round(avg(tip_amount), 2) as avg_tip_amount
    from (
        select
            date_part('year', tpep_pickup_datetime) as trip_year,
            strftime(tpep_pickup_datetime, '%Y-%m') as period,
            epoch(tpep_dropoff_datetime - tpep_pickup_datetime) as trip_duration,
            trip_distance,
            total_amount,
            tip_amount
        from parquet_scan('s3://demo/*.parquet')
        where trip_year >= 2021 and trip_year <= 2024
    )
    group by period
    order by period
"""

    data = get_data(sql=sql_query)
    print(f"Time taken to read the data: {time.time() - start}")
    
    # Print the dataframe
    print(data)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
