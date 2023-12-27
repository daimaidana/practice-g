import sqlite3
from flask import *
import json
import pandas as pd
import logging

app = Flask(__name__)

logging.basicConfig(filename='api_logs.log', level=logging.ERROR)


@app.route('/upload', methods=['POST'])
def upload_departments():
    db = sqlite3.connect("globant.db")

    file = request.files['file']
    name = file.filename.rstrip('.csv')

    df = pd.read_csv(file)

    df.to_sql(name, db, if_exists='replace', index=False)
    
    db.commit()
    db.close()

    return json.dumps("El import del archivo fue exitoso.")

@app.route('/getEmployeesHiredPerJobAndDepartment', methods=['GET'])
def getEmployeesHiredPerJobAndDepartment():
    
    db = sqlite3.connect("globant.db")

    c = db.cursor()
    c.execute("SELECT * from departments limit 1;")  # TO DO

    rows = c.fetchall()

    db.commit()
    db.close()
    
    return json.dumps(rows[0])


if __name__ == '__main__':
    app.run(debug=True, port=8888)
