DROP PROCEDURE IF EXISTS covid_vaccine_distribution_date_state;
DELIMITER //
CREATE PROCEDURE covid_vaccine_distribution_date_state(
	IN i_date date
)
BEGIN
	DROP TABLE IF EXISTS covid_vaccine_distribution_date_state_result;
    CREATE TABLE covid_vaccine_distribution_date_state_result(
        state_name VARCHAR(50),
        pop_vaccine INT
    );
    INSERT INTO covid_vaccine_distribution_date_state_result
		SELECT v.location, v.cumul_vaccinations
        FROM VACCINATIONS as v
        WHERE i_date = v.submission_date;
    
    UPDATE covid_vaccine_distribution_date_state_result
		SET 
			state_name = 'New York'
        WHERE 
			state_name = 'New York State';
        
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS covid_vaccine_ratio;
DELIMITER //
CREATE PROCEDURE covid_vaccine_ratio(
	IN i_date date
)
BEGIN
	DROP TABLE IF EXISTS covid_vaccine_ratio_result;
    CREATE TABLE covid_vaccine_ratio_result(
        state_name VARCHAR(50),
        pop_vaccine_ratio DOUBLE
    );
    UPDATE VACCINATIONS
		SET 
			location = 'New York'
        WHERE 
			location = 'New York State';
            
    INSERT INTO covid_vaccine_ratio_result
		SELECT c.state_name, (v.people_fully_vaccinated/c.tp * 100) as pop_vaccine_ratio
        FROM (SELECT state_name, sum(population) as tp FROM COUNTY_POPULATION group by state_name) as c
        left join (SELECT location, people_fully_vaccinated FROM VACCINATIONS WHERE i_date = submission_date) as v 
         on c.state_name = v.location;
        
END //
DELIMITER ;
