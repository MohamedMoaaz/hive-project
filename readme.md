# Airline Data Warehouse (DWH) Project

---

## 🚀 Overview

This project implements a robust Airline Data Warehouse (DWH) solution using Apache Hive atop a distributed Hadoop cluster. Designed for scalability, flexibility, and performance, it covers the complete lifecycle of data processing—from extraction and transformation to analytical querying.

The project focuses primarily on the **fact\_flight\_reservations\_bigtable**, a denormalized fact table optimized for complex analytical workloads, providing insights into revenue streams, customer behavior, promotion effectiveness, and operational efficiency.

---

## 📚 Table of Contents

* [Infrastructure Setup](#infrastructure-setup)
* [Configuration](#configuration)
* [Data Handling](#data-handling)
* [ETL and ELT Automation](#etl-and-elt-automation)
* [Schema and Table Optimization](#schema-and-table-optimization)
* [Data Validation and Consistency](#data-validation-and-consistency)
* [Scheduled Task Setup](#scheduled-task-setup)

  * [Hive Server (Transformations)](#hive-server-transformations)
  * [Local Host (Python ELT)](#local-host-python-elt)
* [Conclusion](#conclusion)

---

## 🛠 Infrastructure Setup

* **Apache Hive & Hadoop:** Fully operational Hive environment leveraging Hadoop's distributed capabilities.
* **Docker Containers:** Multi-stage Dockerfiles ensure consistent and reproducible environments.
* **Service Orchestration:** Docker Compose setup for Namenodes, Datanodes, Hive Server2, Hive Metastore, and PostgreSQL.

---

## ⚙️ Configuration

* **Execution Engine:** Apache Tez for optimized Hive query performance.
* **Remote Metastore:** PostgreSQL backend for efficient metadata management.
* **Networking & Environment:** Comprehensive configurations in `hive-site.xml` and `tez-site.xml`.

---

## 📥 Data Handling

* **Migration & Incremental Loading:** Historical data migration via CSV to HDFS, and periodic incremental loading from PostgreSQL using Python scripts.
* **Staging Schema:** Initial loading into staging areas on HDFS before transformation into optimized Hive schemas.

---

## 🔄 ETL and ELT Automation

* **Python ELT Script:** Automates extraction from PostgreSQL and incremental data loading.
* **Scheduled Automation:** Using `crontab` for automated data pipeline tasks.

---

## 📊 Schema and Table Optimization

### **Fact Flight Reservations Bigtable**

* **Format:** ORC with Snappy Compression
* **Partitioning:** Year, Month
* **Bucketing:** Passenger ID (32 buckets)
* **Location:** `/data/airline/analytics/reservations_bigtable`

### **Dimensional References**

| Column Name           | Data Type  | Reference        |
| --------------------- | ---------- | ---------------- |
| `Reservation_Key`     | NUMBER(10) | -                |
| `ticket_id`           | NUMBER(10) | -                |
| `channel_key`         | NUMBER(10) | `dim_channel`    |
| `promotion_key`       | NUMBER(10) | `dim_promotion`  |
| `passenger_key`       | NUMBER(10) | `dim_passenger`  |
| `fare_basis_key`      | NUMBER(10) | `dim_fare_basis` |
| `aircraft_key`        | NUMBER(10) | `dim_aircraft`   |
| `source_airport`      | NUMBER(10) | `dim_airport`    |
| `destination_airport` | NUMBER(10) | `dim_airport`    |

### **Reservation & Temporal Attributes**

* Key date fields linked to `dim_date`
* Financial metrics for revenue and operational analysis

---

## ✅ Data Validation and Consistency

Rigorous data validation checks post-transformations ensure accuracy and integrity.

---

## 🕒 Scheduled Task Setup

### **Hive Server (Transformations)**

Setup transformations to run daily at 2 AM:

```bash
sudo service cron start

# Create transformation script
cat << EOF > /app/hive_cron.sh
export PATH=/usr/local/hive/bin:/usr/local/hadoop/bin:/usr/bin:/bin
beeline -u jdbc:hive2://localhost:10000 -n hive -p hive -f /app/test.sql >> /app/hive_cron.log 2>&1
EOF

# Schedule task
(crontab -l 2>/dev/null; echo "0 2 * * * /app/hive_cron.sh") | crontab -
```

### **Local Host (Python ELT)**

Python ELT script scheduled daily at 2 AM:

```bash
(crontab -l 2>/dev/null; echo "0 2 * * * export PATH=/usr/local/bin:/usr/bin:/bin && cd /Users/mohamedmoaaz/Desktop/hive/hadoop/scripts && /usr/local/bin/python3 to_source_staging.py >> /Users/mohamedmoaaz/Desktop/output.log 2>&1") | crontab -
```

---

## 🧩 Data Lineage and Transformation

Source tables joined and mapped to enrich reservation data with dimensional attributes:

* `fact_reservations`
* `scd_passengers`
* `scd_promotions`
* `dim_airports`
* `dim_fare_basis_codes`
* `dim_sales_channels`
* `dim_date`

Calculated fields such as `final_price` derived based on defined business rules.

---

## 🎯 Analytical Applications

* **Revenue Analysis:** Analyze revenue trends from detailed financial metrics.
* **Customer Insights:** Assess booking patterns and demographics.
* **Promotion Effectiveness:** Evaluate promotional strategies.
* **Operational Efficiency:** Optimize cancellation and fee structures.
* **Market Trends:** Identify market trends through temporal and regional analytics.

---

## 🚩 Conclusion

This comprehensive Airline Data Warehouse solution offers robust, scalable, and optimized data warehousing capabilities using Apache Hive, effectively supporting both incremental and batch data processing workflows in a structured and maintainable framework.
