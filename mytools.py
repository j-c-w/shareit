from flask import Flask, render_template
from flask_restful import Resource, Api
from requests import put, get

import json
import urllib2
import payments.payment_manager
import data.tool_manager

app = Flask(__name__, template_folder="static")
api = Api(app)


tools = []
dates = []
with open(".name") as f:
    sharerName = f.read()


library_server_ip = '172.1.1.1'


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
    # TODO -- use the central server to lookup
    # Other IP addresses. For now, use local

    # For demo, setup an IP
    return "<a href='/show/172.16.14.41'>172.16.14.105</a>"


@app.route("/show/<ip>")
def display(ip):
    address = "http://" + ip + "/myTools"
    data = get(address).json()

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

if __name__ == '__main__':
    # Load the tools up from the config file
    tools = data.tool_manager.loadTools("./tools.conf")

    app.run(host='0.0.0.0', port=80, debug=True)
