# Pythonista.io

Pythonista.io is a project that I started to help aggregate python related jobs. Not
exclusive to web development. 
I based my idea on the simple observation that it was somewhat difficult to find a python
job, and I feel like creating a central hub for both companies and developers would
alleviate that frustration.
Personally, I tackled this project because I wanted to gain a deeper knowledge of Flask.
My goals were very specific:

- Learn how to design a REST API in python (using the best practices)
- Learn how to create and run unit tests (which I had never done before [shame on me])
- Learn postgreSQL and sqlAlchemy (I only had experience with MongoDB, mySQL and SQLite)
- Learn how to modularise a web project in python with the use of Blueprints
- Learn how to implement a 'Sign up with your email' functionality (including confirmation
  handling)
- Learn how to use some of the more advanced features of python like decorators
- Learn how to serve and deploy a flask / python app to a linux server 
and many more. 

Overall it was a very rewarding experience because it also enabled me to discover the
world of server administration and linux (both of which I really enjoy). It allowed to
play and experiment with tools like nginx, gunicorn, upstart (I learned about linux
runlevels, vagrant, port forwarding, users/groups and file permissions, threading)

## The concept

The idea is extremely basic, nothing that will revolutionise job applications on the web.
Companies can sign up for an account and publish jobs, which will then be displayed in a
nice looking interface where users will be able to filter based on the contract type.
There are 5 different contract types: Full Time, Part Time, Contract, Internship, Remote
Users can then access job ads and apply using the email address provided by the companies.
It will take the form of a simple clickable link with a mailto attribute.

## Some notes

This is a project that I devoted a lot of time to and I still am motivated to finish it.
However I can't afford to work on it full time anymore so if any of you reading this wish to
contribute and offer some help in the form of pull requests, you are more than welcome to
do so. 

I'm always keen on learning from more experienced developers and if you can teach a
young passionate dev some cool tricks and techniques don't hold back ! :smile: 

Ideally, the only thing I ask when making a contribution is to give an explanation as to
why the solution you're proposing is better (not because I have a massive ego, but by pure
curiosity)

## How to setup the project 

When downloading the project, you will need to create a virtual environment as this
project was developed using python 3.4.3

To do so you will need to navigate inside the project's directory and issue the following command:
```bash
    virtualenv -p python3 .
```
this will create a virtual environment in the current folder.

To activate the virtualenv just run:
``` source bin/activate
```

The next step will be to download the project's dependencies, to do so just quickly run:

```bash
    pip install -r requirements.txt
```

you can then either run:
```bash
    python wsgi.py
```
which will run a server on your localhost at port 5000. or you can replicate my setup by following [this tutorial](tutorial).

Rename the `config_example.py` file found inside the pythonista package `config.py` and
add your info and credentials to it.

if you chose to follow the tutorial linked above, to launch the server you simply have to
run
```bash
    sudo start pythonista
```
and the server should be running.

To view the site, open your browser and visit the url (or ip address) attached to your
server.

To run the tests just call 
```bash
    python manage.py test
```

The migrations are handled in three steps.

First, initialise the migrations

``` python
    python manage.py db init
```

Then run the migrations
``` bash
    python manage.py db migrate
```

and finally, upgrade the DB
```bash
    python manage.py db upgrade
```

## here is what is left to do on the project

- [ ] Create a reset password functionality
- [ ] Create a front end using a framework of your choice
- [ ] Refactor the tests 
- [ ] Test email confirmation functionality 
- [ ] Decorate /api/confirm/token with ogin required
- [ ] Refactor serialise_json decorator
- [ ] Check that the company (user) is confirmed before letting them log in

## Here are all the authentication and api endpoints

### Auth 

```
 /register GET 

 /login    GET 

 /login    POST 

 /logout   POST 
```

### API
```
/api/companies              GET

/api/companies              POST

/api/companies/id           GET 

/api/companies/id           PUT

/api/companies/id/jobs      GET 

/api/jobs                   GET

/api/jobs                   POST

/api/jobs/id                GET

/api/jobs/id                PUT

/api/jobs/<contract_type>   GET 

*contract types include full-time / part-time / internship / contract / remote*
```

## Other notes

All helper functions and methods are commented 

Tests are run using the unittest standard library (feel free to use the tool of your
choice)

## Next features to implement
- [ ] Profile pictures for companies
- [ ] Allow users to apply within the site

[tutorial]: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04





