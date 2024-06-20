# DuckDB fetch data from MinIO
This project demonstrates how to fetch data from MinIO and run SQL queries on it using DuckDB.

## Requirements
- Python
- Docker

## Pre-Infrastructure
### MinIO
The MinIO server is used as local S3 storage. The server is started using docker-compose. The server is started on `localhost:9000`. The access key and secret key are `minioadmin` and `minioadmin` respectively.
On startup the yellow taxi data of new york is uploaded to the MinIO server from `https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page`

#### Start MinIO
```bash
cd minio
make start_minio
```

#### Stop MinIO
```bash
cd minio
make stop_minio
```
## Search/Analysis 
### DuckDB
DuckDB is used to fetch parquet data from MinIO and run SQL queries on it. 

- Modify the `search.py` file to run the desired SQL queries on the data.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 search.py
```

# Credits
https://medium.com/towards-data-science/duckdb-and-aws-how-to-aggregate-100-million-rows-in-1-minute-3634eef06b79