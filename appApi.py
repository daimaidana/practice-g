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
        db.commit()
        db.close()
        return json.dumps("Files are not named correctly.")


@app.route('/testQueries', methods=['GET'])
def testQueries():
    
    db = sqlite3.connect("globant.db")

    c = db.cursor()

    #c.execute("SELECT id, department from departments") 
    #c.execute("SELECT * from jobs") 
    c.execute("SELECT * from hired_employees limit 10") 


    rows = c.fetchall()

    print(rows)

    db.commit()
    db.close()
    
    return json.dumps("Success")


@app.route('/getEmployeesHiredPerJobAndDepartment', methods=['GET'])
def getEmployeesHiredPerJobAndDepartment():
    
    db = sqlite3.connect("globant.db")

    c = db.cursor()

    c.execute("SELECT * from departments") 

    rows = c.fetchall()

    print(rows)

    db.commit()
    db.close()
    
    return json.dumps(rows[0])


if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=8888)
