from flask import Flask, render_template, request
from flask_restful import Resource, Api
from requests import put, get

import json
import threading
import payments.payment_manager
import data.tool_manager

app = Flask(__name__, template_folder="static")
api = Api(app)


tools = []
dates = []
library_id = None

with open(".name") as f:
    sharerName = f.read()

with open(".addr") as f:
    postal_address = f.read()


with open(".nameserverIP") as f:
    nameserver_ip = f.read()


class RESTTool(Resource):
    def get(self):
        print "get request"
        return {'tools': tools, 'date': dates, 'sharer_name': sharerName}

    def put(self):
        toolNo = request.form['toolNo']
        meetingTime = request.form['meetingTime']
        collectionTime = request.form['collectionTime']

        tool = tools[toolNo]

        if tool.isReserved:
            return {"error": "tool reserved"}

        # Otherwise, reserve the tool
        tool.setReserved = True

        tool.setMeetingTime = meetingTime
        tool.setCollectionTime = collectionTime

        # Now, send confirmation email to the user
        # with the QR code attached


        # Then return a confirmation
        return {"tool reserved": True}


api.add_resource(RESTTool, '/myTools')


@app.route("/")
def localLibraries():
    # Lookup the list of IP addresses from the name server:
    nameserver_address = "http://" + nameserver_ip + "/getLibraries"
    ips = put(nameserver_address, {'address': postal_address, 'ip': nameserver_ip}).json()['ips']
    print ips

    return render_template("html/ip_list.html", ips=ips)


@app.route("/show/<ip>")
def display(ip):
    address = "http://" + ip + "/myTools"
    try:
        data = get(address).json()
    except ValueError:
        # The host didn't return reasonable data
        # Just show the user an error message
        return "Whoops! We've had an issue connecting " \
               "to this library :( If you know this person, " \
                "try to get them to restart their server. " \
                "Otherwise, try again in a little while. "

    items = data['tools']
    dates = data['date']
    name = data['sharer_name']

    # Now we have to convert all the elements
    # in items to JSON objects before they are
    # passed. They come in as strings.
    json_items = []
    for item in items:
        json_items.append(json.loads(item))

    return render_template('html/item_list.html', items=json_items, name=name)


def update_nameserver():
    global library_id
    # Get the IP address of this server,
    # Then forward it to the nameserver.
    # In this instance, go local
    # todo -- make this global
    address = "http://" + nameserver_ip + "/ping"

    data = {'address': postal_address, 'id': library_id,
            'name': sharerName}

    try:
        library_id = put(address, data).json()['id']
    except Exception:
        print "Error updating nameserver, check address of " \
              "namesever or internet connection"

    print library_id
    # Set this on a loop to call itself every 6 seconds
    threading.Timer(6.0, update_nameserver).start()


if __name__ == '__main__':
    # Load the tools up from the config file
    tools = data.tool_manager.loadTools()

    # And start pinging the host server
    update_nameserver()

    app.run(host='0.0.0.0', port=80, debug=True)
