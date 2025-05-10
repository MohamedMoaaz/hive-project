# 🚀 Apache Hive Project Documentation

## 📖 Overview

This project demonstrates the setup, configuration, and operation of Apache Hive running atop a Hadoop cluster in a containerized environment. The system is optimized for distributed processing, automated data extraction, incremental loading, and periodic data transformations.

---

## 🛠️ Project Components

### 🌐 Infrastructure Setup

* **🐝 Apache Hive on Hadoop Cluster:** Established a fully operational Apache Hive environment leveraging Hadoop for data storage and distributed computation.
* **🐳 Multi-stage Dockerfile:** Created Dockerfiles for streamlined deployment of both Hadoop and Hive services.
* **🎛️ Service Orchestration:** Utilized `docker-compose.yml` for orchestrating Namenodes, Datanodes, Hive Server2, Hive Metastore, and PostgreSQL.

---

### ⚙️ Configuration

* **🚂 Execution Engine:** Set Apache Hive's execution engine to `Tez` for optimized performance.
* **📚 Hive Metastore:** Configured remote metastore using PostgreSQL for better scalability and metadata management.
* **🌍 Environment and Networking:** Defined proper environment variables, volume mappings, Docker networks, port mappings, and dependencies.
* **📜 Hive and Tez Configuration:** Managed configurations in `hive-site.xml` and `tez-site.xml` to optimize Hive execution and resource allocation.

---

### 📁 Data Handling

* **📤 Data Migration:** Migrated historical DWH data to HDFS as CSV files and loaded transactional PostgreSQL data periodically.
* **🔄 Incremental Loading:** Implemented a Python-based ELT script to incrementally load transactional data into Hive.
* **🛬 Staging Area:** Loaded data initially to a staging schema on HDFS, then transformed it into Hive optimized schemas.

---

### 🤖 ETL and ELT Automation

* **🐍 Python ELT Script:** Developed and deployed Python scripts to automate data extraction from PostgreSQL and incremental loading into Hive.
* **📅 Scheduled Automation:** Utilized `crontab` to schedule:

  * SQL transformation scripts on Hive server.
  * Python incremental load scripts locally.

---

### 📊 Schema and Table Optimization

