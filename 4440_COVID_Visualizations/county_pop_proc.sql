DROP PROCEDURE IF EXISTS calculate_covid_cases_county_ratio;
DELIMITER //
CREATE PROCEDURE calculate_covid_cases_county_ratio (TheDate DATE)
BEGIN 
	DROP TABLE IF EXISTS county_cases_and_pop;
    CREATE TABLE county_cases_and_pop(
        fips VARCHAR(10),
        county_name VARCHAR(35) NOT NULL,
        cumul_cases INT,
        population INT
    );
    INSERT INTO county_cases_and_pop
		SELECT c.fips, c.county, c.cumul_cases, p.population
        FROM (COUNTY_INFECTIONS AS c
        INNER JOIN COUNTY_POPULATION AS p
        ON (c.fips = p.fips_code))
        WHERE c.submission_date = TheDate;
        
        
END //
DELIMITER ;
