import os
import psycopg2

# Create a cursor.
pg_conn_string = os.environ["PG_CONN_STRING"]
connection = psycopg2.connect(pg_conn_string)

cursor = connection.cursor()

# Create a table
def create_tables():
    cursor.execute("CREATE TABLE courses ( \
    id UUID NOT NULL DEFAULT gen_random_uuid(),\
    name STRING NOT NULL,\
    program STRING NOT NULL, \
    code INT NOT NULL, \
    credits DECIMAL NULL \
    )")
    connection.commit()

# Insert data into a table.
def insert_data():
    cursor.execute(
        "INSERT INTO courses VALUES (default, 'Distributed Systems', 'ece', 454, 1.5)"
    )
    cursor.execute(
        "INSERT INTO courses (name, program, code) VALUES ('Databases', 'cs', 348)"
    )
    cursor.execute(
        "INSERT INTO courses (name, program, code, credits) VALUES ('Programming for Performance', 'ece', 459, 1)"
    )
    connection.commit()

# Update data in a table.
def update_rows():
    cursor.execute("UPDATE courses SET program = 'ECE' where program = 'ece'")
    cursor.execute("UPDATE courses SET program = 'CS' where program = 'cs'")
    connection.commit()

# Delete rows.
def delete_rows():
    cursor.execute("DELETE FROM courses WHERE code = 459")
    connection.commit()

def alter_table():
    cursor.execute("ALTER TABLE courses DROP COLUMN credits")
    connection.commit()

    cursor.execute("ALTER TABLE courses ADD COLUMN credits INT DEFAULT 1")
    connection.commit()

# Query a table.
def select_all():
    cursor.execute("SELECT * FROM courses")
    results = cursor.fetchall()
    connection.commit()
    print(results)
    print('\n')

def select_some_with_params():
    cursor.execute("SELECT * FROM courses WHERE program = %s", ('ECE',))
    results = cursor.fetchall()
    connection.commit()
    print(results)
    print('\n')

# Drop table.
def drop_tables():
    cursor.execute("DROP TABLE courses")
    connection.commit()

def add_course_with_params():
    cursor.execute("INSERT INTO courses VALUES (default, %s, %s, %s, %s)",
                   ("Algorithms", "CS", "341", 1))
    connection.commit()

def add_course_with_named_params():
  data = {
    'name': 'Programming for Performance', 
    'code': '459', 
    'program': 'ECE',
  }
  cursor.execute("INSERT INTO courses VALUES (default, %(name)s, %(program)s, %(code)s)", data)

create_tables()
# insert_data()
# update_rows()
# delete_rows()
# alter_table()
# add_course_with_params()
# select_all()
# select_some_with_params()
# drop_tables()
