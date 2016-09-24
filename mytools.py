from flask import Flask, render_template
from flask_restful import Resource, Api

import payments.payment_manager
import data.tool_manager

app = Flask(__name__)
api = Api(app)


tools = []
dates = []

class RESTTool(Resource):
    def get(self):
        return {'tools': tools, 'date' : dates}

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

        # Deal with the payment
        payments.payment_manager.make_payment(producer, request.form['consumer'], request.form['amount'])

        # Then return a confirmation
        return {"tool reserved": True}



api.add_resource(RESTTool, '/myTools')

if __name__ == '__main__':
    # Load the tools up from the config file
    tools = data.tool_manager.loadTools("./tools.conf")

    app.run()
