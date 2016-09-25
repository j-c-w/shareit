from flask import Flask, render_template, request
from flask_restful import Resource, Api
from requests import put, get

import uuid
import data.library_manager

"""
This is the server that deals with dishing out
the IPs and home addresses of the different
servers.

When a server starts up, it aims to provide
its information to the server so that the server
can dish that out to others that request
that information.

We make a decision based on locality as to which
servers we respond with first
"""

app = Flask(__name__, template_folder="static")
api = Api(app)

ips = data.library_manager.LibraryManager()


"""
This displays IPs in a user readable form
"""


@app.route("/")
def all_ips():
    ip_list = ips.getIPsNear("")
    # return " Hi there"
    # print ip_list
    return str(ip_list)


class ListFetch(Resource):
    def put(self):
        print "list fetch"
        # Returns a JSON list of all the IPs
        # todo -- take the address of the
        # sender and calculate the ones within
        # range

        address = request.form['address']

        # return just the ip addresses for
        # the sake of security
        return {'ips': ips.getIPsNear(address)}


class ListSet(Resource):
    def put(self):
        print "list update"
        address = request.form['address']
        name = request.form['name']
        ip = request.environ['REMOTE_ADDR']

        print "ip " + ip
        print "address " + address

        # The ID is a unique way for this
        #
        if 'id' in request.form:
            id = request.form['id']
        else:
            id = generate_id()


        # Now, create an entry in the list
        ips.update({'ip': ip, 'address': address,
                    'id': id, 'name': name})

        # Return the id as confirmation
        return {'id': id}


api.add_resource(ListFetch, "/getLibraries")
api.add_resource(ListSet, "/ping")


def generate_id():
    return uuid.uuid4()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
