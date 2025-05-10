# Apache Hive Project Documentation

## Overview

This project demonstrates the setup, configuration, and operation of Apache Hive running atop a Hadoop cluster in a containerized environment. The system is optimized for distributed processing, automated data extraction, incremental loading, and periodic data transformations.

## Project Components

### Infrastructure Setup

* **Apache Hive on Hadoop Cluster:** Established a fully operational Apache Hive environment leveraging Hadoop for data storage and distributed computation.
* **Multi-stage Dockerfile:** Created Dockerfiles for streamlined deployment of both Hadoop and Hive services.
* **Service Orchestration:** Utilized `docker-compose.yml` for orchestrating Namenodes, Datanodes, Hive Server2, Hive Metastore, and PostgreSQL.

### Configuration

* **Execution Engine:** Set Apache Hive's execution engine to `Tez` for optimized performance.
* **Hive Metastore:** Configured remote metastore using PostgreSQL for better scalability and metadata management.
* **Environment and Networking:** Defined proper environment variables, volume mappings, Docker networks, port mappings, and dependencies.
* **Hive and Tez Configuration:** Managed configurations in `hive-site.xml` and `tez-site.xml` to optimize Hive execution and resource allocation.

### Data Handling

* **Data Migration:** Migrated historical DWH data to HDFS as CSV files and loaded transactional PostgreSQL data periodically.
* **Incremental Loading:** Implemented a Python-based ELT script to incrementally load transactional data into Hive.
* **Staging Area:** Loaded data initially to a staging schema on HDFS, then transformed it into Hive optimized schemas.

### ETL and ELT Automation

* **Python ELT Script:** Developed and deployed Python scripts to automate data extraction from PostgreSQL and incremental loading into Hive.
* **Scheduled Automation:** Utilized `crontab` to schedule:

  * SQL transformation scripts on Hive server.
  * Python incremental load scripts locally.

### Schema and Table Optimization


