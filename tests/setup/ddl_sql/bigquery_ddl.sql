DROP TABLE IF EXISTS EXTERNAL_DATA.ADDRESS_REGION_ATTRIBUTES;
create or replace TABLE EXTERNAL_DATA.ADDRESS_REGION_ATTRIBUTES (
	ID NUMERIC,
	ADDRESS_ID NUMERIC,
	SALES_REGION STRING,
	PRIMARY_REGIONAL_CREDIT_PROVIDER STRING,
	IS_CURRENTLY_TARGETED BOOLEAN
);

DROP TABLE IF EXISTS EXTERNAL_DATA.SOCIAL_USERS_IMPORT;
create or replace TABLE EXTERNAL_DATA.SOCIAL_USERS_IMPORT (
	ID NUMERIC,
	EMAIL STRING,
	SOCIAL_SITE_USERNAME STRING,
	PRIMARY_BROWSER_AGENT STRING,
	SPIRIT_ANIMAL STRING,
	SOURCE_SYSTEM_USER_ID NUMERIC
);

DROP TABLE IF EXISTS SOURCE_SYSTEM.ORDERS;
create or replace TABLE SOURCE_SYSTEM.ORDERS (
	ID NUMERIC,
	USER_ID NUMERIC,
	SHIPPED_DATE STRING,
	DISCOUNT_CODES STRING
);

DROP TABLE IF EXISTS SOURCE_SYSTEM.ORDER_ITEMS;
create or replace TABLE SOURCE_SYSTEM.ORDER_ITEMS (
	ID NUMERIC,
	QUANTITY NUMERIC,
	ORDER_ID NUMERIC,
	PRODUCT_ID NUMERIC
);

DROP TABLE IF EXISTS SOURCE_SYSTEM.PRODUCTS;
create or replace TABLE SOURCE_SYSTEM.PRODUCTS (
	ID NUMERIC,
	PRODUCT_NAME STRING,
	MANUFACTURER STRING,
	UNIT_WEIGHT_LBS FLOAT64,
	SHIPPING_BOX_COLOR_CODE STRING,
	COST_USD FLOAT64
);

DROP TABLE IF EXISTS SOURCE_SYSTEM.USERS;
create or replace TABLE SOURCE_SYSTEM.USERS (
	ID NUMERIC,
	FIRST_NAME STRING,
	LAST_NAME STRING,
	EMAIL STRING,
	GENDER STRING,
	CREATED_AT STRING,
	MEMBER_STATUS_TYPE STRING
);

DROP TABLE IF EXISTS SOURCE_SYSTEM.USER_ADDRESSES;
create or replace TABLE SOURCE_SYSTEM.USER_ADDRESSES (
	ID NUMERIC,
	ADDRESS_LINE_ONE STRING,
	ADDRESS_LINE_TWO STRING,
	CITY STRING,
	STATE STRING,
	ZIPCODE NUMERIC,
	USER_ID NUMERIC
);

DROP TABLE IF EXISTS SOURCE_SYSTEM.USER_COOKIES;
create or replace TABLE SOURCE_SYSTEM.USER_COOKIES (
	ID NUMERIC,
	COOKIE_ID STRING,
	USER_ID NUMERIC
);

DROP TABLE IF EXISTS TESTS_DATA.CASE_TESTING;
create or replace TABLE TESTS_DATA.CASE_TESTING (
	UPPER_COL STRING,
	`QUOTED_UPPER_COL` STRING,
	`lower_col` STRING,
	`CamelCasedCol` STRING,
	`Snake_Case_Camel_Col` STRING,
	`Spaces_Col` STRING --bigquery does not support spaces in identifiers
);

DROP TABLE IF EXISTS TESTS_DATA.DATA_TYPES;
CREATE OR REPLACE TABLE TESTS_DATA.DATA_TYPES (
	ARRAY_COL ARRAY<NUMERIC>,
	BIGINT_COL NUMERIC,
	BINARY_COL BYTES,
	BOOLEAN_COL BOOL,
	CHAR_COL STRING,
	CHARACTER_COL STRING,
	DATE_COL DATE,
	DATETIME_COL DATETIME,
	DECIMAL_COL NUMERIC,
	DOUBLE_COL FLOAT64,
	DOUBLEPRECISION_COL FLOAT64,
	FLOAT_COL FLOAT64,
	FLOAT4_COL FLOAT64,
	FLOAT8_COL FLOAT64,
	INT_COL INT64,
	INTEGER_COL NUMERIC,
	NUMBER_COL NUMERIC,
	NUMERIC_COL NUMERIC,
	OBJECT_COL STRUCT<col_1 STRING>,
	REAL_COL FLOAT64,
	SMALLINT_COL NUMERIC,
	STRING_COL STRING,
	TEXT_COL STRING,
	TIME_COL TIME,
	TIMESTAMP_COL TIMESTAMP,
	TIMESTAMP_NTZ_COL DATETIME,
	TIMESTAMP_LTZ_COL TIMESTAMP,
	TIMESTAMP_TZ_COL TIMESTAMP,
	VARBINARY_COL BYTES,
	VARCHAR_COL STRING,
	VARIANT_COL STRUCT<event STRUCT<id INT64, val STRING>>
);

CREATE OR REPLACE VIEW `snowshu-development`.SOURCE_SYSTEM.ADDRESSES_VIEW as
SELECT * FROM `snowshu-development`.SOURCE_SYSTEM.USER_ADDRESSES LIMIT 100;

CREATE OR REPLACE VIEW `snowshu-development`.SOURCE_SYSTEM.ORDER_ITEMS_VIEW as 
    SELECT * FROM `snowshu-development`.SOURCE_SYSTEM.ORDER_ITEMS;

CREATE OR REPLACE VIEW `snowshu-development`.SOURCE_SYSTEM.ORDER_ITEMS_VIEW as 
    SELECT * FROM `snowshu-development`.SOURCE_SYSTEM.ORDER_ITEMS;