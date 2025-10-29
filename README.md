# Log Analytics Pipeline

## Project Overview

Data engineering pipeline that simulates real-world log analytics using MongoDB, Apache Airflow, and Python. This project demonstrates a complete ETL workflow following industry best practices, from data generation through transformation to visualization and automated orchestration.
The pipeline processes synthetic application logs (user activities, events, errors) and transforms them into actionable insights through aggregations and visualizations, mimicking real-world scenarios such as user behavior tracking, performance monitoring, or sales analytics.

## Business Case

Organizations need to analyze large volumes of log data to:

Monitor user behavior across different countries and devices
Track application events (logins, purchases, errors) in real-time
Identify trends and anomalies in system usage
Generate reports for stakeholders with visual analytics

This pipeline automates the entire process, from data collection to insight generation, reducing manual effort and enabling data-driven decision-making.

### Built With

This project uses the following major frameworks and libraries:

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
* ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
* ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
* ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
* ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
* ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

## Pipeline Stages:

### 1. Log Generation

- Creates synthetic log data using Faker library

- Simulates user events: login, logout, purchase, error, click, view

- Includes metadata: IP address, device type, country

- Stores raw logs in MongoDB


### 2. ETL Process

- Extract: Retrieves raw logs from MongoDB

- Transform: Cleans data, extracts date/time, flattens nested fields

- Aggregate: Groups events by date, country, and event type

- Load: Performs upsert operations to MongoDB daily summary collection


### 3. Analysis & Visualization

#### Generates 5 types of analytical charts:

- Events by type (bar chart)

- Top 10 countries by activity (horizontal bar)

- Events over time (line chart)

- Event distribution by top countries (stacked bar)

- Events heatmap (date vs event type)

Exports summary statistics to CSV files


### 4. Orchestration

- Apache Airflow DAG schedules pipeline execution

- Runs hourly with automatic retries

- Ensures sequential task dependencies

## Environment Setup

### 1. Clone the repository

```bash
git clone https://github.com/dawidfila/event-log-pipeline
cd event-log-pipeline
```

### 2. Create environment file

```bash
cp .env.example .env
```

#### Edit .env and configure your credentials:

```bash
# Generate Fernet key:
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate webserver secret:
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start the services

Build Docker images

```bash
docker-compose build
```

Initialize Airflow database 

```bash
docker-compose up airflow-init
```

Start all services

```bash
docker-compose up -d
```

If the default admin user doesn't work or wasn't created:

**Check running containers:**

```bash
docker ps
```
**Enter the webserver container:**

```bash
docker exec -it airflow_webserver bash
```

**Create admin user manually:**

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```