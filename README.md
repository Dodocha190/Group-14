# Group-14
ClassMate: A web application designed to help you manage and review your university units
### Members:
1. 23340238, Rhianna Hepburn, username=rhiannahep
2. 23859997, Katherine Thio, username = Dodocha190
4. 23670072, Anna Tran, username=anatr5103
5. 24160206, Haidee Diamanta, username=haideedoo

#### Prerequisites:
python3
pip

### Config:
1. Create a virtual environment and activate it
    ```bash
    virtualenv venv
    source venv/bin/activate
    ```
    *(Replace `venv` with your preferred environment name if needed)*
2. Install all necessary requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Create a `.env` file
    * Create a file named `.env` in the root directory of your project.
    * Populate the `.env` file based on the format provided in the `.env.template` file.
    * **Important:** Choose and set your secret key within the `.env` file (e.g., `SECRET_KEY=your_secret_key_here`)
4. Set Flask Application
    ```bash
    export FLASK_APP=run.py:application
    ```
5. Run `flask db upgrade`
6. Run `flask run`


### Testing
1. To run selenium system tests:
    a. `python -m unittest test.systemTests`
2. To run unit tests:
    b.`python -m unittest test.unitTests`

