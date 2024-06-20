#!make
include .env
read_env:
	@echo "AWS_ACCESS_KEY: $(MINIO_ACCESS_KEY)"
	@echo "AWS_SECRET_KEY: $(MINIO_SECRET_KEY)"
	@echo "AWS_REGION: $(MINIO_REGION)"
	@echo "MINIO_URL: $(MINIO_URL)"
	@echo "BUCKET_NAME: $(MINIO_BUCKET_NAME)"

start_minio: docker_start_minio prepare check

stop_minio: docker_stop_minio clean

docker_start_minio:
	docker-compose up -d

docker_stop_minio:
	docker-compose down

prepare:
	@echo "Create ALIAS"
	docker exec -it minio sh -c "mc alias set srv http://localhost:9000 $(MINIO_ACCESS_KEY) $(MINIO_SECRET_KEY)"
	@echo "Create bucket"
	docker exec -it minio sh -c "mc mb srv/$(MINIO_BUCKET_NAME)"
	@echo "Downloading data"
	mkdir -p ./data/tmp
	for year in {2021..2024}; do for month in {01..12}; do [ $$year -eq 2024 -a $$month -gt 4 ] && break; wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_$$year-$$(printf "%02d" $$month).parquet -P ./data/tmp; done; done
	@echo "Upload data"
	docker exec -it minio sh -c "mc cp /data/tmp/* srv/$(MINIO_BUCKET_NAME)"
	@echo "Remove tmp data"
	rm -rf ./data/tmp

clean:
	rm -rf ./data

# Helper command to ensure data directory is created on host system
.PHONY: prepare_data_directory
prepare_data_directory:
	@echo "Preparing data directory"
	mkdir -p ./data/$(MINIO_BUCKET_NAME)


check:
	aws configure --profile minio set aws_access_key_id $(AWS_ACCESS_KEY_ID)
	aws configure --profile minio set aws_secret_access_key $(AWS_SECRET_ACCESS_KEY)
	aws configure --profile minio set region $(AWS_REGION)
	aws --endpoint-url $(MINIO_URL) s3 ls s3://$(MINIO_BUCKET_NAME)  --profile minio