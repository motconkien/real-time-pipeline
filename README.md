# 📊 Real-Time Data Pipeline with Kafka, Spark & AWS S3 (Local)

## 🌟 Overview

This project demonstrates a real-time data pipeline using:

- **Kafka** for streaming ingestion
- **Apache Spark** for real-time processing
- **AWS S3** (simulated locally) for storage
- **PostgreSQL / Redshift** as a data warehouse
- **Docker Compose** for containerized development

The pipeline simulates ingesting real-time Forex or Tweet data, transforms it using Spark, and stores it for analytics and dashboarding.

---

## 🛠 Tech Stack

| Component        | Tool/Service                  |
|------------------|-------------------------------|
| Ingestion        | Kafka                         |
| Processing       | Spark Structured Streaming    |
| Storage (Raw)    | AWS S3 (or local folder)      |
| Storage (DW)     | PostgreSQL                    |
| Deployment       | Docker + Docker Compose       |
| Optional UI      | Streamlit                     |

---

## 📁 Project Structure

```
├── dashboard/
│   ├── forex_dashboard.py       # Streamlit dashboard for real-time Forex visualization
│   └── Procfile                 # Procfile to deploy dashboard (e.g., on Heroku)
│
├── output/
│   ├── forex_data/              # Parquet files output from Spark streaming
│   └── forex_data_checkpoint/   # Spark streaming checkpoint directory
│
├── producer/
│   └── forex_producer.py        # Kafka producer script sending Forex data
│
├── spark-apps/
│   └── consumer.py              # Spark streaming consumer reading from Kafka and writing to PostgreSQL
│
├── .env                        # Environment variables (e.g., DB credentials, Kafka config)
├── .gitignore                  # Git ignore file
├── config.json                 # Configuration file for AWS or other keys
├── Dockerfile.producer         # Dockerfile to containerize producer service
├── kafka-docker-compose.yml    # Docker Compose for Kafka, Zookeeper, and related services
├── Makefile                    # Automation commands (build, run, clean, etc.)
├── README.md                   # This README file
├── requirements.txt            # Python dependencies

```
---

## 🚀 Getting Started
- Prerequisites
- Docker and Docker Compose installed
- Python 3.8+
- Java (for Spark)
- Kafka and Zookeeper (via kafka-docker-compose.yml)
- PostgreSQL instance running (local or Docker)

---

## ⚙️ Configuration

- Store sensitive data in .env and load it in your scripts.
- Configure config.json for AWS S3 keys if using S3 for storage.
- Update database connection details in spark-apps/consumer.py and .env.

---

## 📋 Usage

- Producer streams Forex data into Kafka topic forex_topic.
- Spark consumer reads from Kafka, processes data, writes parquet files locally (output/forex_data/) and ingests into PostgreSQL.
- Dashboard reads from PostgreSQL or parquet files to visualize Forex data in real-time.

---

## 📋 Automation
```
make kafka-up           # Start Kafka and services
make run-producer       # Run Kafka producer
make run-consumer       # Run Spark consumer
make run-dashboard      # Run Streamlit dashboard
make stop-all           # Stop all services

```
