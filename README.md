# Globant Coding Challenge

### Dependencias:

- pip install pandas
- pip install Flasks

### Selected database: Sqlite3
- SQLite is file-based. It is not scalable, it's just for the exercise.

### Local REST API methods:

1 - Upload  (POST): Recieves a csv file and saves its data into the database. 

2 - Hired employees per job and department metric (GET): Returns a dataset with the number of employees hired for each job and department in 2021 divided by quarter. The table is ordered alphabetically by department and job.

3 - Departments that hired more than the mean metric (GET): Returns a dataset with the ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

### General comments
- Still remains to host the solution in a cloud public architecture and so the Dockerfile and the automated Tests.
- Because of time limits, the solution is not modelled correctly. Each request read the "transactional data" at the moment. It is not scalable and with a big volume of data the response could have a real delay. 
- For metrics per Q, Pivot window function could have been used, but Sqlite3 does not allow it. At the moment is is not supported. 
