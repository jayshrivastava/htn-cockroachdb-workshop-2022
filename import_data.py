import os
import psycopg2

# Create a cursor.
pg_conn_string = os.environ["PG_CONN_STRING"]

connection = psycopg2.connect(pg_conn_string)


# Set to automatically commit each statement
connection.set_session(autocommit=True)

cursor = connection.cursor()

# Columns
# id,NAME,host id,host_identity_verified,host name,neighbourhood group,neighbourhood,
# lat,long,country,country code,instant_bookable,cancellation_policy,room type,Construction year,price,service fee,minimum nights,number of reviews,last review,reviews per month,review rate number,calculated host listings count,availability 365,house_rules,license

# Rows
# 1006859,Cute & Cozy Lower East Side 1 bdrm,1280143094,verified,Miranda,Manhattan,Chinatown,
# 40.71344,-73.99037,United States,US,FALSE,flexible,Entire home/apt,2004,
# $319 ,$64 ,1,160,6/9/2019,1.33,3,4,1,,

cursor.execute(
    "CREATE TABLE airbnbs (id SERIAL PRIMARY KEY, title STRING, neighbourhood_group STRING, neighbourhood STRING, host_name STRING, verified BOOL, year INT)"
)

with open("airbnbs.csv", "r") as f:
    lines = f.readlines()
  
    # Print the column names
    first_line = lines[0].strip().split(',')
    print(first_line[0], first_line[1], first_line[5], first_line[6], first_line[4],
              first_line[3] == "verified", first_line[14])
  
    for line in lines[1:]:
        parts = line.strip().split(',')
      
        print(parts[0], parts[1], parts[5], parts[6], parts[4],
              parts[3] == "verified", parts[14])

        cursor.execute(
            "INSERT INTO airbnbs VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (parts[0], parts[1], parts[5], parts[6], parts[4], parts[3]
             == "verified", parts[14]))
