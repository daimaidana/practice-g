import sqlite3
from flask import *
import json
import pandas as pd
import logging
import os

app = Flask(__name__)

logging.basicConfig(filename='api_logs.log', level=logging.ERROR)

def create_tables():
    c = sqlite3.connect("globant.db").cursor()

    c.execute("DROP TABLE IF EXISTS departments")    
    c.execute("DROP TABLE IF EXISTS jobs")
    c.execute("DROP TABLE IF EXISTS hired_employees")

    c.execute("CREATE TABLE IF NOT EXISTS departments("
              "id INTEGER, department TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS jobs("
              "id INTEGER, job TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS hired_employees("
              "id INTEGER, name TEXT, datetime TEXT, department_id INTEGER, job_id INTEGER )")

    c.connection.close()


def create_tmp_general_view(cursor):
    
    cursor.execute('''
              CREATE TEMP VIEW tmp_sum_employees AS
              SELECT 
                j.id job_id, 
                j.job, 
                d.id department_id, 
                d.department, 
                CAST(strftime('%Y', he.datetime) as INTEGER) year, 
                CAST(strftime('%m', he.datetime) as INTEGER) month,
                count(*) employees_hired
              
                FROM hired_employees he
                INNER JOIN jobs j on j.id = he.job_id
                INNER JOIN departments d on d.id = he.department_id
                WHERE he.name is not null 
              
                group by 
                j.id, 
                j.job, 
                d.id, 
                d.department, 
                strftime('%Y', he.datetime), 
                strftime('%m', he.datetime);
              -- I use inner to guarantee integrity, assuming empty values are not correct. 
            ''')
    


@app.route('/upload', methods=['POST'])
def upload():
    db = sqlite3.connect("globant.db")

    file = request.files['file'] 
    name = file.filename
    name = os.path.splitext(name)[0]

    print(name)
    if name.upper() == 'DEPARTMENTS':
        df = pd.read_csv(file, names=['id', 'department'] )
        df.to_sql(name, db, if_exists='replace', index=False)
        db.commit()
        db.close()
        return json.dumps("Successfull import.")
    
    elif name.upper() == 'JOBS':
        df = pd.read_csv(file, names=['id', 'job'] )
        df.to_sql(name, db, if_exists='replace', index=False)
        db.commit()
        db.close()
        return json.dumps("Successfull import.")
    
    elif name.upper() == 'HIRED_EMPLOYEES':
        df = pd.read_csv(file, names=['id', 'name', 'datetime', 'department_id', 'job_id'] )
        df.to_sql(name, db, if_exists='replace', index=False)
        db.commit()
        db.close()
        return json.dumps("Successfull import.")
    
    else:
        db.close()
        return json.dumps("Files are not named correctly.")


@app.route('/employees-hired-per-job-and-department', methods=['GET'])
def get_employees_hired_per_job_and_department():
    
    db = sqlite3.connect("globant.db")
    c = db.cursor()

    create_tmp_general_view(c)

    c.execute('''
                SELECT 
                department, 
                job, 
                sum(case when month IN (1,2,3) then employees_hired else 0 end) as Q1,
                sum(case when month IN (4,5,6) then employees_hired else 0 end) as Q2,
                sum(case when month IN (7,8,9) then employees_hired else 0 end) as Q3,
                sum(case when month IN (10,11,12) then employees_hired else 0 end) as Q4
              
                FROM tmp_sum_employees 
                    where year = 2021
                group by
                department,
                job
                
                order by department asc, job asc;  ''') 

    rows = c.fetchall()
    db.close()
    
    return json.dumps(rows)


@app.route('/departments-that-hired-more-than-the-mean', methods=['GET'])
def get_departments_that_hired_more_than_the_mean():
    
    db = sqlite3.connect("globant.db")
    c = db.cursor()
    create_tmp_general_view(c)

    # Dataset para la media
    c.execute('''
              CREATE TEMP VIEW tmp_sum_departments as
                SELECT 
                department_id,
                sum(employees_hired) hired
                
                FROM tmp_sum_employees 
                    where year = 2021
                group by
                department_id;
              ''') 

    c.execute('''
              CREATE TEMP VIEW tmp_departments_list as
                SELECT 
                department_id
                
                FROM tmp_sum_employees 
                    
                group by
                department_id
              
                having sum(employees_hired) > ( Select avg(hired) from tmp_sum_departments );
               ''') 

    c.execute('''
                SELECT 
                department_id as id,
                department, 
                sum(employees_hired) as hired
              
                FROM tmp_sum_employees 
                    where department_id in (select department_id from tmp_departments_list)
              
                group by
                department_id,
                department 

              order by sum(employees_hired) desc;
              
              ''') 

    rows = c.fetchall()
    db.close()
    
    return json.dumps(rows)


if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=8888)