![Fact_Reservation](https://github.com/TmohamedashrafT/Airline-DWH/blob/main/drawio%20schema/fact_reservation.drawio.png)

### Columns  

#### Foreign Keys (Dimensional References)  
These columns link to various dimension tables to provide detailed contextual information.  

| Column Name              | Data Type      | Description                                          | Reference Dimension |
|--------------------------|---------------|------------------------------------------------------|----------------------|
| `Reservation_Key`        | NUMBER(10) (PK) | Unique identifier for each reservation record.       | - |
| `ticket_id`             | NUMBER(10)     | Unique identifier for the ticket.                   | - |
| `channel_key`           | NUMBER(10)     | Booking channel used for the reservation.           | `dim_channel` |
| `promotion_key`         | NUMBER(10)     | Promotion applied to the reservation.               | `dim_promotion` (if applicable) |
| `passenger_key`         | NUMBER(10)     | Passenger associated with the reservation.          | `dim_passenger` |
| `fare_basis_key`        | NUMBER(10)     | Fare classification for the reservation.            | `dim_fare_basis` |
| `aircraft_key`          | NUMBER(10)     | Aircraft used for the flight.                       | `dim_aircraft` |
| `source_airport`        | NUMBER(10)     | Departure airport.                                  | `dim_airport` |
| `destination_airport`   | NUMBER(10)     | Arrival airport.                                    | `dim_airport` |

#### Date and Time Attributes  
These attributes provide insights into reservation and flight schedules.  

| Column Name              | Data Type      | Description                                          | Reference Dimension |
|--------------------------|---------------|------------------------------------------------------|----------------------|
| `reservation_date_key`   | NUMBER(8)     | Date when the reservation was made.                 | `dim_date` |
| `departure_date_key`     | NUMBER(8)     | Scheduled departure date of the flight.             | `dim_date` |
| `departure_time`         | TIMESTAMP     | Exact departure time of the flight.                 | - |
| `Reservation_timestamp`  | TIMESTAMP     | Timestamp when the reservation was created.         | - |

#### Reservation Details  

| Column Name              | Data Type      | Description                                          |
|--------------------------|---------------|------------------------------------------------------|
| `payment_method`         | STRING  | Payment method used for the reservation.            |
| `seat_no`               | STRING  | Seat assigned to the passenger.                     |
| `Is_Cancelled`          | NUMBER(1)     | Indicates if the reservation was canceled (0 = No, 1 = Yes). |

#### Measures & Calculations  

These numeric attributes are used for financial analysis and revenue tracking.  

| Column Name          | Data Type      | Description                                              | Calculation |
|----------------------|---------------|----------------------------------------------------------|-------------|
| `Promotion_Amount`  | NUMBER(10,2)  | Discount applied to the reservation.                    | - |
| `tax_amount`        | NUMBER(10,2)  | Tax amount added to the ticket price.                   | - |
| `Operational_Fees`  | NUMBER(10,2)  | Additional fees for operations (e.g., service fees).    | - |
| `Cancelation_Fees`  | NUMBER(10,2)  | Fees applied if the reservation is canceled.            | - |
| `Fare_Price`        | NUMBER(10,2)  | Base fare price of the ticket.                          | - |
| `Final_Price`       | NUMBER(10,2)  | Total price paid by the passenger.                      | `if Is_cancelled == 0: Final_price = Fare_Price + Operational_Fees + tax_amount - Promotion_Amount else: Final_price = Cancelation_Fees` |

### Usage  
- Supports revenue analysis and pricing optimization.  
- Helps in understanding passenger booking patterns and channel preferences.  
- Tracks the impact of promotions and cancellation fees on overall revenue.  
- Provides insights into reservation trends and seat allocation efficiency.


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

# Fact Flight Reservations Bigtable

## Overview
The `fact_flight_reservations_bigtable` table serves as a denormalized fact table, consolidating flight reservation data enriched with passenger, promotion, airport, fare, and channel information. Designed for analytical workloads, it supports partitioning and bucketing to optimize query performance.

### Storage Details
- **Storage Format:** Parquet
- **Partitioned By:** `reservation_year`, `reservation_month`
- **Clustered By:** `passenger_id` into 32 buckets
- **Location:** `/data/airline/analytics/reservations_bigtable`

### Table Properties

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| booking_class | STRING | Booking class code (e.g., Economy, Business). |
| seat_number | STRING | Assigned seat number for the passenger. |
| is_cancelled | BOOLEAN | Indicates if the reservation was canceled. |
| cancellation_reason | STRING | Reason provided for cancellation, if any. |

### Passenger Details
| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| passenger_id | STRING | Unique identifier for the passenger. |
| passenger_name | STRING | Full name of the passenger. |
| passenger_dob | DATE | Date of birth of the passenger. |
| passenger_nationality | STRING | Nationality of the passenger. |
| passenger_gender | STRING | Gender of the passenger. |
| frequent_flyer_tier | STRING | Frequent flyer tier status. |

### Fare and Promotion Details
| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| fare_basis_code | STRING | Fare basis code for the ticket. |
| fare_class | STRING | Fare class category. |
| refundable | BOOLEAN | Indicates if the ticket is refundable. |
| baggage_allowance | STRING | Baggage allowance associated with the fare. |
| promotion_name | STRING | Name of the applied promotion. |
| promotion_type | STRING | Type/category of the promotion. |
| discount_value | DECIMAL(10,2) | Monetary value of the discount. |
| discount_type | STRING | Type of discount (e.g., percentage, fixed). |


## Data Lineage and Transformation
Data for the `fact_flight_reservations_bigtable` table is sourced and transformed through a series of joins and mappings:

### Source Tables:
- `dwh_staging.fact_reservations` (fact table)
- `scd_passengers` (slowly changing dimension for passengers)
- `scd_promotions` (slowly changing dimension for promotions)
- `dwh_staging.dim_airports` (airport dimension)
- `dwh_staging.dim_fare_basis_codes` (fare basis dimension)
- `dwh_staging.dim_sales_channels` (sales channel dimension)
- `dwh_staging.dim_date` (date dimension)

### Transformation Logic:
- Joins are performed to enrich reservation data with passenger, promotion, airport, fare, and channel details
- Date keys are mapped to actual dates using the date dimension
- Calculated fields such as `final_price` are derived based on business rules (e.g., applying promotions, taxes, and fees)

## Usage and Analytical Applications
The `fact_flight_reservations_bigtable` table is designed to support various analytical use cases:

- **Revenue Analysis:** Evaluate revenue streams by analyzing fare prices, taxes, operational fees, and discounts
- **Customer Insights:** Understand passenger demographics, booking behaviors, and loyalty tier distributions
- **Promotion Effectiveness:** Assess the impact of different promotions on sales and customer acquisition
- **Operational Efficiency:** Monitor cancellation rates, reasons, and associated fees to improve operational strategies
- **Market Trends:** Analyze booking patterns across different regions, channels, and time periods to identify market trends


```bash
sudo service cron start

echo export PATH=/usr/local/hive/bin:/usr/local/hadoop/bin:/usr/bin:/bin >> /app/hive_cron.sh
echo "beeline -u jdbc:hive2://localhost:10000 -n hive -p hive -f /app/test.sql >> /app/hive_cron.log 2>&1" >> /app/hive_cron.sh

echo "* 2 * * * /app/hive_cron.sh" | crontab -
```

### Local Host (Python ELT)

```bash
* 2 * * * export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin && cd /Users/mohamedmoaaz/Desktop/hive/hadoop/scripts && /usr/local/bin/python3 to_source_staging.py >> /Users/mohamedmoaaz/Desktop/output.log 2>&1
```

## Conclusion

This comprehensive project setup provides an efficient, reliable, and scalable solution for data warehousing using Apache Hive, facilitating both batch and incremental data processing workflows.