![Fact\_Reservation](https://github.com/TmohamedashrafT/Airline-DWH/blob/main/drawio%20schema/fact_reservation.drawio.png)

### 🔑 Columns

#### Foreign Keys (Dimensional References)

| Column Name          | Data Type       | Description                                    | Reference Dimension            |
| -------------------- | --------------- | ---------------------------------------------- | ------------------------------ |
| Reservation\_Key     | NUMBER(10) (PK) | Unique identifier for each reservation record. | -                              |
| ticket\_id           | NUMBER(10)      | Unique identifier for the ticket.              | -                              |
| channel\_key         | NUMBER(10)      | Booking channel used for the reservation.      | dim\_channel                   |
| promotion\_key       | NUMBER(10)      | Promotion applied to the reservation.          | dim\_promotion (if applicable) |
| passenger\_key       | NUMBER(10)      | Passenger associated with the reservation.     | dim\_passenger                 |
| fare\_basis\_key     | NUMBER(10)      | Fare classification for the reservation.       | dim\_fare\_basis               |
| aircraft\_key        | NUMBER(10)      | Aircraft used for the flight.                  | dim\_aircraft                  |
| source\_airport      | NUMBER(10)      | Departure airport.                             | dim\_airport                   |
| destination\_airport | NUMBER(10)      | Arrival airport.                               | dim\_airport                   |

#### 📅 Date and Time Attributes

| Column Name            | Data Type | Description                                 | Reference Dimension |
| ---------------------- | --------- | ------------------------------------------- | ------------------- |
| reservation\_date\_key | NUMBER(8) | Date when the reservation was made.         | dim\_date           |
| departure\_date\_key   | NUMBER(8) | Scheduled departure date of the flight.     | dim\_date           |
| departure\_time        | TIMESTAMP | Exact departure time of the flight.         | -                   |
| Reservation\_timestamp | TIMESTAMP | Timestamp when the reservation was created. | -                   |

#### 📋 Reservation Details

| Column Name     | Data Type | Description                                                  |
| --------------- | --------- | ------------------------------------------------------------ |
| payment\_method | STRING    | Payment method used for the reservation.                     |
| seat\_no        | STRING    | Seat assigned to the passenger.                              |
| Is\_Cancelled   | NUMBER(1) | Indicates if the reservation was canceled (0 = No, 1 = Yes). |

#### 📈 Measures & Calculations

| Column Name       | Data Type    | Description                                          | Calculation                             |
| ----------------- | ------------ | ---------------------------------------------------- | --------------------------------------- |
| Promotion\_Amount | NUMBER(10,2) | Discount applied to the reservation.                 | -                                       |
| tax\_amount       | NUMBER(10,2) | Tax amount added to the ticket price.                | -                                       |
| Operational\_Fees | NUMBER(10,2) | Additional fees for operations (e.g., service fees). | -                                       |
| Cancelation\_Fees | NUMBER(10,2) | Fees applied if the reservation is canceled.         | -                                       |
| Fare\_Price       | NUMBER(10,2) | Base fare price of the ticket.                       | -                                       |
| Final\_Price      | NUMBER(10,2) | Total price paid by the passenger.                   | Calculated based on cancellation status |

---

### 🗂️ Usage

* Supports revenue analysis and pricing optimization.
* Helps in understanding passenger booking patterns and channel preferences.
* Tracks the impact of promotions and cancellation fees on overall revenue.
* Provides insights into reservation trends and seat allocation efficiency.

---

### 🗃️ Hive Schema

#### 🔑 Foreign Keys (Dimensional References)

| Column Name          | Data Type       | Description                                    | Reference Dimension            |
| -------------------- | --------------- | ---------------------------------------------- | ------------------------------ |
| Reservation\_Key     | NUMBER(10) (PK) | Unique identifier for each reservation record. | -                              |
| ticket\_id           | NUMBER(10)      | Unique identifier for the ticket.              | -                              |
| channel\_key         | NUMBER(10)      | Booking channel used for the reservation.      | dim\_channel                   |
| promotion\_key       | NUMBER(10)      | Promotion applied to the reservation.          | dim\_promotion (if applicable) |
| passenger\_key       | NUMBER(10)      | Passenger associated with the reservation.     | dim\_passenger                 |
| fare\_basis\_key     | NUMBER(10)      | Fare classification for the reservation.       | dim\_fare\_basis               |
| aircraft\_key        | NUMBER(10)      | Aircraft used for the flight.                  | dim\_aircraft                  |
| source\_airport      | NUMBER(10)      | Departure airport.                             | dim\_airport                   |
| destination\_airport | NUMBER(10)      | Arrival airport.                               | dim\_airport                   |

#### 📅 Date and Time Attributes

| Column Name            | Data Type | Description                                 | Reference Dimension |
| ---------------------- | --------- | ------------------------------------------- | ------------------- |
| reservation\_date\_key | NUMBER(8) | Date when the reservation was made.         | dim\_date           |
| departure\_date\_key   | NUMBER(8) | Scheduled departure date of the flight.     | dim\_date           |
| departure\_time        | TIMESTAMP | Exact departure time of the flight.         | -                   |
| reservation\_timestamp | TIMESTAMP | Timestamp when the reservation was created. | -                   |

#### 📋 Reservation Details

| Column Name     | Data Type | Description                                                  |
| --------------- | --------- | ------------------------------------------------------------ |
| payment\_method | STRING    | Payment method used for the reservation.                     |
| seat\_no        | STRING    | Seat assigned to the passenger.                              |
| Is\_Cancelled   | NUMBER(1) | Indicates if the reservation was canceled (0 = No, 1 = Yes). |

#### 📈 Measures & Calculations

| Column Name       | Data Type    | Description                                          | Calculation                             |
| ----------------- | ------------ | ---------------------------------------------------- | --------------------------------------- |
| Promotion\_Amount | NUMBER(10,2) | Discount applied to the reservation.                 | -                                       |
| tax\_amount       | NUMBER(10,2) | Tax amount added to the ticket price.                | -                                       |
| Operational\_Fees | NUMBER(10,2) | Additional fees for operations (e.g., service fees). | -                                       |
| Cancelation\_Fees | NUMBER(10,2) | Fees applied if the reservation is canceled.         | -                                       |
| Fare\_Price       | NUMBER(10,2) | Base fare price of the ticket.                       | -                                       |
| Final\_Price      | NUMBER(10,2) | Total price paid by the passenger.                   | Calculated based on cancellation status |

---

### 🗂️ Usage

* 📊 Supports revenue analysis and pricing optimization.
* 📈 Helps in understanding passenger booking patterns and channel preferences.
* 💸 Tracks the impact of promotions and cancellation fees on overall revenue.
* 🧑‍✈️ Provides insights into reservation trends and seat allocation efficiency.

---

### 🔍 Advanced Optimization Strategies

* 📄 **Hive Schema:** Designed scalable schema optimized for distributed querying and analytics.
* 🗃️ **ORC File Format:** Chose ORC files for efficient storage, compression, and improved query performance.
* 🔒 **ACID Compliance:** Implemented Slowly Changing Dimensions (SCD) as ACID-compliant tables.
* 📦 **Non-ACID Tables:** Managed larger, denormalized Hive tables optimized for query performance.
* 📌 **Partitioning Strategy:** Optimized for query performance and data management.
* 🗃️ **Bucketing Strategy:** Chose bucketing to evenly distribute data across buckets for efficient joins and aggregations.
* 🗜️ **Compression (Snappy):** Selected for balance between compression ratio and speed.
* **Hive Schema:** Designed a scalable schema optimized for distributed querying and analytics.


* **File Format (ORC):** Chose ORC (Optimized Row Columnar) files because they are highly compatible with Hive. ORC format provides efficient storage, compression, and improved query performance due to built-in indexing and statistics.

* **ACID Compliance:** Implemented Slowly Changing Dimensions (SCD) as ACID-compliant tables in Hive, supporting transactional operations such as row-level updates, deletes, and inserts, essential for managing slowly changing dimension data.

* **Non-ACID Tables:** Managed larger, denormalized Hive tables optimized for query performance and minimal complexity. Non-ACID tables are suitable for data that doesn't require frequent updates or transactional consistency.

* **Partitioning Strategy:**

  * **Big Tables:** Partitioned by year and month to enhance query performance by enabling efficient pruning, minimizing data scanning, and optimizing resource utilization.
  * **Passenger Dimension (ACID Table):** Partitioned by passenger frequent flyer tier, ensuring fast lookups and updates based on customer loyalty categories.
  * **Promotions (ACID Table):** Partitioned by promotion type, allowing efficient management and queries related to promotional analytics.

* **Bucketing Strategy:** Chose bucketing on passenger ID for both the big table and passenger dimension to evenly distribute data across buckets, facilitating efficient joins, aggregations, and data sampling.

* **Compression (Snappy):** Selected Snappy compression for compaction because it provides a balance between compression ratio and processing speed, reducing storage costs and enhancing query performance without significant CPU overhead.

### Data Validation and Consistency

* Performed rigorous data validation checks to ensure consistency and correctness post-transformation.

## Scheduled Task Setup

### Hive Server (Transformations)

# Fact Flight Reservations Bigtable

## Overview
The `fact_flight_reservations_bigtable` table serves as a denormalized fact table, consolidating flight reservation data enriched with passenger, promotion, airport, fare, and channel information. Designed for analytical workloads, it supports partitioning and bucketing to optimize query performance.

### Storage Details
- **Storage Format:** Parquet
- **Partitioned By:** `reservation_year`, `reservation_month`
- **Clustered By:** `passenger_id` into 32 buckets
- **Location:** `/data/airline/analytics/reservations_bigtable`

---

### ✅ Data Validation and Consistency

Performed rigorous data validation checks to ensure consistency and correctness post-transformation.

---

## 📅 Scheduled Task Setup

### 📌 Hive Server (Transformations)

Scheduled SQL transformation scripts via Hive Server.

```bash
sudo service cron start
echo export PATH=/usr/local/hive/bin:/usr/local/hadoop/bin:/usr/bin:/bin >> /app/hive_cron.sh
echo "beeline -u jdbc:hive2://localhost:10000 -n hive -p hive -f /app/test.sql >> /app/hive_cron.log 2>&1" >> /app/hive_cron.sh
echo "* 2 * * * /app/hive_cron.sh" | crontab -
```

### 🖥️ Local Host (Python ELT)

Scheduled Python scripts locally.

```bash
* 2 * * * export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin && cd /path/to/scripts && python3 script.py >> /path/to/output.log 2>&1
```

---

## 🎯 Conclusion

This comprehensive project setup provides an efficient, reliable, and scalable solution for data warehousing using Apache Hive, facilitating both batch and incremental data processing workflows.
