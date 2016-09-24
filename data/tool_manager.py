import json

class RentalTool(object):
    def __init__(self, id, name, descr, price, rented, pickupDate, returnDate):
        self.id = id
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
    return [RentalTool("WRENCH", "Wrench", "A wrench", 100, False, None, None).toJSON()]

