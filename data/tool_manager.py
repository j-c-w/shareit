import json

tools = []

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

def loadTools(configFile=".tools"):
    # This loads in the various tools from the config file
    global tools

    with open(configFile) as f:
        lines = f.readlines()

        lines_index = 0

        while lines_index < len(lines):
            try:
                name = lines[lines_index]
                price = lines[lines_index + 1]
                description = lines[lines_index + 2]
                id = lines[lines_index + 3]

                tools.append(RentalTool(id, name, description, price, False, None, None).toJSON())

                lines_index += 5
            except IndexError:
                # Likely just an error with
                # how the configuration file
                # was written
                print "Unexpected end to item config" \
                      " file. Ensure it follows the correct" \
                      " standard."
    return tools

def item_from_id(item_id):
    for item in tools:
        # That is going to be slow
        item = json.load(item)
        if item['id'] == item_id:
            return item

    return None

