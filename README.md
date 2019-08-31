# flask-tutorial

## Technologies used

* Python 3.7
* Flask

## Setup

Run the program via the terminal by entering;
```
$ flask run
```
Which should launch a simple local server at http://127.0.0.1:5000/

The flask script is nice to start a local development server, but you would have to restart it manually after each change to your code. That is not very nice and Flask can do better. If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong.

To enable all development features (including debug mode) you can export the FLASK_ENV environment variable and set it to development before running the server:

Tell Flask where to find your application
```
$ export FLASK_APP=flaskr
```
Then run it in development mode
```
$ export FLASK_ENV=development
$ flask run
```

To create a flaskr.sqlite file if missing from the ./instance file, run the
following command.
```
$ flask init-db
```
