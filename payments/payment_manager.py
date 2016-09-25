import uuid
import md5

# The idea here is to interact with the
# payments SDK.

"""
This sends a payment of value 'amount' from
'username_from' to 'username_to'
"""

pending_payments_in = []
pending_payments_out = []


def make_payment(username_from, username_to, amount):
    pass


def generate_loan_outter_link(self, transaction_id, own_ip, dest_ip,
                              item_id, amount):
    payment_state = {'transaction_id': transaction_id,
                     'auth_token': None,
                     'amount': amount,
                     'dest_ip': dest_ip,
                     'remote_conf': False}
    pending_payments_in.append(payment_state)

    return "http://" + own_ip + "/auth_loan_out/" + transaction_id


def generate_loaner_link(self, transaction_id, own_ip, dest_ip, item_id, amount):
    # The idea is to send the auth token to the
    # other device when that link is scanned.
    # Then, accept payment when presented with
    # the correct auth_token.
    auth_token = uuid.uuid4().int

    # Add this to the pending payments list
    # (idea is to have this in a database
    # so it isn't quite so volatile)

    payment_state = {'transaction_id': transaction_id,
                     'auth_token': auth_token,
                     'dest_ip': dest_ip,
                     'amount': amount}
    pending_payments_out.append(payment_state)

    return "http://" + own_ip + "/auth_loaner/" + transaction_id


def has_remote_conf(transaction_id):
    for item in pending_payments_in:
        if item['transaction_id'] == transaction_id:
            return item['remote_conf']

    print "Transaction, ", transaction_id, "not found"
    return False


def get_destination_address(transaction_id):
    for item in pending_payments_out:
        if item['transaction_id'] == transaction_id:
            return item['dest_ip']


def get_auth_token(transaction_id):
    for item in pending_payments_out:
        if item['transaction_id'] == transaction_id:
            return item['auth_token']


def loanee_confirmation(transaction_id, auth_token):
    for item in pending_payments_out:
        if item['transaction_id'] == transaction_id:
            item['auth_token'] = auth_token
            item['remote_conf'] = True
