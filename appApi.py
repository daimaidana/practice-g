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

    c = db.cursor()

    file = request.files['file']
    
    df = pd.read_csv(file)

    df.to_sql('departments', db, if_exists='replace', index=False)
    
    db.commit()
    db.close()

    return json.dumps("El import del archivo fue exitoso.")


if __name__ == '__main__':
    app.run(debug=True, port=8888)
