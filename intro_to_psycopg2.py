import os
import psycopg2

# Create a cursor.
user = os.environ["USERNAME"]
host = os.environ['HOST']
cluster = os.environ["CLUSTER"]
password = os.environ["DATABASE_PW"]

connection = psycopg2.connect(user=user,
                              host=host,
                              port=26257,
                              database=f'{cluster}.defaultdb',
                              password=password,
                              sslmode='verify-full')

cursor = connection.cursor()


# Create a table
def create_tables():
    cursor.execute(
        "CREATE TABLE programs (id SERIAL PRIMARY KEY, name string)")
    connection.commit()

    cursor.execute("CREATE TABLE courses ( \
    id UUID NOT NULL DEFAULT gen_random_uuid(),\
    name STRING NOT NULL,\
    code INT NOT NULL, \
    program INT NOT NULL, \
    credits DECIMAL NULL, \
    CONSTRAINT fk_program FOREIGN KEY (program) REFERENCES programs(id) ON DELETE CASCADE \
    )")
    connection.commit()


# Insert data into a table.
def insert_data():
    cursor.execute("INSERT INTO programs VALUES (1, 'ece')")
    cursor.execute("INSERT INTO programs VALUES (2, 'cs')")
    cursor.execute("INSERT INTO programs VALUES (3, 'math')")
    connection.commit()

    cursor.execute(
        "INSERT INTO courses VALUES (default, 'Distributed Systems', 454, 1, 1.5)"
    )
    cursor.execute(
        "INSERT INTO courses (name, code, program) VALUES ('Databases', 348, 2)"
    )
    cursor.execute(
        "INSERT INTO courses (name, code, program) VALUES ('Programming for Performance', 459, 1)"
    )
    connection.commit()


# Update data in a table.
def update_rows():
    cursor.execute("UPDATE programs SET name = 'ECE' where name = 'ece'")
    cursor.execute("UPDATE programs SET name = 'CS' where name = 'cs'")
    cursor.execute("UPDATE programs SET name = 'MATH' where name = 'math'")
    connection.commit()


# Delete rows.
def delete_rows():
    cursor.execute("DELETE FROM courses WHERE code = 348")
    connection.commit()


def alter_table():
    cursor.execute("ALTER TABLE courses DROP COLUMN credits")
    connection.commit()

    cursor.execute("ALTER TABLE courses ADD COLUMN credits INT DEFAULT 1")
    connection.commit()


# Query a table.
def select_all():
    cursor.execute("SELECT * FROM programs")
    results = cursor.fetchall()
    print(results)
    print('\n')


def select_some():
    cursor.execute("SELECT * FROM courses WHERE credits > 0")
    results = cursor.fetchall()
    print(results)
    print('\n')


# Drop table.
def drop_tables():
    cursor.execute("DROP TABLE courses")
    connection.commit()

    cursor.execute("DROP TABLE programs")
    connection.commit()


def add_course_with_params(name, code, program, credits):
    cursor.execute("INSERT INTO courses VALUES (default, %s, %s, %s, %s)",
                   (name, code, program, credits))


create_tables()
insert_data()
update_rows()
delete_rows()
alter_table()
add_course_with_params("Algorithms", "341", 2, 1)
select_all()
select_some()
drop_tables()
