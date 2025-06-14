

# Run Kafka 
kafka-up:
	docker-compose -f kafka-docker-compose.yml up -d
# Stop Kafka
kafka-down:
	docker-compose -f kafka-docker-compose.yml down

#stop all 
stop-all:
	docker-compose -f kafka-docker-compose.yml down --remove-orphans

#run bash 
bash-airflow:
	docker-compose -f airflow-docker-compose.yml exec airflow-scheduler bash
# Run procedure 
run-producer:
	python3 producer/forex_producer.py

# Run consumer 
run-consumer:
	spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.hadoop:hadoop-aws:3.3.4,org.postgresql:postgresql:42.5.4 spark-apps/consumer.py

#Run dashboard 
run-dashboard:
	streamlit run dashboard/forex_dashboard.py