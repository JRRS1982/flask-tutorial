import sqlite3

import click

# current_app is another special object that points to the Flask application
# handling the request. Since you used an application factory, there is no application 
# object when writing the rest of your code.

# g is a special object that is unique for each request. It is used to store 
# data that might be accessed by multiple functions during the request. The 
# connection is stored and reused instead of creating a new connection get_db 
# will be called when the application has been created and is handling a request
# , so current_app can be used.

from flask import current_app, g
from flask.cli import with_appcontext

def get_db()
  if 'db' not in g: 
    # sqlite3.connect() establishes a connection to the file pointed at by the
    #  DATABASE configuration key. This file doesn’t have to exist yet, and
    # won’t until you initialize the database later.
    g.db = sqlite3.connect(
      current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    # sqlite3.Row tells the connection to return rows that behave like dicts.
    # This allows accessing the columns by name.
    g.db.row_factory = sqlite3.Row

    return g.db


# close_db checks if a connection was created by checking if g.db was set. If
#  the connection exists, it is closed. Further down you will tell your
# application about the close_db function in the application factory so that it
# is called after each request.
def close_db(e=None):
  db = g.pop('db', None)

  if db is not None: 
    db.close()
