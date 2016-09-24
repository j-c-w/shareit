from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask("Eco", template_folder='static')
socketio = SocketIO(app)


@app.route('/')
def home_page():
    return render_template('html/login.html')


"""
This takes a 'username' and 'password' and does
a login. Either returns an AUTH_TOKEN to represent
all-ok or and error message if the login failed
"""
@socketio.on('login')
def login(message):
    pass


"""
This takes a message with a 'description' (a JSON
object that represents the description of the item)
and a list of 'group_ids' to post to. Also needs
an 'AUTH_TOKEN' to identify the user
"""
@socketio.on('post_item')
def post_item(message):
    # must make sure that the user posting
    # actually belongs to all the groups they
    # are posting to.
    pass


"""
This takes the 'AUTH_TOKEN' and a 'group_id'
and returns a list of all the items
that correspond to the group.
"""
@socketio.on('get_things')
def get_things(message):
    pass


"""
This takes the 'AUTH_TOKEN' and returns all the
groups that the user is a part of.
"""
@socketio.on('part_of')
def part_of(message):
    pass


"""
This takes the 'AUTH_TOKEN' and a group id and
joins the group
"""
@socketio.on('join_group')
def join_group(message):
    pass


"""
Takes the 'AUTH_TOKEN' and returns a
list of all defined groups
"""
@socketio.on('list_groups')
def  list_groups():
    pass

"""
Takes a group ID and returns some infromation
about it
"""
@socketio.on('group_information')
def group_information():
    pass
socketio.run(app)
