# Group-14
CITS3403 2025/1 Group 14 Project
### Members:
1. 23340238
2. 23859997
3. 23670072
4. 24160206


### Config:
1. Create a virtual environment and activate it\n 
    a. Run the following command: `virtualenv venv`\n
    b. Replace venv with your desired environment name if necessary\n
    c. Activate your virtual environment by running `source venv/bin/activate`
2. Install all necessary requirements\n
    a. `pip install -r requirements.txt`
3. Create a .env file in the root directory, following the .env .template format 
    a. Within this file, choose your secret key 
4. Run this in your terminal: `export FLASK_APP=run.py:application`
5. Run `flask db migrate`
6. Run `flask db upgrade`
7. Run `flask run`


### Testing
1. To run selenium system tests:
    a. `python -m unittest test.systemTests`
2. To run unit tests:
    b.`python -m unittest test.unitTests`

