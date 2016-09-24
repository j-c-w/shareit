import json

class RentalTool(object):
    def __init__(self, name, descr, price, rented, pickupDate, returnDate):
        self.name = name
        self.descr = descr
        self.price = price
        self.rented = rented
        self.pickupDate = pickupDate
        self.returnDate = returnDate

    def toJSON(self):
        return json.dumps(self, default=lambda o:
                          o.__dict__, sort_keys=True,
                          indent=4)

def loadTools(configFile):
    # This loads in the various tools from the config file
    return [RentalTool("Wrench", "A wrench", 100, False, None, None).toJSON()]
