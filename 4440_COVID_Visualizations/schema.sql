-- SHOW PROCESSLIST;
DROP DATABASE IF EXISTS covid_db;
CREATE DATABASE IF NOT EXISTS covid_db;
USE covid_db;
SET GLOBAL local_infile = 1;

DROP TABLE IF EXISTS COUNTY_POPULATION;
CREATE TABLE COUNTY_POPULATION(
	county VARCHAR(35) NOT NULL,
    state_name VARCHAR(15) NOT NULL,
    fips_code VARCHAR(15) NOT NULL,
	population INT NOT NULL,
    area INT NOT NULL,
    density INT NOT NULL,
    PRIMARY KEY (state_name, county)
);

DROP TABLE IF EXISTS STATE_POPULATION;
CREATE TABLE STATE_POPULATION(
	state_name VARCHAR(15) NOT NULL,
    state_population INT NOT NULL,
    PRIMARY KEY (state_name)
);

DROP TABLE IF EXISTS COUNTY_INFECTIONS;
CREATE TABLE COUNTY_INFECTIONS(
	submission_date DATE NOT NULL, 
    county VARCHAR(35) NOT NULL,
	state VARCHAR(25) NOT NULL,
    fips VARCHAR(10),
	cumul_cases INT NOT NULL,
    daily_cases INT NOT NULL, -- add if possible 
	deaths VARCHAR(10),
    PRIMARY KEY (submission_date, county, state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS VACCINATIONS;
CREATE TABLE VACCINATIONS(
    submission_date DATE NOT NULL,
    location VARCHAR(30) NOT NULL,
    total_vaccinations VARCHAR(20),
    total_distributed VARCHAR(20),
    people_fully_vaccinated VARCHAR(20),
    cumul_vaccinations VARCHAR(20),
    PRIMARY KEY (submission_date, location)
    -- FOREIGN KEY (location) REFERENCES STATE_POPULATION(state_name) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- clean up data
DELETE FROM COUNTY_INFECTIONS where county = "Unknown" OR fips = "";


-- insert data
LOAD DATA INFILE '/var/lib/mysql-files/us_state_vaccinations.csv'
INTO TABLE VACCINATIONS
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- insert county population data
LOAD DATA INFILE '/var/lib/mysql-files/population-counties.csv'
INTO TABLE COUNTY_POPULATION
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- delete unneccessary data columns which were in csv's
-- ALTER TABLE COUNTY_INFECTIONS DROP COLUMN deaths;
ALTER TABLE COUNTY_POPULATION DROP COLUMN area;
ALTER TABLE COUNTY_POPULATION DROP COLUMN density;

-- insert data into state table by summing county populations
INSERT INTO STATE_POPULATION(state_name, state_population)
SELECT cp.state_name, sum(population) from COUNTY_POPULATION as cp group by cp.state_name;

-- add the zero back to the fips codes that need it to match the infections table
UPDATE COUNTY_POPULATION SET fips_code = concat('0', fips_code) WHERE length(fips_code) = 4;
