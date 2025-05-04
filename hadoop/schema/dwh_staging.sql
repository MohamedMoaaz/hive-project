CREATE EXTERNAL TABLE fact_reservation (
    ticket_id               STRING,
    channel_key             INT,
    promotion_key           INT,
    passenger_key           INT,
    fare_basis_key          INT,
    aircraft_key            INT,
    source_airport          INT,
    destination_airport     INT,
    reservation_date_key    INT,  
    departure_date_key      INT,
    booking_class           STRING,
    seat_number             STRING,
    Promotion_Amount        DECIMAL(10,2),
    tax_amount              DECIMAL(10,2),
    Operational_Fees        DECIMAL(10,2),
    Cancelation_Fees        DECIMAL(10,2),
    Fare_Price              DECIMAL(10,2),
    Final_Price             DECIMAL(10,2),
    is_cancelled            BOOLEAN,
    cancellation_reason     STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/fact_reservation';

CREATE EXTERNAL TABLE dim_passenger (
    passenger_key           INT,
    passenger_id            STRING,
    passenger_national_id   STRING,
    passenger_firstname     STRING,
    passenger_lastname      STRING,
    passenger_dob           DATE,
    passenger_nationality   STRING,
    passenger_email         STRING,
    passenger_phoneno       STRING,
    passenger_gender        STRING,
    passenger_status        STRING,
    frequent_flyer_tier     STRING,
    effective_date          DATE,
    expiry_date             DATE,
    is_current              BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/dim_passenger';

CREATE EXTERNAL TABLE dim_promotions (
    promotion_key           INT,
    promotion_id           STRING,
    promotion_name         STRING,
    promotion_type         STRING,
    promotion_target_segment STRING,
    promotion_channel      STRING,
    promotion_start_date   DATE,
    promotion_end_date     DATE,
    discount_value         DECIMAL(10,2),
    discount_type          STRING,
    max_discount_amount    DECIMAL(10,2),
    effective_date         DATE,
    expiry_date            DATE,
    is_current             BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/dim_promotions';

CREATE EXTERNAL TABLE dim_airport (
    airport_key            INT,
    airport_id             STRING,
    airport_name           STRING,
    airport_code           STRING,
    airport_city           STRING,
    airport_country        STRING,
    airport_region         STRING,
    airport_timezone       STRING,
    airport_latitude       DOUBLE,
    airport_longitude      DOUBLE,
    airport_no_of_runways  INT,
    airport_size_category  STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/dim_airport';

CREATE EXTERNAL TABLE dim_fare_basis (
    fare_basis_key         INT,
    fare_basis_code        STRING,
    fare_class             STRING,
    refundable             BOOLEAN,
    changeable             BOOLEAN,
    fare_description       STRING,  
    baggage_allowance      STRING,
    meal_included          BOOLEAN,
    upgrade_eligible       BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/dim_fare_basis';

CREATE EXTERNAL TABLE dim_channel (
    channel_key            INT,
    channel_name          STRING,
    channel_type          STRING,
    channel_category      STRING,
    commission_rate       DECIMAL(5,2),
    is_active             BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/dim_channel';

CREATE EXTERNAL TABLE dim_aircraft (
    aircraft_key           INT,
    aircraft_model        STRING,
    aircraft_manufacturer STRING,
    aircraft_capacity     INT,
    economy_seats         INT,
    business_seats        INT,
    firstclass_seats      INT,
    aircraft_age          INT,
    fuel_efficiency       DECIMAL(5,2),
    maintenance_status    STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/dim_aircraft';

CREATE EXTERNAL TABLE dim_date (
    date_key               INT,
    full_date              DATE,
    day_number             INT,
    day_name               STRING,
    month_name             STRING,
    year_no                INT,
    quarter                INT,
    week_of_year           INT,
    is_weekend             BOOLEAN,
    is_holiday             BOOLEAN,
    holiday_name           STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/staging/migrated/dim_date';