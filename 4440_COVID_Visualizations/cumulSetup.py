import pymysql
import csv as csv

county_count = {}
count = 0


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password', # replace your db password here
                             db='covid_db')

try:
    with connection.cursor() as cur:
        testFile = open('us_counties_infections.csv')
        csv_reader = csv.reader(testFile, delimiter=',')


        for row in csv_reader:
            if count != 0 and row[3] != "" and row[5] != "":
                county_name = row[1]

                if "'" in county_name:
                    name_cleaner = county_name.split("'")
                    county_name = name_cleaner[0]

                fips = row[3]

                if fips in county_count:
                    diff = int(row[4]) - county_count[fips]
                    if not(int(row[4]) == county_count[fips]):
                        # add to count
                        county_count[fips] = county_count[fips] + diff
                    if diff < 0:
                        diff = 0
                else:
                    diff = int(row[4])
                    county_count[fips] = int(row[4])

              
                sql_line = "INSERT INTO COUNTY_INFECTIONS VALUES(" + "'" + row[0] + "', '" +  county_name + "', '" +  row[2] + "', '" + fips + "', " + row[4] + ", " + str(diff) + ", " + row[5] + ")"
               
               
                cur.execute(sql_line)
            count += 1
        
        connection.commit()
        testFile.close()

finally:
    connection.close()
