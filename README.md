# 📊 Real-Time Data Pipeline with Kafka, Spark, Airflow & AWS S3 (Local)

## 🌟 Overview

This project demonstrates a real-time data pipeline using:

- **Kafka** for streaming ingestion
- **Apache Spark** for real-time processing
- **Airflow** for workflow orchestration
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
| Orchestration    | Apache Airflow                |
| Storage (Raw)    | AWS S3 (or local folder)      |
| Storage (DW)     | Redshift / PostgreSQL         |
| Deployment       | Docker + Docker Compose       |
| Optional UI      | Streamlit / Superset Dashboard|

---

## 📁 Project Structure

