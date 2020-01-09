from flask_tutorial import app, db
from flask_tutorial.models import User, Post


# decorator registers the items returned by it in the shell session.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
