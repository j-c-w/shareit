import json
import threading #aaaahhhh
import time

"""
The idea of this class is that
it is used to manage the libraries.

For the moment it writes out to disk and then
copies it all back in.

Ideally will use MongoDB in the future to
deal with the writing and reading
"""

# In seconds
TTL = 30

class LibraryManager(object):
    def __init__(self, datafile=".libraryData"):
        self.data = []
        # Also need to start the expiry timer:
        threading.Timer(30.0, self._cleanup).start()

    """ Takes a dictionary with 'ip', 'address' and
    'id' defined"""
    def update(self, message):
        message_id = message['id']
        message['refreshTime'] = time.time()
        new_item = True

        for index, item in enumerate(self.data):
            if item['id'] == message_id:
                new_item = False
                # Then replace the item here
                self.data[index] = message

        if new_item:
            # Then just add to the list
            self.data.append(message)

    """ This goes through the data list and
    clears out all the data with timestamps
    that were too long ago"""
    def _cleanup(self):
        current_time = time.time()

        for index, item in enumerate(self.data):
            if current_time - item['refreshTime'] > TTL:
                # delete the item and remove it:
                del self.data[index]

        # Then reschedule itself
        threading.Timer(30.0, self._cleanup).start()

    def getIPsNear(self, address):
        # todo -- implement a search for nearby addresses

        ips = []

        for item in self.data:
            ips.append(item['ip'])

        return ips



