import json
from requests import get

"""
The idea of the resolution packet is to contain the
IP address and the real address of the server,
along with a (potentially not yet set) ID that
the client has. The ID is so that the client can
update the information on file for it
as needed.
"""
class RouterInfo(object):
    def __init__(self):
        # Read in the address from the .addr
        # file
        with open(".addr") as f:
            self.address = f.read()

        # Further, read in the IP address
        # from elsewhere on the internet

        self.ip = \
            get('https://api.ipify.org?format=json').json()['ip']


        # Also, get the ID from the .id file if
        # it exists
        with open(".id") as f:
            self.id = f.read()

    def json(self):
        return json.dump(self.__dict__)
