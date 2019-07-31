# NYCCT-Course-Advisor
Project made in part for Credit Advisement for students of CityTech

This is an application to better improve the credit advisement given at CityTech. The goal with this project is to have more efficient course schedules for each semester created for students based on pre-requiste courses that they have. Students tend to typically graduate from CET department after 5years instead of the standard 4years due to not taken the correct courses at certain times so CreditTracker will be the solution.

## Getting Started

To get this project up and running,

1. Download the repo

2. Change directories into the root directory for the project within command prompt.

3. From here, you have to set FLASK config variable
   Windows command: set FLASK_APP=credit_calc.py
   Other platforms: export FLASK_APP=credit_calc.py
4. Run the following commands:
   flask run

After these steps, application should be running on localhost:5000 which you can view in a browser

	

### Prerequisites

What things you need to install the software and how to install them

```
Python
Flask
FlaskWTF (used for forms in our app)
Flask SQLAlchemy
Flask Migrate (used for database migrations for model changes)
Flask Login
Oauth2
venv (virtual enviroment holding the requirement packages above)

```

### Installing

Here is how to get the development env setup.

1. Install Python if it is not installed already.
2. If you have Python3 installed then you create a virtual enviroment with 
```
python3 -m venv 'name of venv'
```
Older versions of Python use
```
virtualenv venv
```
3. Use pip install <package name> (below are package names you will install)
       * flask
       * flask-wtf
       * flask-sqlalchemy
       * flask-migrate
       * flask-login
   As a easier way to make it more convenient for you all, please use the below command with the requirements.txt file to install the above packages
	pip install -r requirements.txt



## Running the tests

If the database is not populated when running the app locally, you can run the test_data.py file which will then import sample data.
```
python test_data.py
```

## Deployment

This project was deployed on Heroku and can be view live [here] (https://ct-credittracker.herokuapp.com/).

The deployment process will later be chronicled on [YouTube]

## Built With

* Python
* Flask
* HTML
* CSS
* Javascript
* JQuery


## Authors

* **Adam Hussain** - *Initial work* - [adamdevelops] (https://github.com/adamdevelops/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Miguel Grinberg and his book Flask Mega-Tutorial
* Professor Mendoza @ CityTech College

