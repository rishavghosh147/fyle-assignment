## Installation and Execution

## Method 1(using docker):
    
### 1. Clone the repository into your local machine using:

```
git clone https://github.com/rishavghosh147/fyle-assignment.git
```
   
### 2. For running the application on your local machine, please ensure that you have docker installed.
### 3. Run the application using docker:

```
docker-compose up
```

### 4. Application will run on port 7755.

## Method 2:

### 1. Clone the repository into your local machine using:

```
git clone https://github.com/rishavghosh147/fyle-assignment.git
```

### 2. Install all recurements(run in fyle-assignment folder):

```
pip3 install -r recurements.txt
```

### 3. Run server

```
bash run.sh
```

### 4. Application will run on port 7755.

## Run Tests

### 1. Run this command in fyle-assignment folder

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
pytest tests/ --cov-report html --cov
```

### 2. open htmlcov file to check coverage

## Some Extra test case has been added to make it more acurate(total 38 test case.)

``
*** my code coverage 99%.
*** some other code has been edited for make this application more acurate and more operational.
``
