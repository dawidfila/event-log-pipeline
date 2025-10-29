# Log Analytics Pipeline

## Project Overview

data engineering pipeline that simulates real-world log analytics using MongoDB, Apache Airflow, and Python. This project demonstrates a complete ETL workflow following industry best practices, from data generation through transformation to visualization and automated orchestration.
The pipeline processes synthetic application logs (user activities, events, errors) and transforms them into actionable insights through aggregations and visualizations, mimicking real-world scenarios such as user behavior tracking, performance monitoring, or sales analytics.

## Business Case

Organizations need to analyze large volumes of log data to:

Monitor user behavior across different countries and devices
Track application events (logins, purchases, errors) in real-time
Identify trends and anomalies in system usage
Generate reports for stakeholders with visual analytics

This pipeline automates the entire process, from data collection to insight generation, reducing manual effort and enabling data-driven decision-making.

## Pipeline Stages:

### 1. Log Generation (generate_logs.py)

- Creates synthetic log data using Faker library

- Simulates user events: login, logout, purchase, error, click, view

- Includes metadata: IP address, device type, country

- Stores raw logs in MongoDB


### 2. ETL Process (etl.py)

- Extract: Retrieves raw logs from MongoDB

- Transform: Cleans data, extracts date/time, flattens nested fields

- Aggregate: Groups events by date, country, and event type

- Load: Performs upsert operations to MongoDB daily summary collection


### 3. Analysis & Visualization (analysis.py)

#### Generates 5 types of analytical charts:

- Events by type (bar chart)

- Top 10 countries by activity (horizontal bar)

- Events over time (line chart)

- Event distribution by top countries (stacked bar)

- Events heatmap (date vs event type)

- Exports summary statistics to CSV files


### 4. Orchestration (log_pipeline_dag.py)

- Apache Airflow DAG schedules pipeline execution

- Runs hourly with automatic retries

- Ensures sequential task dependencies