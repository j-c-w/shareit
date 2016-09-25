from flask import Flask, render_template, request
from flask_restful import Resource, Api
from requests import put, get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json
import threading
import payments.payment_manager
import data.tool_manager
import smtplib
import uuid


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

with open(".email") as f:
    useremail = f.read()


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

    return render_template('html/item_list.html', items=json_items, name=name, ip=ip)


@app.route("/auth_loan_out/<transaction_id>")
def auth_loan_out(transaction_id):
    # At this point should have the ID from
    # the other server for confirmation
    # of the payment.
    if (payments.payment_manager.has_remote_conf(transaction_id)):
        # Make payment
        payments.payment_manager.make_payment(transaction_id)

        return "Payment made!"
    else:
        # Make sure that the payment can be made when the
        # other ID is received
        return "Pending on loanee to confirm payment, follow this link \
                again once the loanee has followed theirs"


@app.route("/auth_loaner/<transaction_id>")
def auth_loaner(transaction_id):
    # This is simpler, because the other side will
    # always initiate payments. Just send the confirmation.
    destination_address = payments.payment_manager.get_destination_address(transaction_id)
    confirmation_id = payments.payment_manager.get_auth_token(transaction_id)

    success = put(destination_address, {'confirmation_id': confirmation_id,
                              'transaction_id': transaction_id}).json()


    if success['Sucess']:
        return "Sucessfully authenticated payment"
    else:
        return "Failed to authenticate payment"



""" This deals with setting up the rental
from the perspective of this client.

Idea is to send an email to the user that
gives them a link they can follow once they
have completed the transaction. This
link does the payment processing. """
@app.route("/rent/<ip>/<id>")
def rent(ip, id):
    # The first step is to talk to the other server
    # to confirm the rent. Then, take back the name
    # and description of the item and use these
    # to craft an email.
    print "Item ID:" + id


    destinationAddress = "http://" + ip + "/rent_request"

    data_sent = {'transaction_id': generate_uuid(),
                 'item_id': id,
                 'sharerName': sharerName,
                 'loan_out_ip': ip}

    response = put(destinationAddress, data_sent).json()

    item_name = response['item_name']
    destination_postal_address = response['postal_address']
    own_ip = response['loaner_ip']
    amount = response['amount']

    confirmation_link = payments.payment_manager.generate_loaner_link(own_ip, ip, id, amount)

    # NOTE: the item_id here does not correspond
    # to an ID on this server.
    fromAddr = "shareit@shareit.com"
    toAddr = useremail

    email = MIMEMultipart("alternative")
    email['Subject'] = "Sharing " + id
    email['From'] = fromAddr
    email['To'] = useremail

    text = MIMEText("""
        This is to confirm your share request for """ +
                    id + """. To collect this
                      item, go to """ + destination_postal_address +
                      """ to pick it up :)
                      Once you have picked it up, click on the below
                      link to confirm your payment for the """ + item_name +
                      "\n\n" + confirmation_link, 'plain')

    email.attach(text)

    with smtplib.SMTP('localhost') as server:
        server.sendmail(email, fromAddr, toAddr)

    return "Confirmation emails sent! Go to " + \
            destination_postal_address + """ to
            pick up  your """ + item_name


class RentConfirmation(Resource):
    def put(self):
        transaction_id = request.form['transaction_id']
        auth_token = request.form['auth_token']

        payments.payment_manager.loanee_confirmation(transaction_id, auth_token)

        return {"success" : True}


class RentRequest(Resource):
    def put(self):
        print "rent request received"
        # We get the item_id and are expected
        # to return most of the  item.

        item_id = request.form['item_id']
        transaction_id = request.form['transaction_id']
        other_name = request.form['sharerName']
        own_ip = request.form['loan_out_ip']

        other_ip = request.environ['REMOTE_ADDR']

        print item_id
        print transaction_id
        print other_name
        print own_ip
        # Generate the confirmation link and
        # send it to yourself.

        item = data.tool_manager.item_from_id(item_id)

        item_name = item['name']
        item_amount = item['price']

        confirmation_link = payments.payment_manager.generate_loan_outter_link(transaction_id, own_ip, other_ip, item_id, item_amount)

        fromAddr = "shareit@shareit.com"
        toAddr = useremail

        email = MIMEMultipart("alternative")
        email['Subject'] = "Sharing " + item_id
        email['From'] = fromAddr
        email['To'] = useremail
        text = MIMEText("""There's been a request
            put in for your tool """ + item_name + """.
            """ + other_name + """ is coming to collect it.
            """ + """ The following is a link that you
            should click only when they have returned the
            tool in satisfactory condition to confirm
            the payment (before the payment is made,
            this platform will support a mediated form
            or renegotiation wrt the value of the tool
            """, 'text')

        email.attach(text)

        print "email created"

        with smtplib.SMTP('localhost') as server:
            server.sendmail(email, fromAddr, toAddr)

        print "email sent"

        # Now return the data that is needed on
        # the other end
        return {'item_name': item_name,
                'postal_address': postal_address,
                'loaner_ip': other_ip,
                'amount': item_amount}

api.add_resource(RentRequest, '/rent_request')
api.add_resource(RentConfirmation, '/auth_loaner')

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


def generate_uuid():
    return uuid.uuid4().int

if __name__ == '__main__':
    # Load the tools up from the config file
    tools = data.tool_manager.loadTools()

    # And start pinging the host server
    threading.Timer(6.0, update_nameserver).start()

    app.run(host='0.0.0.0', port=80, debug=True)
